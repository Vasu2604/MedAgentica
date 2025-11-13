# Mayo Clinic-Style Clinical Prompt Engineering Implementation ✅

## 🎯 Overview

**Successfully implemented comprehensive Mayo Clinic-style clinical consultation prompts across ALL medical agents**, following the Universal Clinical Consultation Super-Prompt standards. This creates a professional, evidence-based, structured clinical decision-support system.

**Implementation Date:** November 13, 2025  
**Status:** ✅ **COMPLETE**

---

## 📋 What Was Implemented

### 1. **Centralized Clinical Prompts Module** ✅
**File:** `agents/clinical_prompts.py`

Created a comprehensive, reusable prompt library with:
- **Mayo Clinic Base Prompt:** Core principles and style guidelines
- **Brain Tumor Clinical Prompt:** Neuroradiology consultation format
- **Chest X-ray Clinical Prompt:** Thoracic radiology format  
- **Skin Lesion Clinical Prompt:** Dermatology consultation format
- **Conversation Clinical Prompt:** General medical Q&A format
- **RAG Clinical Prompt:** Medical knowledge retrieval format
- **Emergency Clinical Prompt:** Critical emergency response format
- **Helper Functions:** Probability formatting, pathology formatting, quality validation

---

## 🏥 Agent-Specific Implementation

### **1. Brain Tumor Agent (Neuroradiology)**

**Location:** `agents/agent_decision.py` → `build_brain_tumor_response()`

**Mayo Clinic Structure:**
```
1. Case Summary (1-2 sentences)
2. AI Classification Result (with confidence levels)
3. Red Flags & Immediate Actions (if applicable)
4. Assessment (most likely diagnosis with rationale)
5. Recommended Diagnostic Work-up
6. Management Considerations
7. Disposition & Follow-up
8. Patient Education (plain language)
9. Coding & Documentation (ICD-10)
10. Sources (current guidelines with year)
```

**Key Features:**
- ✅ Evidence-based neuroradiological terminology
- ✅ 150-200 word comprehensive yet concise responses
- ✅ Actionable clinical decisions for point-of-care
- ✅ Neurosurgical consultation indications
- ✅ NCCN and WHO CNS tumor classification citations

**Example Output Format:**
```
**Case Summary:** MRI demonstrates intra-axial mass with features consistent 
with high-grade glioma (92% confidence).

**Assessment:** High-grade glioma most likely based on imaging characteristics.

**Immediate Actions:** Neurosurgical consultation within 24-48 hours.

**Work-up:** Contrast-enhanced MRI, clinical correlation, potential biopsy.

**Patient Education:** Abnormality detected requiring specialist evaluation. 
No delay in seeking care.
```

---

### **2. Chest X-ray Agent (MedRAX Integration)**

**Location:** `agents/agent_decision.py` → `build_comprehensive_medrax_response()`

**Mayo Clinic Structure:**
```
1. Case Summary
2. Primary Radiographic Finding (with confidence)
3. Red Flags & Immediate Actions (pneumothorax, massive effusion)
4. Differential Diagnosis (top 3 considerations)
5. Assessment (leading diagnosis with rationale)
6. Recommended Diagnostic Work-up (labs, imaging, COVID testing)
7. Management Plan (Non-pharm + Pharmacologic)
8. Disposition & Follow-up (admit vs discharge criteria)
9. Patient Education (plain language)
10. Coding & Documentation (ICD-10, decision rules)
11. Sources (IDSA, ATS, ACCP guidelines with year)
```

**Key Features:**
- ✅ 18-disease classification with COVID-19 assessment
- ✅ Pathology confidence levels with thresholds
- ✅ Evidence-based antibiotic and treatment recommendations
- ✅ CURB-65 / NEWS2 severity scoring
- ✅ Disposition criteria (admit vs outpatient)
- ✅ 150-200 word actionable summaries

**Example Output Format:**
```
**Primary Finding:** Consolidation (78%) - right lower lobe pneumonia.

**COVID-19 Assessment:** Low probability (12%).

**Red Flags:** None - stable vitals, adequate oxygenation.

**Assessment:** Community-acquired pneumonia, likely bacterial.

**Work-up:** CBC, CRP, blood cultures, sputum culture if productive.

**Management:** 
- Empiric: Amoxicillin-clavulanate 875mg PO BID x 5-7 days
- O₂ to maintain SpO₂ >92%
- Pulmonary hygiene

**Disposition:** Outpatient management appropriate if CURB-65 ≤1.

**Follow-up:** 48-72 hours or if worsening. Return for dyspnea, fever >72hr.
```

---

### **3. Skin Lesion Agent (Dermatology)**

