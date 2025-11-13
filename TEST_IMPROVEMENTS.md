# Testing Guide for New Improvements

## Quick Start - Test in 5 Minutes

### 1. Start the Server
```bash
cd /Users/vasupatel/Desktop/MedAgentica/Multi-Agent-Medical-Assistant
./run_server.sh
```

### 2. Test Health Endpoints

**Basic Health Check:**
```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy", "timestamp": "..."}
```

**Comprehensive Readiness Check:**
```bash
curl http://localhost:8000/health/ready | python -m json.tool
# Expected: Full system status with all checks
```

**Liveness Check:**
```bash
curl http://localhost:8000/health/live
# Expected: {"status": "alive", "timestamp": "..."}
```

**Metrics:**
```bash
curl http://localhost:8000/metrics | python -m json.tool
# Expected: {"active_sessions": N, "total_image_accesses": M, ...}
```

### 3. Test Session Expiry

**Upload an image:**
```bash
curl -X POST http://localhost:8000/upload \
  -F "image=@sample_images/chest_x-ray_covid_and_normal/covid.jpeg" \
  -F "text=Analyze this" \
  -c cookies.txt
```

**Check session is active:**
```bash
curl http://localhost:8000/metrics
# Note the active_sessions count
```

**Wait 2+ hours and check again:**
```bash
# Session should be automatically cleaned up
curl http://localhost:8000/metrics
# active_sessions should be lower
```

### 4. Test Audit Logging

**Watch the logs:**
```bash
tail -f server.log | grep AUDIT
```

**Perform actions:**
```bash
# Upload image
curl -X POST http://localhost:8000/upload \
  -F "image=@sample_images/chest_x-ray_covid_and_normal/covid.jpeg" \
  -F "text=test" \
  -b cookies.txt

# You should see in logs:
# AUDIT: action=IMAGE_STORED session=abc12345... details=path=...
# AUDIT: action=IMAGE_UPLOAD session=abc12345... details=filename=covid.jpeg
```

### 5. Test Secure Cookies

**Make a request and inspect cookies:**
```bash
curl -v -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello", "conversation_history": []}' \
  2>&1 | grep -i "set-cookie"
```

**Expected cookie attributes:**
- `HttpOnly` - ✅ Present (prevents XSS)
- `SameSite=strict` - ✅ Present (prevents CSRF)
- `Max-Age=7200` - ✅ Present (2 hour expiry)

### 6. Run Unit Tests

**Install test dependencies:**
```bash
pip install pytest pytest-cov
```

**Run all tests:**
```bash
python -m pytest tests/ -v
```

**Run specific test:**
```bash
python -m pytest tests/unit/test_session_management.py -v
python -m pytest tests/unit/test_error_handling.py -v
```

**Run with coverage:**
```bash
python -m pytest --cov=. --cov-report=html tests/
open htmlcov/index.html  # View coverage report
```

### 7. Test Error Handling

**Test retry mechanism:**
```python
from utils.error_handling import retry_api_call

@retry_api_call
def test_function():
    # Will retry up to 3 times if it fails
    return "success"

result = test_function()
print(result)
```

**Test circuit breaker:**
```python
from utils.error_handling import CircuitBreaker

breaker = CircuitBreaker(failure_threshold=3)

def unreliable_function():
    import random
    if random.random() < 0.5:
        raise Exception("Failed")
    return "Success"

try:
    result = breaker.call(unreliable_function)
    print(result)
except Exception as e:
    print(f"Error: {e}")
```

---

## Detailed Testing Scenarios

### Scenario 1: Session Lifecycle

**1. Create Session:**
```bash
curl -X POST http://localhost:8000/upload \
  -F "image=@sample_images/chest_x-ray_covid_and_normal/normal.jpeg" \
  -F "text=analyze" \
  -c session_cookies.txt
```

**2. Use Session:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What does the image show?", "conversation_history": []}' \
  -b session_cookies.txt
