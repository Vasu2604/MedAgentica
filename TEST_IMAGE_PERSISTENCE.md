# Testing Guide: Image Persistence & Routing Fix

## Overview
This guide walks you through testing the newly implemented image persistence and routing fix that allows users to upload an image once and then ask multiple follow-up questions about it.

## Prerequisites

1. **Server must be running**:
   ```bash
   cd /Users/vasupatel/Desktop/MedAgentica/Multi-Agent-Medical-Assistant
   ./run_server.sh
   ```

2. **Open browser** and navigate to:
   ```
   http://localhost:8000
   ```

## Test Case 1: Brain MRI Analysis with Follow-up

### Steps:

1. **Upload a brain MRI image**
   - Click the image upload button
   - Select a brain MRI image from `sample_images/` or your own
   - The system should analyze it and display results

2. **Ask follow-up questions** (WITHOUT re-uploading):
   - Type: "Can you analyze the image?"
   - Expected: ✅ System should analyze the stored image, NOT ask for upload
   
   - Type: "What does this image show?"
   - Expected: ✅ System should reference the previously analyzed image
   
   - Type: "Is there a tumor in the scan?"
   - Expected: ✅ System should use the stored brain MRI

### Expected Routing:
- All follow-up queries should route to **BRAIN_TUMOR_AGENT**
- System should display analysis results (tumor classification, probabilities, etc.)
- Console should show: `🔍 User query mentions image analysis - Using stored image: ...`

### What NOT to expect:
- ❌ "Please upload the image in question"
- ❌ "To better assist you, could you please upload the image?"
- ❌ Routing to CONVERSATION_AGENT asking for upload

---

## Test Case 2: Chest X-ray Analysis with Follow-up

### Steps:

1. **Upload a chest X-ray image**
   - Upload from `sample_images/chest_x-ray_covid_and_normal/`
   - System should perform MedRAX analysis (18-disease classification)

2. **Ask follow-up questions**:
   - Type: "Analyze the image"
   - Expected: ✅ System should analyze the stored X-ray
   
   - Type: "Does it show COVID-19?"
   - Expected: ✅ System should use the stored chest X-ray
   
   - Type: "What pathologies are detected?"
   - Expected: ✅ System should reference the previous analysis

### Expected Routing:
- All follow-up queries should route to **CHEST_XRAY_AGENT**
- System should display:
  - Original X-ray image
  - Segmentation overlay (if available)
  - Disease grounding visualization (if available)
  - Pathology probabilities
- Console should show: `🔍 User query mentions image analysis - Using stored image: ...`

---

## Test Case 3: Skin Lesion Analysis with Follow-up

### Steps:

1. **Upload a skin lesion image**
   - Upload from `sample_images/skin_lesion_images/`
   - System should classify as benign or malignant

2. **Ask follow-up questions**:
   - Type: "Can you analyze the image?"
   - Expected: ✅ System should analyze the stored skin lesion
   
   - Type: "Is it cancerous?"
   - Expected: ✅ System should use the stored skin lesion
   
   - Type: "What's the classification?"
   - Expected: ✅ System should reference the previous analysis

### Expected Routing:
- All follow-up queries should route to **SKIN_LESION_AGENT**
- System should display benign/malignant classification
- Console should show: `🔍 User query mentions image analysis - Using stored image: ...`

---

## Test Case 4: Multiple Query Types

### Steps:

1. **Upload an image** (any type)
2. **Ask various types of follow-up queries**:
   
   **Direct analysis requests:**
   - "analyze the image"
   - "examine the picture"
   - "check the scan"
   - "diagnose this"
   
   **Question-based queries:**
   - "What does the image show?"
   - "Is there anything concerning?"
   - "What's wrong with the scan?"
   - "Can you detect any abnormalities?"
   
   **Specific medical queries:**
   - "Does it show COVID?"
   - "Is there a tumor?"
   - "Is it benign or malignant?"

### Expected Behavior:
- ✅ ALL queries should automatically use the stored image
- ✅ ALL queries should route to the appropriate medical vision agent
- ❌ NONE should ask user to re-upload the image

---

## Test Case 5: Session Persistence

### Steps:

1. **Upload an image**
2. **Ask follow-up question** - should work ✅
3. **Refresh the page** (browser refresh)
4. **Ask follow-up question again**

### Expected Behavior:
- After refresh, session cookie should persist
- Image should still be available in session
- Follow-up questions should still work ✅