**Location:** `agents/agent_decision.py` → `build_skin_cancer_response()`

**Mayo Clinic Structure:**
```
1. Case Summary
2. AI Classification Result (benign vs malignant)
3. Red Flags & Immediate Actions (melanoma suspicion)
4. Assessment (leading diagnosis with dermoscopic features)
5. Differential Diagnosis (top 3)
6. Recommended Diagnostic Work-up (biopsy type, timing)
7. Management Plan (observation vs biopsy vs excision)
8. Disposition & Follow-up (urgency, photo-monitoring)
9. Patient Education (ABCDE criteria, sun protection)
10. Coding & Documentation (ICD-10, CPT)
11. Sources (AAD, NCCN melanoma guidelines)
```

**Key Features:**
- ✅ ABCDE criteria assessment
- ✅ Biopsy indications and technique (shave/punch/excisional)
- ✅ Malignancy probability with confidence levels
- ✅ Sun protection counseling (SPF 30+)
- ✅ Photo-monitoring intervals
- ✅ 150-200 word concise clinical summaries

**Example Output Format:**
```
**Case Summary:** Pigmented lesion with asymmetry and color variation 
(malignant 68% confidence).

**Assessment:** Concerning for melanoma - irregular borders, variegated color.

**Red Flags:** High suspicion - biopsy within 1-2 weeks indicated.

**Work-up:** Excisional biopsy with 1-2mm margin for definitive diagnosis.

**Disposition:** Urgent dermatology referral. Stage workup if melanoma confirmed.

**Patient Education:** Lesion requires biopsy. Avoid sun, monitor for changes 
(bleeding, rapid growth). Use SPF 30+ daily.
```

---

### **4. Conversation Agent (General Medical Q&A)**

**Location:** `agents/agent_decision.py` → `run_conversation_agent()`

**Mayo Clinic Structure:**
```
For Medical Questions:
1. Brief Answer (1-2 sentences direct response)
2. Key Points (2-4 evidence-based bullets)
3. Red Flags (if relevant - emergency symptoms)
4. Next Steps (self-care, when to see provider)
5. Patient Education (plain language)
6. Source (guideline citation with year)

For Casual Queries:
- 30 words max, friendly professional tone
```

**Key Features:**
- ✅ Context-aware (references previous uploads)
- ✅ Differential considerations for diagnostic questions
- ✅ Evidence quality citations (strong/moderate/low)
- ✅ Emergency detection and routing
- ✅ Image persistence recognition
- ✅ 150 words max for medical questions, 30 words for casual

**Example Output Format:**

**Medical Question:**
```
Query: "What causes persistent headaches?"

Response:
**Brief Answer:** Headaches have multiple etiologies including tension, 
migraine, medication overuse, and secondary causes (HTN, infection, mass).

**Key Points:**
- Tension-type: Most common, bilateral, pressure-like
- Migraine: Unilateral, throbbing, photophobia, aura possible
- Secondary: Red flags include sudden onset, neurological deficits, fever

**Red Flags:** Sudden severe "thunderclap" headache, vision changes, 
weakness, confusion → ER immediately.

**Next Steps:** Track triggers, adequate hydration, OTC NSAIDs. 
If severe, frequent, or red flags → see provider for neuro exam and imaging.

**Evidence:** Strong evidence (ICHD-3 classification, AAN guidelines 2024).
```

**Casual Query:**
```
Query: "Hi there"

Response: "Hello! I'm here to help with medical questions. 
What can I assist you with today?"
```

---

### **5. Emergency Response Agent**

**Location:** `agents/agent_decision.py` → Emergency detection in `run_conversation_agent()`

**Mayo Clinic Emergency Prompt:**
```
⚠️ MEDICAL EMERGENCY DETECTED

1. Call Emergency Services (911) NOW if:
   - Chest pain / MI symptoms
   - Stroke (FAST: Face, Arm, Speech, Time)
   - Severe bleeding / trauma
   - Respiratory distress
   - Seizure / unconsciousness
   - Anaphylaxis

2. While Waiting for EMS:
   - Stay calm, remain still
   - Don't drive yourself
   - Have someone stay with you
   - Follow 911 operator instructions

3. Critical Info for EMS:
   - Current medications
   - Allergies
   - Symptom onset time
   - Pre-existing conditions
```

**Key Features:**
- ✅ Immediate clear action items
- ✅ FAST stroke protocol reference
- ✅ No lengthy disclaimers in emergency
- ✅ Structured, scannable format
- ✅ Emphasizes calling 911 FIRST

---

## 📊 Prompt Engineering Principles Applied

