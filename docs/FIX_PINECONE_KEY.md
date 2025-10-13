# 🔑 Fix Pinecone API Key Issue

## ❌ Problem Detected

Your Pinecone API key is **invalid or incorrect**.

Error: `(401) Unauthorized - Invalid API Key`

---

## ✅ Solution (2 Steps)

### Step 1: Get Your Correct Pinecone API Key

1. **Go to Pinecone Dashboard:**
   ```
   https://app.pinecone.io/
   ```

2. **Sign in** to your account

3. **Navigate to API Keys:**
   - Click on your project name (top left)
   - Click "API Keys" in the left sidebar
   - OR go directly to: https://app.pinecone.io/organizations/-/projects/-/keys

4. **Copy your API key:**
   - Click "Create API Key" if you don't have one
   - Or copy your existing key
   - It should look like: `pcsk_xxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

### Step 2: Update Your .env File

**Option A: Use the setup script (Easiest)**

```bash
cd /Users/vasupatel/Desktop/MedAgentica/Multi-Agent-Medical-Assistant
python setup_evaluation.py
```

When prompted, paste your correct Pinecone API key.

**Option B: Edit .env file directly**

```bash
# Open .env file
nano .env

# Update this line with your correct key:
PINECONE_API_KEY=pcsk_your_actual_key_here

# Save: Ctrl+O, Enter, Ctrl+X
```

**Option C: Export directly (temporary)**

```bash
export PINECONE_API_KEY='pcsk_your_actual_key_here'
```

---

## ✅ Verify the Fix

After updating your API key, run:

```bash
cd /Users/vasupatel/Desktop/MedAgentica/Multi-Agent-Medical-Assistant
python check_evaluation_setup.py
```

You should see:
```
✅ Pinecone Connection: Connected
✅ Index 'medagentica': Found
```

---

## 🔍 Common Issues

### Issue 1: "Still getting 401 error"
**Solution:** Make sure you copied the **entire** API key, including the `pcsk_` prefix

### Issue 2: "Can't find API key in Pinecone dashboard"
**Solutions:**
- Create a new key: Click "Create API Key" button
- Check you're in the right organization/project
- Make sure you have appropriate permissions

### Issue 3: "Environment variable not loading"
**Solution:** Reload environment:
```bash
cd /Users/vasupatel/Desktop/MedAgentica/Multi-Agent-Medical-Assistant
export $(cat .env | grep -v '^#' | xargs)
```

---

## 📋 Quick Checklist

- [ ] Logged into Pinecone dashboard
- [ ] Copied correct API key (starts with `pcsk_`)
- [ ] Updated .env file or ran setup_evaluation.py
- [ ] Reloaded environment variables
- [ ] Ran check_evaluation_setup.py
- [ ] All checks pass ✅

---

## 🚀 Next Steps (After Fix)

Once Pinecone connection works:

1. **Check if index has data:**
   ```bash
   python check_evaluation_setup.py
   ```
   
2. **If index is empty, ingest data:**
   ```bash
   python demo_ingest_pinecone.py
   ```

3. **Run evaluation:**
   ```bash
   python quick_evaluate.py
   ```

---

## 💡 Alternative: Use Different Index

If you have a different Pinecone index you want to use:

1. Update index name in .env:
   ```bash
   PINECONE_INDEX_NAME=your_index_name
   ```

2. Or specify when running:
   ```bash
   export PINECONE_INDEX_NAME='your_index_name'
   python quick_evaluate.py
   ```

---

## 🆘 Still Need Help?

### Check Your API Key Format:
```bash
echo $PINECONE_API_KEY
```

Should show something like: `pcsk_xxxxx-xxxx-xxxx...`

If it shows your old/wrong key, you need to reload:
```bash
source .env
# OR
export $(cat .env | grep -v '^#' | xargs)
```

### Verify .env file contents:
```bash
cat .env | grep PINECONE
```

Should show:
```
PINECONE_API_KEY=pcsk_your_actual_key
PINECONE_INDEX_NAME=medagentica
```

---

## 🎯 Summary

**The fix is simple:**

1. Get correct Pinecone API key from: https://app.pinecone.io/
2. Run: `python setup_evaluation.py`
3. Paste your correct key when prompted
4. Verify: `python check_evaluation_setup.py`

**That's it! Your Pinecone connection will work!** 🎉

---

**Need your Pinecone key? Go here:** https://app.pinecone.io/organizations/-/projects/-/keys