**Note**: If cookies are cleared, session will be lost and user needs to re-upload.

---

## Test Case 6: No Image Uploaded

### Steps:

1. **Start a new session** (new browser tab or clear cookies)
2. **WITHOUT uploading an image**, type: "Can you analyze the image?"

### Expected Behavior:
- ✅ System should recognize NO image was uploaded yet
- ✅ CONVERSATION_AGENT should politely ask user to upload an image
- Expected response: "I don't see any image uploaded yet. Please upload the medical image you'd like me to analyze."

---

## Console Debugging

When testing, monitor the server console for these log messages:

### Successful Image Storage:
```
📸 Stored image for session <session_id>: /path/to/image.jpg
```

### Successful Image Retrieval:
```
✅ Retrieved image for session <session_id>: /path/to/image.jpg
🔍 User query mentions image analysis - Using stored image: /path/to/image.jpg
```

### Image Not Found:
```
⚠️ User mentions image but no stored image found for session <session_id>
```

### Routing Success:
```
Selected agent: BRAIN_TUMOR_AGENT
Selected agent: CHEST_XRAY_AGENT
Selected agent: SKIN_LESION_AGENT
```

---

## Troubleshooting

### Issue: Follow-up queries still ask for upload

**Check**:
1. Is the image analysis keyword in the query?
   - Keywords: analyze, image, picture, scan, x-ray, mri, check, examine, diagnose
2. Is the session cookie being set?
   - Check browser dev tools → Application → Cookies → `session_id`
3. Is the image actually stored in session?
   - Check console logs for `📸 Stored image for session...`

**Fix**:
- Ensure cookies are enabled
- Don't use incognito mode (session won't persist)
- Check console for error messages

---

### Issue: Wrong agent is being used

**Check**:
1. What type of image was uploaded?
2. What was the query?
3. Check console logs for routing decision

**Fix**:
- Use specific keywords in query (e.g., "chest x-ray", "brain mri", "skin lesion")
- Check `image_type` classification in console

---

### Issue: Image not found error

**Check**:
1. Was the image successfully uploaded?
2. Does the file still exist on disk?
3. Check console for file path

**Fix**:
- Re-upload the image
- Ensure upload directory has write permissions
- Check disk space

---

## Success Criteria

The fix is working correctly if:

1. ✅ User can upload image once
2. ✅ User can ask multiple follow-up questions without re-uploading
3. ✅ All follow-up queries automatically use stored image
4. ✅ System routes to appropriate medical vision agent
5. ✅ CONVERSATION_AGENT doesn't ask for upload when image exists
6. ✅ Console shows correct session storage and retrieval logs
7. ✅ Session persists across page refreshes (until cookies cleared)

---

## Test Results Template

Use this template to document your test results:

```
## Test Results - [Date]

### Test Case 1: Brain MRI
- Upload: ✅/❌
- Follow-up 1 ("analyze image"): ✅/❌
- Follow-up 2 ("what does it show"): ✅/❌
- Routing: BRAIN_TUMOR_AGENT ✅/❌
- Notes: ___________________________

### Test Case 2: Chest X-ray
- Upload: ✅/❌
- Follow-up 1 ("analyze image"): ✅/❌
- Follow-up 2 ("does it show COVID"): ✅/❌
- Routing: CHEST_XRAY_AGENT ✅/❌
- Notes: ___________________________

### Test Case 3: Skin Lesion
- Upload: ✅/❌
- Follow-up 1 ("analyze image"): ✅/❌
- Follow-up 2 ("is it cancerous"): ✅/❌
- Routing: SKIN_LESION_AGENT ✅/❌
- Notes: ___________________________

### Test Case 4: Session Persistence
- Before refresh: ✅/❌
- After refresh: ✅/❌
- Notes: ___________________________

### Test Case 5: No Image
- Correct response: ✅/❌
- Notes: ___________________________

### Overall Result: PASS/FAIL
```

---

## Additional Notes

- **Session Duration**: Sessions persist until cookies are cleared
- **Concurrent Users**: Each user has their own session with isolated image storage
- **Security**: File paths are not exposed to frontend; only served via static file routes
- **Performance**: Minimal overhead; only stores file path in memory per session

---

## Need Help?

If tests are failing, check:
1. Server logs in `server.log`
2. Browser console for JavaScript errors
3. Network tab for API request/response details
4. File permissions on upload directories

For debugging, enable verbose logging by setting environment variable:
```bash
export DEBUG=1
./run_server.sh
```