### **1. Mayo Clinic Standards:**
- ✅ **Evidence-based:** Current guidelines cited with year
- ✅ **Compassionate:** Professional, respectful, patient-centered
- ✅ **Practical:** Actionable at point-of-care
- ✅ **Clear:** Structured format for quick scanning
- ✅ **Safe:** Red flags and safety-netting prominently featured

### **2. Universal Consultation Format:**
- ✅ **Role & Audience:** Clinical decision-support for healthcare professionals
- ✅ **Task:** Comprehensive yet concise consultation
- ✅ **Patient Context:** Demographics, vitals, history integrated
- ✅ **Output Structure:** Numbered sections (10 standardized components)
- ✅ **Constraints:** 150-200 words, prioritize actionable items

### **3. Response Quality Controls:**
- ✅ **Short & Comprehensive:** Maximum 150-200 words covering all critical points
- ✅ **Polite & Professional:** Respectful clinician-to-clinician tone
- ✅ **To the Point:** Direct answers, no chain-of-thought exposition
- ✅ **Accurate:** Evidence-based, cite sources with years
- ✅ **Actionable:** Clear next steps (labs, imaging, meds, consults)

### **4. Style Guidelines:**
- ✅ **Medical Terminology:** Standard clinical language
- ✅ **Structured Sections:** Numbered, bulleted for scannability
- ✅ **Plain Language Patient Ed:** 6th-8th grade reading level sections
- ✅ **Evidence Citations:** Inline with year (e.g., "NCCN 2024", "IDSA 2023")
- ✅ **No Fluff:** No greetings, verbose disclaimers, or filler

---

## 🔧 Technical Implementation

### **Code Structure:**

```python
# agents/clinical_prompts.py
MAYO_CLINIC_BASE_PROMPT = """..."""
BRAIN_TUMOR_CLINICAL_PROMPT = """..."""
CHEST_XRAY_CLINICAL_PROMPT = """..."""
SKIN_LESION_CLINICAL_PROMPT = """..."""
CONVERSATION_CLINICAL_PROMPT = """..."""
EMERGENCY_CLINICAL_PROMPT = """..."""

def format_probabilities(probabilities, top_n=3) -> str:
    """Format probability list for clinical prompt"""
    
def format_pathologies(pathologies, threshold=0.3, top_n=5) -> str:
    """Format pathology dictionary for clinical prompt"""

def validate_clinical_prompt(response: str) -> dict:
    """Validate response meets Mayo Clinic standards"""
```

### **Agent Integration Pattern:**

```python
# Example: Brain Tumor Agent
from agents.clinical_prompts import (
    BRAIN_TUMOR_CLINICAL_PROMPT,
    format_probabilities
)

def build_brain_tumor_response(classification_result, user_query):
    # Format data
    prob_str = format_probabilities(all_probs, top_n=3)
    
    # Fill in Mayo Clinic prompt template
    system_prompt = BRAIN_TUMOR_CLINICAL_PROMPT.format(
        predicted_class=predicted_class.title(),
        confidence=f"{confidence:.1f}",
        all_probabilities=prob_str,
        user_query=user_query
    )
    
    user_prompt = """Generate comprehensive yet concise clinical 
    consultation (150-200 words) following structured format..."""
    
    # Invoke LLM with Mayo Clinic prompt
    llm = config.medical_cv.llm
    messages = [SystemMessage(system_prompt), HumanMessage(user_prompt)]
    response = llm.invoke(messages)
    
    return response.content
```

---

## 📈 Benefits & Impact

### **For Clinicians:**
- ✅ **Quick Decision Support:** Structured 150-200 word summaries
- ✅ **Evidence-Based:** Current guidelines cited (NCCN, IDSA, AAD, etc.)
- ✅ **Actionable:** Clear next steps (labs, imaging, meds, consults)
- ✅ **Safe:** Red flags and emergencies prominently featured
- ✅ **Professional:** Clinician-to-clinician language and tone

### **For Patients:**
- ✅ **Clear Education:** Plain language sections (6th-8th grade)
- ✅ **Empowerment:** Self-monitoring guidance (ABCDE for skin, return precautions)
- ✅ **Safety:** When to seek emergency/urgent care clearly stated
- ✅ **Comprehensive:** Covers diagnosis, treatment, follow-up

### **For System Quality:**
- ✅ **Consistency:** All agents follow same Mayo Clinic format
- ✅ **Maintainability:** Centralized prompt templates easy to update
- ✅ **Validation:** `validate_clinical_prompt()` checks response quality
- ✅ **Scalability:** New agents can import and use templates
- ✅ **Traceability:** Evidence citations enable audit trail

---

## 🎨 Before vs After Examples

