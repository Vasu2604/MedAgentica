# Quick Test Guide - Image Routing Fixes

## How to Test the Fixes

### 🧪 Test Case 1: Brain MRI Image (Q1 Fix)

**Before the fix:**
- Brain MRI → misrouted to CHEST_XRAY_AGENT ❌

**After the fix:**
- Brain MRI → correctly routed to BRAIN_TUMOR_AGENT ✅

**How to test:**
1. Start the web application:
   ```bash
   cd web
   python app.py
   ```

2. Open browser: `http://localhost:8000`

3. Upload a Brain MRI image (the one from your screenshot)

4. Type query: "can u analyze the image for me?"

5. **Expected result:**
   - System should analyze the image
   - Output: "BRAIN MRI (confidence: 0.70-0.85)"
   - Routes to **BRAIN_TUMOR_AGENT**
   - Shows tumor classification results

6. **What to look for in terminal logs:**
   ```
   🖼️ Analyzing NEW image: uploads/brain_mri_xxx.jpg
   [ImageAnalyzer] Heuristic Analysis:
     - Image dimensions: 512x512
     - Aspect ratio: 1.00
     - Gray mean: 65.23
     - Is square aspect: True
     - Skin lesion score: 0
     - Brain MRI score: 8
     - X-ray score: 5
   
   🔍 ANALYZED IMAGE TYPE: BRAIN MRI (confidence: 0.75)
      Reasoning: Square grayscale medical image, likely brain MRI
      (score: 8 vs X-ray: 5)
   
   ✅ Routing brain MRI to BRAIN_TUMOR_AGENT
   ```

---

### 🧪 Test Case 2: Chest X-ray Image (Verification)

**Expected:**
- Chest X-ray → correctly routed to CHEST_XRAY_AGENT ✅

**How to test:**
1. Upload a Chest X-ray image

2. Type query: "Analyze this chest X-ray"

3. **Expected result:**
   - System should analyze the image
   - Output: "CHEST X-RAY (confidence: 0.80-0.90)"
   - Routes to **CHEST_XRAY_AGENT**
   - Shows MedRAX analysis with 3 images

4. **What to look for in terminal logs:**
   ```
   🖼️ Analyzing NEW image: uploads/chest_xray_xxx.jpg
   [ImageAnalyzer] Heuristic Analysis:
     - Image dimensions: 768x1024
     - Aspect ratio: 0.75
     - Gray mean: 145.67
     - Is square aspect: False
     - Skin lesion score: 0
     - Brain MRI score: 3
     - X-ray score: 9
   
   🔍 ANALYZED IMAGE TYPE: CHEST X-RAY (confidence: 0.85)
      Reasoning: Rectangular grayscale image with X-ray intensity
      (score: 9)
   
   ✅ Routing chest X-ray to CHEST_XRAY_AGENT
   ```

---

### 🧪 Test Case 3: Ambiguous/Unknown Image (Q2 Fix)

**Before the fix:**
- Ambiguous image → defaulted to CHEST_XRAY_AGENT ❌
- No clarification prompt ❌

**After the fix:**
- Ambiguous image → asks for clarification ✅
- User specifies type → routes correctly ✅

**How to test:**
1. Upload an ambiguous medical image (or manipulated image with low confidence)

2. Type query: "What is this?"

3. **Expected result - Step 1 (Clarification Request):**
   ```
   Assistant: "I see you've uploaded a medical image, but I'm having 
   difficulty determining what type of image it is.

   To route your image to the correct specialist agent, could you 
   please tell me what type of medical image this is?

   **Please specify one of the following:**
   - Chest X-ray - For lung, chest, or respiratory conditions
   - Brain MRI - For brain or neurological conditions
   - Skin lesion - For skin conditions, moles, rashes

   **Examples:**
   - "This is a chest X-ray"
   - "It is a skin lesion"
   - "This is a brain MRI"

   What type of medical image is this?"
   ```

4. **User clarifies by typing:** "It's a brain MRI"

5. **Expected result - Step 2 (Correct Routing):**
   - System detects "brain" keyword
   - Routes to **BRAIN_TUMOR_AGENT**
   - Shows tumor classification results

6. **What to look for in terminal logs:**
   ```
   🖼️ Analyzing NEW image: uploads/unknown_xxx.jpg
   [ImageAnalyzer] Heuristic Analysis:
     - Skin lesion score: 1
     - Brain MRI score: 4
     - X-ray score: 4
   
   🔍 ANALYZED IMAGE TYPE: BRAIN MRI (confidence: 0.45)
      Reasoning: Square grayscale image (MRI: 4, X-ray: 4),
      defaulting to brain MRI with low confidence
   
   ❓ Unknown/ambiguous image type (BRAIN MRI, confidence: 0.45)
      - Routing to CONVERSATION_AGENT for clarification
   
   [User response: "It's a brain MRI"]
   
   ✅ User clarified image type as BRAIN MRI
      - Routing to BRAIN_TUMOR_AGENT
   ```

