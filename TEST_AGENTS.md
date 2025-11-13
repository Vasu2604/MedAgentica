# Comprehensive Agent Testing Guide

This guide provides test cases to verify that all agents in your Multi-Agent Medical Assistant are working correctly.

## 🧪 Test Cases for All Agents

### 1. **CONVERSATION_AGENT** - General Chat & Greetings
**Test Cases:**
- "Hello, how are you?"
- "What's your name?"
- "Tell me about yourself"
- "How can you help me?"
- "Thanks for your help!"

**Expected Behavior:** Should respond in a friendly, conversational manner without routing to medical agents.

### 2. **RAG_AGENT** - Medical Knowledge Queries
**Test Cases:**
- "What are the symptoms of diabetes?"
- "How does insulin work in the body?"
- "What is hypertension and how is it treated?"
- "Explain the causes of heart disease"
- "What are the risk factors for stroke?"

**Expected Behavior:** Should provide detailed medical information from the knowledge base with citations.

### 3. **WEB_SEARCH_PROCESSOR_AGENT** - Recent Medical News
**Test Cases:**
- "What's the latest news about COVID-19 vaccines?"
- "Are there any recent breakthroughs in cancer treatment?"
- "What are the current guidelines for managing diabetes?"
- "Tell me about recent medical research on Alzheimer's"

**Expected Behavior:** Should search for and summarize recent medical developments.

### 4. **CHEST_XRAY_AGENT** - COVID-19 Detection
**Test Cases (with chest X-ray image uploaded):**
- "Does this show COVID-19?"
- "Analyze this chest X-ray for abnormalities"
- "Is this a normal chest X-ray?"
- "Check if this X-ray shows pneumonia"

**Expected Behavior:** Should analyze the image and provide COVID-19 detection results.

### 5. **BRAIN_TUMOR_AGENT** - Brain MRI Analysis
**Test Cases (with brain MRI image uploaded):**
- "Does this MRI show a brain tumor?"
- "Analyze this brain scan for tumors"
- "Is there any abnormality in this MRI?"
- "Check this brain image for cancer"

**Expected Behavior:** Should analyze the MRI and provide tumor detection results.

### 6. **SKIN_LESION_AGENT** - Skin Lesion Classification
**Test Cases (with skin lesion image uploaded):**
- "Is this skin lesion malignant?"
- "Analyze this mole for cancer risk"
- "What type of skin lesion is this?"
- "Should I be concerned about this skin spot?"

**Expected Behavior:** Should analyze the skin lesion and provide classification results.

## 🚀 How to Test Each Agent

### **Step 1: Start the Application**
```bash
cd /Users/vasupatel/Desktop/MedAgentica/Multi-Agent-Medical-Assistant
python launch.py
```
Then open http://localhost:8000 in your browser.

### **Step 2: Test Conversation Agent**
1. Type: "Hello, how are you today?"
2. Expected: Friendly response from CONVERSATION_AGENT

### **Step 3: Test RAG Agent**
1. Type: "What are the symptoms of type 2 diabetes?"
2. Expected: Detailed medical information from RAG_AGENT

### **Step 4: Test Web Search Agent**
1. Type: "What's the latest news about COVID-19?"
2. Expected: Recent information from WEB_SEARCH_PROCESSOR_AGENT

### **Step 5: Test Image Analysis Agents**

#### **Chest X-ray Testing:**
1. Click the paperclip 📎 button
2. Upload a chest X-ray image (use sample images from `sample_images/chest_xray_covid_and_normal/`)
3. Type: "Does this show COVID-19?"
4. Expected: Analysis from CHEST_XRAY_AGENT with COVID detection results

#### **Brain MRI Testing:**
1. Click the paperclip 📎 button
2. Upload a brain MRI image (you may need to find sample brain MRI images)
3. Type: "Does this MRI show a brain tumor?"
4. Expected: Analysis from BRAIN_TUMOR_AGENT

#### **Skin Lesion Testing:**
1. Click the paperclip 📎 button
2. Upload a skin lesion image from `sample_images/skin_lesion_images/`
3. Type: "Is this skin lesion concerning?"
4. Expected: Analysis from SKIN_LESION_AGENT

## 🔍 Troubleshooting

### **If Agents Aren't Routing Correctly:**

1. **Check the browser console** for JavaScript errors
2. **Verify API keys** are set in your `.env` file:
   ```bash
   PINECONE_API_KEY=your_key_here
   GROQ_API_KEY=your_key_here
   ```
3. **Check server logs** - Look for error messages in the terminal where the server is running
4. **Ensure models are loaded** - Check that the medical image analysis models are present in the correct directories

### **If Images Aren't Displaying:**
- Make sure you're using supported formats (PNG, JPG, JPEG)
- Check file size (should be under the configured limit)
- Verify the image preview shows correctly in the chat before sending

### **If Responses Are Too Brief:**
- The new prompts should provide more elaborate responses
- Check that the RAG system has sufficient medical documents ingested

## 📊 Expected Response Format

All responses should now be:
- **Polite and empathetic** - Speaking as a caring physician
- **Elaborate and thorough** - Providing comprehensive explanations
- **Simple and clear** - Using everyday language
- **Professional** - Maintaining medical accuracy

## 🎯 Quick Test Script

You can also run this automated test script:

```bash
cd /Users/vasupatel/Desktop/MedAgentica/Multi-Agent-Medical-Assistant
python -c "
from agents.agent_decision import process_query

# Test conversation agent
print('Testing Conversation Agent...')
result = process_query('Hello, how are you?')
print(f'Agent: {result.agent_name}')
print(f'Response preview: {result.messages[-1].content[:100]}...')

# Test RAG agent
print('\nTesting RAG Agent...')
result = process_query('What are the symptoms of diabetes?')
print(f'Agent: {result.agent_name}')
print(f'Response preview: {result.messages[-1].content[:100]}...')
"
```

## ✅ Success Indicators

- ✅ **Conversation Agent**: Friendly, contextual responses
- ✅ **RAG Agent**: Detailed medical information with citations
- ✅ **Web Search Agent**: Current medical news and developments
- ✅ **Image Analysis Agents**: Proper routing and analysis results for uploaded images
- ✅ **No Path Display**: Images show as previews, not file paths
- ✅ **Polite Responses**: All responses sound like a caring physician

If all these work correctly, your Multi-Agent Medical Assistant is fully functional! 🎉






