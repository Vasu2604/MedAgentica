# Testing Mayo Clinic-Style Prompts - Quick Guide

## 🎯 Purpose
Test all agents with the new Mayo Clinic Universal Clinical Consultation format to ensure:
- ✅ Structured 10-section output
- ✅ 150-200 word concise yet comprehensive responses
- ✅ Evidence citations with years
- ✅ Professional clinician tone
- ✅ Actionable clinical decisions

---

## 🧪 Test Protocol

### **1. Brain Tumor Agent Test**

**Upload:** `sample_images/brain_mri_sample.jpg` (or any brain MRI)  
**Query:** "What do you see in this brain MRI?"

**Expected Output Structure:**
```
1. ✅ Case Summary (1-2 sentences)
2. ✅ AI Classification Result (Glioma/Meningioma/Pituitary with %)
3. ✅ Red Flags & Immediate Actions (if mass effect present)
4. ✅ Assessment (most likely diagnosis with rationale)
5. ✅ Recommended Diagnostic Work-up (contrast MRI, labs, consults)
6. ✅ Management Considerations (dexamethasone, antiepileptics)
7. ✅ Disposition & Follow-up (admit vs outpatient, neurosurgery timing)
8. ✅ Patient Education (plain language explanation)
9. ✅ Coding & Documentation (ICD-10 codes)
10. ✅ Sources (NCCN 2024, WHO Classification 2021)
```

**Quality Checks:**
- [ ] Response 150-200 words
- [ ] Professional neuroradiology terminology
- [ ] Clear next steps (imaging, consults)
- [ ] Patient education in plain language
- [ ] ICD-10 codes included
- [ ] Guidelines cited with year

---

### **2. Chest X-ray Agent Test**

**Upload:** `sample_images/chest_x-ray_covid_and_normal/chest_xray.jpg`  
**Query:** "Can you analyze this chest X-ray for pneumonia?"

**Expected Output Structure:**
```
1. ✅ Case Summary
2. ✅ Primary Radiographic Finding (consolidation, opacity with %)
3. ✅ Red Flags & Immediate Actions (pneumothorax, massive effusion)
4. ✅ Differential Diagnosis (CAP, viral, aspiration)
5. ✅ Assessment (leading diagnosis with rationale)
6. ✅ Recommended Diagnostic Work-up (CBC, CRP, cultures, COVID PCR)
7. ✅ Management Plan:
   - Non-pharm: O₂, hydration, incentive spirometry
   - Pharm: Amoxicillin-clavulanate 875mg BID x 5-7d with alternatives
8. ✅ Disposition & Follow-up (CURB-65 score, admit criteria, return precautions)
9. ✅ Patient Education (plain language - what pneumonia is, med instructions)
10. ✅ Coding & Documentation (ICD-10, CURB-65 score)
11. ✅ Sources (IDSA 2023, ATS 2024)
```

**Quality Checks:**
- [ ] Response 150-200 words
- [ ] COVID-19 probability mentioned
- [ ] Pathologies with percentages
- [ ] Antibiotic doses specified (mg, frequency, duration)
- [ ] CURB-65 or NEWS2 mentioned
- [ ] Follow-up timing (48-72hr, 6-week CXR)
- [ ] Return precautions clear
- [ ] Guidelines cited (IDSA/ATS with year)

---

### **3. Skin Lesion Agent Test**

**Upload:** `sample_images/skin_lesion_images/melanoma_sample.jpg`  
**Query:** "Is this mole concerning?"

**Expected Output Structure:**
```
1. ✅ Case Summary
2. ✅ AI Classification Result (benign vs malignant %)
3. ✅ Red Flags & Immediate Actions (melanoma suspicion → biopsy 1-2 weeks)
4. ✅ Assessment (leading diagnosis with ABCDE criteria if relevant)
5. ✅ Differential Diagnosis (melanoma vs dysplastic nevus vs seborrheic keratosis)
6. ✅ Recommended Diagnostic Work-up (biopsy type: shave/punch/excisional)
7. ✅ Management Plan:
   - If benign: observation, photo-monitoring
   - If malignant: biopsy urgency, staging, oncology referral
   - Sun protection counseling (SPF 30+)
8. ✅ Disposition & Follow-up (biopsy timing, follow-up intervals)
9. ✅ Patient Education (ABCDE criteria, self-monitoring, sun safety)
10. ✅ Coding & Documentation (ICD-10, CPT for biopsy)
11. ✅ Sources (AAD guidelines, NCCN melanoma guidelines year)
```

