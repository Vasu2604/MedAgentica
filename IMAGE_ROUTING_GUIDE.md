# Image Routing Guide

## How Image Classification Works

The Multi-Agent Medical Assistant uses a sophisticated **heuristic-based image classification** system to automatically detect the type of medical image uploaded and route it to the appropriate specialist agent.

---

## Three Types of Medical Images Supported

### 1. **Skin Lesion** 🩹
- **Agent**: SKIN_LESION_AGENT
- **Model**: EfficientNet-B0 (Benign/Malignant classification)
- **Characteristics**:
  - Colorful (warm tones: red, brown, pink)
  - High saturation
  - Color variation
  - Organic shapes

### 2. **Brain MRI** 🧠
- **Agent**: BRAIN_TUMOR_AGENT
- **Model**: BrainMRI-Tumor-Classifier-Pytorch (5-class classification)
- **Characteristics**:
  - Grayscale medical image
  - **Square aspect ratio** (1:1 or close)
  - Darker overall intensity (gray_mean < 80)
  - Low contrast (uniform appearance)
  - Pure grayscale (no color tint)

### 3. **Chest X-ray** 🫁
- **Agent**: CHEST_XRAY_AGENT
- **Model**: MedRAX (18-disease classification)
- **Characteristics**:
  - Grayscale medical image
  - **Rectangular aspect ratio** (taller than wide)
  - Brighter intensity (gray_mean 80-220)
  - Higher contrast (bones vs soft tissue)
  - Pure grayscale

---

## How Classification Works

### Step 1: Image Analysis
When you upload an image, the system analyzes:
- Aspect ratio (width / height)
- Color properties (BGR channels, HSV)
- Grayscale intensity
- Saturation levels
- Contrast and variance

### Step 2: Scoring System
Each image type gets a score based on its characteristics:

```python
# Brain MRI Score (max 11 points):
- Square aspect (0.9 < ratio < 1.1): +3 points ⭐⭐⭐
- Grayscale-like: +2 points
- Darker intensity (< 80): +2 points
- Very grayscale (BGR diff < 5): +2 points
- Low saturation: +1 point
- Low contrast: +1 point

# Chest X-ray Score (max 12 points):
- X-ray intensity (80-220): +3 points ⭐⭐⭐
- Grayscale-like: +2 points
- Rectangular aspect: +2 points
- High contrast: +2 points
- Low saturation: +2 points
- BGR diff < 10: +1 point

# Skin Lesion Score (max 9 points):
- High saturation (> 40): +2 points
- Warm tones (red dominant): +2 points
- Not grayscale: +2 points
- Color variation: +1 point
- Red channel > 100: +1 point
```

### Step 3: Decision Logic (11 Tiers)
The system uses a **priority-based decision tree**:

1. **Strong Skin Lesion** (score ≥ 4) → 85% confidence
2. **Moderate Skin Lesion** (score ≥ 3) → 70% confidence
3. **Strong Brain MRI** (score ≥ 6) → 85% confidence
4. **Moderate Brain MRI** (score ≥ 4 + square) → 70% confidence
5. **Strong Chest X-ray** (score ≥ 7) → 90% confidence
6. **Moderate Chest X-ray** (score ≥ 5 + not square) → 75% confidence
7. **Weak Brain MRI** (score ≥ 3 + square) → 60% confidence
8. **Weak Skin Lesion** (score ≥ 2) → 60% confidence
9. **Colorful non-X-ray** → Skin Lesion, 55% confidence
10. **Ambiguous Grayscale** → 45% confidence (triggers clarification)
11. **Truly Ambiguous** → unknown, 30% confidence (triggers clarification)

### Step 4: Routing
- **High confidence (≥ 0.5)**: Routes directly to the appropriate agent
- **Low confidence (< 0.5)**: Routes to CONVERSATION_AGENT for clarification

---

## Clarification Flow (Q2 Implementation)

When the system **cannot confidently determine** the image type, it asks the user for help:

### Trigger Conditions:
- Image type = "unknown"
- Confidence < 0.5
- Ambiguous grayscale image

### Example Flow:

#### 1. User Uploads Ambiguous Image
```
[User uploads brain_scan.jpg]
System: Analyzing image... confidence: 0.45
```

#### 2. System Asks for Clarification
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

#### 3. User Clarifies
```
User: "It's a brain MRI"
```

#### 4. System Routes to Correct Agent
```
System detects "brain" keyword
→ Updates state: image_type = "BRAIN MRI"
→ Routes to BRAIN_TUMOR_AGENT
→ Analysis proceeds
```

### Clarification Keywords:

**Skin Lesion Keywords:**
- skin, lesion, mole, rash, dermatology, dermatologist
- benign, malignant, cancer, melanoma

**Chest X-ray Keywords:**
- chest, x-ray, xray, lung, pneumonia, covid
- pulmonary, respiratory

**Brain MRI Keywords:**
- brain, mri, tumor, tumour, neurology, neurological

---

## Key Differences Between Brain MRI and Chest X-ray

Since both are grayscale medical images, the system uses these **distinguishing features**:

| Feature | Brain MRI | Chest X-ray |
|---------|-----------|-------------|
| **Aspect Ratio** | Square (1:1) ⭐ | Rectangular (taller) ⭐ |
| **Intensity** | Darker (< 80) ⭐ | Brighter (80-220) ⭐ |
| **Contrast** | Low (uniform) | High (bones vs tissue) |
| **Typical Size** | 256x256, 512x512 | 512x683, 768x1024 |
| **Appearance** | Darker, smoother | Brighter, more texture |

⭐ = **Strong indicators** used by the classifier

---

## Testing Your Images

### Expected Behavior:

#### **Brain MRI** (should route to BRAIN_TUMOR_AGENT)
```
Example: brain_mri_sample.jpg (512x512, grayscale, dark)

Expected output:
🔍 ANALYZED IMAGE TYPE: BRAIN MRI (confidence: 0.75)
   Reasoning: Square grayscale medical image, likely brain MRI
   (score: 7 vs X-ray: 4)
```

#### **Chest X-ray** (should route to CHEST_XRAY_AGENT)
```
Example: chest_xray_sample.jpg (768x1024, grayscale, bright)

Expected output:
🔍 ANALYZED IMAGE TYPE: CHEST X-RAY (confidence: 0.85)
   Reasoning: Rectangular grayscale image with X-ray intensity
   (score: 9)
```

#### **Skin Lesion** (should route to SKIN_LESION_AGENT)
```
Example: skin_lesion_sample.jpg (640x480, colorful, warm tones)

Expected output:
🔍 ANALYZED IMAGE TYPE: SKIN LESION (confidence: 0.80)
   Reasoning: Colorful image with warm tones (score: 7),
   likely skin lesion
```

#### **Ambiguous Image** (should ask for clarification)
```
Example: unclear_scan.jpg (confidence: 0.42)

Expected output:
🔍 ANALYZED IMAGE TYPE: BRAIN MRI (confidence: 0.45)
❓ Unknown/ambiguous image type (BRAIN MRI, confidence: 0.45)
   - Routing to CONVERSATION_AGENT for clarification