---

### 🧪 Test Case 4: Skin Lesion Image (Verification)

**Expected:**
- Skin lesion → correctly routed to SKIN_LESION_AGENT ✅

**How to test:**
1. Upload a skin lesion image

2. Type query: "Is this skin cancer?"

3. **Expected result:**
   - System should analyze the image
   - Output: "SKIN LESION (confidence: 0.75-0.85)"
   - Routes to **SKIN_LESION_AGENT**
   - Shows benign/malignant classification

4. **What to look for in terminal logs:**
   ```
   🖼️ Analyzing NEW image: uploads/skin_xxx.jpg
   [ImageAnalyzer] Heuristic Analysis:
     - Image dimensions: 640x480
     - Aspect ratio: 1.33
     - Gray mean: 125.45
     - Saturation: 65.23
     - Is square aspect: False
     - Skin lesion score: 7
     - Brain MRI score: 1
     - X-ray score: 2
   
   🔍 ANALYZED IMAGE TYPE: SKIN LESION (confidence: 0.80)
      Reasoning: Colorful image with warm tones (score: 7),
      likely skin lesion
   
   ✅ Routing skin lesion to SKIN_LESION_AGENT
   ```

---

## Understanding the Logs

### Key Metrics to Watch:

1. **Aspect Ratio**
   - **1.00** (square) → likely Brain MRI
   - **0.75-0.85** (rectangular) → likely Chest X-ray
   - **1.2-1.5** (slightly wider) → could be anything

2. **Gray Mean** (average brightness)
   - **< 80** → likely Brain MRI (darker)
   - **80-220** → likely Chest X-ray (brighter)
   - **> 100 with color** → likely Skin Lesion

3. **Scores**
   - **Skin Lesion ≥ 4** → routes to SKIN_LESION_AGENT
   - **Brain MRI ≥ 6** → routes to BRAIN_TUMOR_AGENT
   - **X-ray ≥ 7** → routes to CHEST_XRAY_AGENT
   - **All scores < 3** → asks for clarification

4. **Confidence**
   - **≥ 0.70** → High confidence, routes directly
   - **0.50-0.69** → Medium confidence, routes with caution
   - **< 0.50** → Low confidence, asks for clarification

---

## Troubleshooting

### Issue: Brain MRI still routed to X-ray agent

**Possible causes:**
1. Image is not square (check aspect ratio in logs)
2. Image is very bright (check gray_mean > 80)
3. Image has high contrast (check std values)

**Solution:**
- Check terminal logs for scores
- If Brain MRI score < X-ray score, the image characteristics may be unusual
- Use clarification by saying "It's a brain MRI"

### Issue: System doesn't ask for clarification

**Possible causes:**
1. Confidence is ≥ 0.5 (system is confident enough)
2. One score is clearly dominant

**Solution:**
- Check confidence value in logs
- If you disagree with classification, explicitly mention image type in query
- Example: "This is a brain MRI, please analyze it"

### Issue: System asks for clarification but doesn't understand

**Possible causes:**
1. User response doesn't contain the right keywords
2. Keywords: "brain", "mri", "chest", "x-ray", "skin", "lesion"

**Solution:**
- Use clear keywords: "It's a brain MRI" or "This is a chest X-ray"
- Be explicit: "Brain scan" or "Lung X-ray"

---

## Quick Reference - Clarification Keywords

**Brain MRI:**
- brain, mri, tumor, tumour, neurology, neurological, brain scan, head scan

**Chest X-ray:**
- chest, x-ray, xray, lung, pneumonia, covid, pulmonary, respiratory, chest scan

**Skin Lesion:**
- skin, lesion, mole, rash, dermatology, benign, malignant, cancer, melanoma

---

## Success Criteria

✅ **Q1 Fixed:** Brain MRI images route to BRAIN_TUMOR_AGENT (not X-ray)  
✅ **Q2 Fixed:** Ambiguous images trigger clarification prompt  
✅ **Bonus:** All three image types route correctly with high confidence  
✅ **Bonus:** Comprehensive logging for debugging  

---

## Need Help?

Check the logs in terminal for detailed scoring breakdown:
- Skin lesion score
- Brain MRI score
- X-ray score
- Final classification
- Confidence level
- Routing decision

If routing is still incorrect, check `ROUTING_FIXES_COMPLETE.md` and `IMAGE_ROUTING_GUIDE.md` for more details.