**Quality Checks:**
- [ ] Response 150-200 words
- [ ] Benign vs malignant % stated
- [ ] ABCDE criteria mentioned (if relevant)
- [ ] Biopsy type specified (shave/punch/excisional)
- [ ] Biopsy urgency timeline (1-2 weeks if concerning)
- [ ] Sun protection guidance (SPF 30+)
- [ ] Self-monitoring instructions
- [ ] ICD-10 and CPT codes
- [ ] AAD/NCCN citations with year

---

### **4. Conversation Agent Test (Medical Question)**

**Query:** "What causes persistent headaches?"

**Expected Output Structure:**
```
1. ✅ Brief Answer (1-2 sentences direct response)
2. ✅ Key Points (2-4 bullets):
   - Tension-type headaches
   - Migraines
   - Secondary causes (HTN, infection, mass)
3. ✅ Red Flags (thunderclap, neuro deficits → ER)
4. ✅ Next Steps (track triggers, hydration, when to see provider)
5. ✅ Patient Education (plain language)
6. ✅ Source (ICHD-3, AAN guidelines 2024)
```

**Quality Checks:**
- [ ] Response 100-150 words
- [ ] Direct answer to question
- [ ] 2-4 key points (differential considerations)
- [ ] Red flags clearly stated
- [ ] Next steps actionable
- [ ] Evidence citation with year (ICHD-3, AAN 2024)
- [ ] Evidence quality noted (strong/moderate/low)

---

### **5. Conversation Agent Test (Casual Query)**

**Query:** "Hi there"

**Expected Output:**
```
"Hello! I'm here to help with your medical questions. What can I assist you with today?"
```

**Quality Checks:**
- [ ] Response ≤30 words
- [ ] Friendly, professional tone
- [ ] No unnecessary information
- [ ] Invites next question

---

### **6. Emergency Detection Test**

**Query:** "I have severe chest pain and can't breathe"

**Expected Output:**
```
⚠️ MEDICAL EMERGENCY DETECTED

**Immediate Actions Required:**

1. **Call Emergency Services (911) NOW** if experiencing:
   - Chest pain / heart attack symptoms
   - Stroke symptoms (FAST: Face droop, Arm weakness, Speech difficulty, Time = critical)
   - Severe bleeding or trauma
   - Difficulty breathing / not breathing
   ...

2. **While Waiting for EMS:**
   - Stay calm, remain still
   - Don't drive yourself
   - Have someone stay with you
   - Follow 911 operator instructions

3. **Critical Information for EMS:**
   - Current medications
   - Allergies
   - When symptoms started
   - Pre-existing conditions

**This is NOT a substitute for emergency medical care.**
**If life-threatening: CALL 911 IMMEDIATELY.**
```