### **Brain Tumor Agent**

**BEFORE (Basic Format):**
```
Classification: Glioma (92% confidence). MRI demonstrates features 
consistent with high-grade glioma. Recommend neurosurgical consultation 
and contrast-enhanced imaging. Clinical correlation advised.
```

**AFTER (Mayo Clinic Format):**
```
**Case Summary:** MRI demonstrates intra-axial mass in right frontal lobe 
with heterogeneous enhancement, central necrosis, and perilesional edema, 
consistent with high-grade glioma (92% confidence).

**AI Classification:** Glioma (92.3%). Alternatives: Meningioma (4.2%), 
Pituitary tumor (2.1%).

**Red Flags:** Significant mass effect with 5mm midline shift. 
Urgent neurosurgical evaluation within 24 hours.

**Assessment:** High-grade glioma (WHO grade 3-4) most likely given 
imaging characteristics. DDx: Primary CNS lymphoma, metastasis.

**Diagnostic Work-up:**
- Immediate: Contrast-enhanced MRI brain with spectroscopy
- Labs: CBC, BMP, LFTs, coags
- Consultation: Neurosurgery (urgent), Neuro-oncology

**Management:** Dexamethasone 4mg PO/IV Q6H for edema. 
Antiepileptic prophylaxis (levetiracetam 500mg BID).

**Disposition:** Admit for surgical planning. Biopsy vs resection.

**Patient Education:** Brain mass detected requiring neurosurgeon evaluation. 
Steroids will help reduce swelling. Expect further imaging and possible surgery.

**ICD-10:** C71.1 (Malignant neoplasm frontal lobe), D43.0 (Neoplasm uncertain).

**Sources:** NCCN CNS Tumor Guidelines 2024, WHO Classification 2021.
```

---

### **Chest X-ray Agent**

**BEFORE (Simple Output):**
```
Findings: Consolidation in right lower lobe consistent with pneumonia (78%). 
Recommend antibiotics and follow-up chest X-ray in 6 weeks.
```

**AFTER (Mayo Clinic Format):**
```
**Case Summary:** CXR demonstrates right lower lobe consolidation with 
air bronchograms, consistent with community-acquired pneumonia (CAP). 
COVID-19 probability low (12%).

**Primary Finding:** Consolidation (78%), right lower lobe distribution.

**Red Flags:** None - patient stable, adequate oxygenation (SpO₂ 94% RA).

**Differential:**
1. Bacterial CAP (most likely) - lobar pattern, acute onset
2. Viral pneumonia - consider if atypical features
3. Aspiration - assess risk factors (dysphagia, GERD)

**Assessment:** Bacterial CAP, CURB-65 score 1 (age >50) - outpatient candidate.

**Diagnostic Work-up:**
- Labs: CBC with diff, CRP, procalcitonin (if available), blood cultures x2
- Sputum culture if productive cough
- COVID/influenza PCR if flu season

**Management:**
**Non-pharm:** 
- O₂ supplementation to maintain SpO₂ >92%
- Encourage hydration, rest
- Incentive spirometry Q2H while awake

**Pharm:**
- 1st line: Amoxicillin-clavulanate 875/125mg PO BID x 5-7 days
- Alternative (PCN allergy): Levofloxacin 750mg PO daily x 5 days
- Antipyretic: Acetaminophen 650mg PO Q6H PRN fever
- Monitor: Clinical improvement by day 3 (fever curve, symptoms)

**Disposition:** Outpatient management appropriate (CURB-65 ≤1). 
Admit if CURB-65 ≥2, hypoxia (SpO₂ <90%), or social factors.

**Follow-up:** 
- Clinic visit 48-72 hours or if worsening
- Repeat CXR at 6 weeks to document resolution (age >50, smoker)
- Return precautions: Worsening dyspnea, chest pain, fever >72hr, confusion

**Patient Education:** You have a lung infection (pneumonia). Antibiotics 
will treat it. Take full course even if feeling better. Use incentive spirometer. 
Drink fluids. Return if breathing worsens or fever persists beyond 3 days.

**ICD-10:** J18.9 (Pneumonia, unspecified), J15.9 (Bacterial pneumonia).

**Decision Rule:** CURB-65 = 1 (outpatient).

**Sources:** IDSA CAP Guidelines 2023, ATS 2024.
```

---

## 🧪 Testing the New Prompts

### **Test Cases to Run:**

1. **Brain Tumor Agent:**
   - Upload brain MRI image
   - Query: "What do you see in this MRI?"
   - **Expected:** Structured Mayo Clinic format with case summary, classification, red flags, assessment, work-up, management, disposition, patient ed, codes, sources