```

**3. Check Session in Logs:**
```bash
grep "session=" server.log | tail -5
```

**Expected:**
- `AUDIT: action=IMAGE_STORED`
- `AUDIT: action=IMAGE_ACCESSED`
- Session ID consistently used

---

### Scenario 2: Health Monitoring

**1. Check System Health:**
```bash
curl http://localhost:8000/health/ready | python -m json.tool
```

**Expected Response:**
```json
{
  "server": "ok",
  "config": "ok",
  "agent_system": "ok",
  "upload_directories": "ok",
  "session_storage": "ok (N active sessions)",
  "overall_status": "ready",
  "timestamp": "2025-11-13T..."
}
```

**2. Monitor Metrics Over Time:**
```bash
# Every 10 seconds, check metrics
watch -n 10 'curl -s http://localhost:8000/metrics | python -m json.tool'
```

**3. Use in Kubernetes:**
```yaml
livenessProbe:
  httpGet:
    path: /health/live
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /health/ready
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
```

---

### Scenario 3: Error Resilience

**1. Test with Network Issues:**
```python
from utils.error_handling import retry_with_backoff, RetryConfig
import requests

@retry_with_backoff(RetryConfig(max_attempts=3, initial_delay=0.5))
def fetch_data():
    # This will retry on connection errors
    return requests.get("https://api.example.com/data", timeout=5)

try:
    data = fetch_data()
    print(data.json())
except Exception as e:
    print(f"Failed after retries: {e}")
```

**2. Test Circuit Breaker:**
```python
from utils.error_handling import CircuitBreaker
import time

breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=5)

def flaky_service():
    # Simulates unreliable service
    import random
    if random.random() < 0.7:
        raise ConnectionError("Service unavailable")
    return "Success"

# Will open circuit after 3 failures
for i in range(10):
    try:
        result = breaker.call(flaky_service)
        print(f"Attempt {i+1}: {result}")
    except Exception as e:
        print(f"Attempt {i+1}: {e}")
    time.sleep(1)
```

---

## Performance Testing

### Load Testing with Apache Bench

**Test health endpoint:**
```bash
ab -n 1000 -c 10 http://localhost:8000/health
```

**Test chat endpoint:**
```bash
ab -n 100 -c 5 -p chat_payload.json -T application/json http://localhost:8000/chat
```

**chat_payload.json:**
```json
{"query": "Hello", "conversation_history": []}
```

### Memory Leak Testing

**Monitor session cleanup:**
```bash
# Start monitoring
watch -n 5 'curl -s http://localhost:8000/metrics | grep active_sessions'

# Upload many images
for i in {1..20}; do
  curl -X POST http://localhost:8000/upload \
    -F "image=@sample_images/chest_x-ray_covid_and_normal/normal.jpeg" \
    -F "text=test $i"
  sleep 1
done

# Wait 2+ hours and verify sessions are cleaned up
```

---

## Troubleshooting

### Issue: Health check fails

**Check logs:**
```bash
tail -50 server.log | grep ERROR
```

**Verify dependencies:**
```bash
python -c "from config import Config; c = Config(); print('Config OK')"
python -c "from agents.agent_decision import init_agent_state; s = init_agent_state(); print('Agents OK')"
```

### Issue: Tests fail

**Check Python version:**
```bash
python --version  # Should be 3.9+
```

**Install dependencies:**
```bash
pip install -r requirements.txt
pip install pytest pytest-cov
```

**Run tests in verbose mode:**
```bash
python -m pytest tests/ -v -s
```

### Issue: Sessions not expiring

**Check background worker:**
```bash
grep "Cleaned up.*expired sessions" server.log
```

**Verify configuration:**
```bash
grep "SESSION_EXPIRY_HOURS" web/app.py
```

---

## Success Criteria

All improvements are working if:

1. ✅ Health endpoints return 200 with correct data
2. ✅ Secure cookies have HttpOnly + SameSite attributes
3. ✅ Sessions expire after 2 hours
4. ✅ Audit logs show all actions
5. ✅ Unit tests pass (>90% passing)
6. ✅ Integration tests pass
7. ✅ Metrics endpoint shows accurate data
8. ✅ No memory leaks (sessions cleaned up)
9. ✅ Error handling prevents crashes
10. ✅ Logs are structured and parseable

---

## Next Steps

After verifying all improvements work:

1. **Deploy to staging** - Test in staging environment
2. **Monitor metrics** - Set up monitoring dashboard
3. **Load testing** - Perform comprehensive load tests
4. **Security audit** - Run security scanning tools
5. **Documentation** - Update API documentation

---

**Status**: All critical improvements implemented and ready for testing ✅