**Quality Checks:**
- [ ] Emergency detected instantly
- [ ] "CALL 911 NOW" prominent
- [ ] FAST protocol mentioned (for stroke)
- [ ] Clear action items (don't drive, stay calm)
- [ ] Critical info for EMS listed
- [ ] No lengthy disclaimers
- [ ] Structured, scannable format

---

### **7. Image Persistence Test**

**Step 1:** Upload chest X-ray  
**Step 2:** Query: "What did you find?"

**Expected:**
- ✅ System retrieves stored image from session
- ✅ Routes to Chest X-ray agent
- ✅ Returns Mayo Clinic format analysis

**Quality Checks:**
- [ ] Image recognized from previous upload
- [ ] No "please upload image" re-request
- [ ] Correct agent routing (chest X-ray)
- [ ] Mayo Clinic format response

---

## 📊 Overall Quality Metrics

### **All Responses Should Have:**

| Metric | Target | Check |
|--------|--------|-------|
| **Word Count** | 150-200 (medical), 30 (casual) | [ ] |
| **Structure** | Numbered sections | [ ] |
| **Tone** | Professional clinician-to-clinician | [ ] |
| **Evidence** | Guidelines cited with year | [ ] |
| **Actionable** | Clear next steps | [ ] |
| **Patient Education** | Plain language section (6th-8th grade) | [ ] |
| **Red Flags** | Safety concerns prominent | [ ] |
| **Codes** | ICD-10 included for diagnoses | [ ] |
| **No Fluff** | No greetings, verbose disclaimers | [ ] |
| **Scannable** | Bullets, numbered lists, bold headers | [ ] |

---

## 🚀 Running Tests

### **Option 1: Web Interface**

```bash
# Start server
cd /Users/vasupatel/Desktop/MedAgentica/Multi-Agent-Medical-Assistant
./run_server.sh

# Open browser
open http://localhost:8000

# Upload images and enter queries as outlined above
# Check responses against expected structure
```

### **Option 2: Python Script**

```python
import requests

# Test Brain Tumor Agent
files = {'image': open('sample_images/brain_mri.jpg', 'rb')}
response = requests.post('http://localhost:8000/upload', files=files)
session_id = response.cookies.get('session_id')

# Query
query_response = requests.post(
    'http://localhost:8000/chat',
    json={"query": "What do you see in this brain MRI?"},
    cookies={'session_id': session_id}
)
print(query_response.json()['response'])

# Validate Mayo Clinic format
from agents.clinical_prompts import validate_clinical_prompt
quality = validate_clinical_prompt(query_response.json()['response'])
print(f"Quality Score: {quality['quality_score']}")
```

---

## ✅ Success Criteria

**Test PASSES if:**

1. ✅ **All agents** return Mayo Clinic structured format (10 sections)
2. ✅ **Word count** within 150-200 for medical, 30 for casual
3. ✅ **Evidence citations** present with years (NCCN 2024, IDSA 2023, etc.)
4. ✅ **Professional tone** - clinician-to-clinician language
5. ✅ **Actionable items** - clear next steps (labs, imaging, meds with doses)
6. ✅ **Patient education** - plain language sections present
7. ✅ **Red flags** - safety concerns prominently featured
8. ✅ **ICD-10 codes** - included for all diagnoses
9. ✅ **No chain-of-thought** - concise rationales only
10. ✅ **Emergency detection** - instant routing with clear call 911 message

---

## 🐛 Common Issues & Fixes

| Issue | Likely Cause | Fix |
|-------|--------------|-----|
| Response too verbose (>250 words) | LLM not following length constraint | Check prompt includes "Maximum 150-200 words" |
| No evidence citations | Prompt missing source requirement | Verify `Sources (cite guidelines with year)` in prompt |
| Patient-friendly language in clinical section | Tone instruction unclear | Ensure prompt specifies "clinician-to-clinician" |
| Missing ICD-10 codes | Coding section not in prompt | Add "Coding & Documentation" section to prompt |
| No red flags for concerning findings | Safety-netting not emphasized | Add "Red Flags & Immediate Actions" as section 3 |
| Casual tone for medical questions | Wrong prompt selected | Verify `CONVERSATION_CLINICAL_PROMPT` is used, not base prompt |

---

## 📈 Results Tracking

**After testing, document:**

| Agent | Structure ✅ | Length ✅ | Evidence ✅ | Professional ✅ | Actionable ✅ | Pass/Fail |
|-------|-------------|----------|-------------|----------------|--------------|-----------|
| Brain Tumor | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Chest X-ray | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Skin Lesion | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Conversation (Med) | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Conversation (Casual) | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Emergency | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Image Persistence | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |

---

## 🎯 Next Steps After Testing

**If all tests PASS:**
- ✅ Document results in `TEST_RESULTS.md`
- ✅ Mark TODO item #7 as completed
- ✅ Ready for production deployment

**If any tests FAIL:**
1. Review `agents/clinical_prompts.py` for the specific agent
2. Check prompt formatting and structure
3. Verify LLM is receiving complete system prompt
4. Re-test with adjustments

---

**Happy Testing! 🧪**

**Expected Outcome:** All agents return professional, evidence-based, Mayo Clinic-style clinical consultations! 🏥✨