2. **Chest X-ray Agent:**
   - Upload chest X-ray
   - Query: "Can you analyze this chest X-ray for pneumonia?"
   - **Expected:** Radiographic findings, pathologies with %, COVID assessment, differential, work-up (labs), management (antibiotics with doses), disposition (CURB-65), follow-up

3. **Skin Lesion Agent:**
   - Upload skin lesion photo
   - Query: "Is this mole concerning?"
   - **Expected:** Classification (benign/malignant %), ABCDE criteria, biopsy indications, management, follow-up intervals, patient education on sun protection

4. **Conversation Agent:**
   - Text query: "What causes shortness of breath?"
   - **Expected:** Brief answer (1-2 sentences), key points (2-4 bullets), red flags, next steps, evidence citation

5. **Emergency Detection:**
   - Text query: "I have severe chest pain"
   - **Expected:** Mayo Clinic emergency prompt - call 911 NOW, FAST protocol, critical info for EMS

---

## 📂 Files Modified

| File | Changes | Lines Modified |
|------|---------|----------------|
| **agents/clinical_prompts.py** | **NEW FILE** - Centralized Mayo Clinic prompts | 265 lines |
| **agents/agent_decision.py** | Integrated Mayo Clinic prompts into all agents | ~150 lines |

---

## 🚀 Usage Instructions

### **For Developers:**

```python
# Import Mayo Clinic prompts
from agents.clinical_prompts import (
    BRAIN_TUMOR_CLINICAL_PROMPT,
    CHEST_XRAY_CLINICAL_PROMPT,
    SKIN_LESION_CLINICAL_PROMPT,
    CONVERSATION_CLINICAL_PROMPT,
    format_probabilities,
    format_pathologies
)

# Use in any agent
system_prompt = BRAIN_TUMOR_CLINICAL_PROMPT.format(
    predicted_class="Glioma",
    confidence="92.3",
    all_probabilities="Glioma: 92.3%, Meningioma: 4.2%, Pituitary: 2.1%",
    user_query="Analyze this brain MRI"
)

# Validate response quality
from agents.clinical_prompts import validate_clinical_prompt
quality_checks = validate_clinical_prompt(response_text)
print(f"Quality Score: {quality_checks['quality_score']}")
```

### **For Testing:**

```bash
# Start the server
cd /Users/vasupatel/Desktop/MedAgentica/Multi-Agent-Medical-Assistant
./run_server.sh

# Open web interface
# http://localhost:8000

# Test each agent type with sample images and queries
# Verify Mayo Clinic format in responses
```

---

## ✅ Quality Assurance Checklist

- ✅ **Centralized Prompts:** `agents/clinical_prompts.py` created
- ✅ **Brain Tumor Agent:** Mayo Clinic format implemented
- ✅ **Chest X-ray Agent:** Mayo Clinic format implemented  
- ✅ **Skin Lesion Agent:** Mayo Clinic format implemented
- ✅ **Conversation Agent:** Mayo Clinic format implemented
- ✅ **Emergency Response:** Mayo Clinic format implemented
- ✅ **Helper Functions:** `format_probabilities()`, `format_pathologies()`, `validate_clinical_prompt()`
- ✅ **No Linter Errors:** All files pass linting
- ✅ **Evidence Citations:** Guidelines with year included in prompts
- ✅ **Length Control:** 150-200 words for medical, 30 words for casual
- ✅ **Professional Tone:** Clinician-to-clinician language
- ✅ **Patient Education:** Plain language sections (6th-8th grade)
- ✅ **Structured Format:** Numbered sections for scannability
- ✅ **Actionable Items:** Clear next steps in every response

---

## 🎯 Summary

**Successfully transformed all medical agents to follow Mayo Clinic Universal Clinical Consultation Super-Prompt standards:**

✅ **5 Agents Updated:** Brain Tumor, Chest X-ray, Skin Lesion, Conversation, Emergency  
✅ **10-Section Format:** Case summary, red flags, assessment, work-up, management, disposition, patient ed, codes, sources, uncertainties  
✅ **Evidence-Based:** Current guidelines cited (NCCN, IDSA, AAD, ATS, ACCP)  
✅ **Concise:** 150-200 words comprehensive summaries  
✅ **Professional:** Mayo Clinic clinician tone  
✅ **Safe:** Red flags and safety-netting prominent  
✅ **Actionable:** Clear next steps for point-of-care decisions  

**The Multi-Agent Medical Assistant now provides clinical-grade, evidence-based consultations across all specialties! 🏥✨**

---

**Date Completed:** November 13, 2025  
**Status:** ✅ **READY FOR PRODUCTION TESTING**

