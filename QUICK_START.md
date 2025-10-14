# 🚀 Quick Start Guide - Neo-Aurora MedAgentica

## 🎯 Get Started in 3 Steps

### Step 1: Launch the Application

**Option A: Python Launcher (Easiest & Most Reliable)**
```bash
cd Multi-Agent-Medical-Assistant
python launch.py
```

**Option B: Bash Script**
```bash
cd Multi-Agent-Medical-Assistant
./launch_neo_aurora.sh
```

**Option C: Manual Launch**
```bash
cd Multi-Agent-Medical-Assistant
source venv/bin/activate
export PYTHONPATH="$(pwd):$PYTHONPATH"
cd web
python app.py
```

### Step 2: Open Your Browser
Navigate to: **http://localhost:8000**

### Step 3: Start Chatting!
That's it! You're ready to experience the Neo-Aurora interface! 🌌

---

## 🎨 What You'll See

### The Beautiful Landing Page
```
╔══════════════════════════════════════════════════════════╗
║  🏥 MedAgentica                                    ⚙️    ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║   Your AI-Powered                                        ║
║   Medical Assistant                                      ║
║                                                          ║
║   Advanced multi-agent system powered by cutting-edge   ║
║   AI. Get instant medical insights, image analysis,     ║
║   and research-backed answers.                          ║
║                                                          ║
║   [●] Multi-Agent  [●] Real-time  [●] RAG Powered      ║
║                                                          ║
║   ┌──────────┬──────────┬──────────┬──────────┐        ║
║   │ Active   │ Queries  │ Response │ Success  │        ║
║   │ Agents   │ Processed│ Time     │ Rate     │        ║
║   │   6      │    0     │   ~2s    │   98%    │        ║
║   └──────────┴──────────┴──────────┴──────────┘        ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

---

## 💬 How to Chat

### Basic Text Query
```
You: What are the symptoms of diabetes?

[📚 RAG Agent]
Diabetes symptoms include:
• Increased thirst and frequent urination
• Extreme fatigue
• Blurred vision
• Slow-healing wounds
...
```

### Upload Medical Image
```
1. Click the 📎 paperclip icon
2. Select your medical image (or drag & drop)
3. Add optional text description
4. Press Send

[🧠 Brain Tumor Agent]
Analysis complete! The MRI scan shows...
[View Full Image] 🖼️
```

---

## 🤖 Available Agents

### 💬 Conversation Agent
**When to use:** General health questions, greetings, casual chat

**Example:**
```
You: Hello! How are you today?

[💬 Conversation Agent]
Hello! I'm here and ready to help you with any health-related 
questions or concerns. How can I assist you today?
```

### 📚 RAG Agent
**When to use:** Specific medical knowledge questions

**Example:**
```
You: Explain how insulin regulates blood sugar

[📚 RAG Agent]
Insulin is a hormone produced by the pancreas that regulates 
blood glucose levels by:

1. **Glucose Uptake**: Facilitates cellular glucose absorption
2. **Glycogen Storage**: Converts excess glucose to glycogen
3. **Fat Storage**: Promotes fat synthesis in adipose tissue
...
```

### 🌐 Web Search Agent
**When to use:** Latest medical research, current health news

**Example:**
```
You: What's the latest research on COVID-19 treatments?

[🌐 Web Search Agent]
Based on recent medical publications:

📄 Recent Study (2024): "New antiviral shows promise..."
📄 Clinical Trial Results: "Monoclonal antibodies..."
...
```

### 🧠 Brain Tumor Agent
**When to use:** Analyzing brain MRI scans

**Example:**
```
You: [Uploads brain MRI scan]

[🧠 Brain Tumor Agent]
MRI Analysis Complete:
• Region detected: Frontal lobe
• Tumor classification: [Result]
• Segmentation: [View Image]
```

### 🫁 Chest X-ray Agent
**When to use:** Analyzing chest X-rays for COVID-19

**Example:**
```
You: [Uploads chest X-ray]

[🫁 Chest X-ray Agent]
The analysis indicates: POSITIVE for COVID-19
Confidence: 94%
[View Detailed Analysis]
```

### 🩺 Skin Lesion Agent
**When to use:** Analyzing skin conditions

**Example:**
```
You: [Uploads skin lesion photo]

[🩺 Skin Lesion Agent]
Segmentation complete! 
Classification: Benign
[View Segmented Image]
```

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Send message |
| `Shift + Enter` | New line in message |
| `Ctrl + U` | Toggle file upload area |
| `↑↑↓↓←→←→BA` | Activate rainbow mode 🌈 |

---

## 🎨 Cool Features to Try

### 1. **Copy Messages**
Hover over any assistant message → Click the copy icon in top-right corner
```
✓ Copied to clipboard!
```

### 2. **View Images Full-Screen**
Click any medical image to open it in full-screen modal
```
Click anywhere to close
```

### 3. **Drag & Drop Images**
Drag any medical image directly into the chat window
```
Drop your medical image here! 📤
```

### 4. **Watch the Aurora**
Notice the beautiful floating orbs in the background—they create an aurora effect! 🌌

### 5. **Agent Color Coding**
Each agent has its own color:
- 💬 Conversation: Green
- 📚 RAG: Purple
- 🌐 Web: Blue
- 🩺 Medical: Pink

---

## 📊 KPI Dashboard

Watch the stats update in real-time as you use the system:

```
┌─────────────────────────────────────────────────┐
│ Active Agents: 6                                │
│ ↑ Increases when new agents are loaded         │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ Queries Processed: [Counter]                    │
│ ↑ Increments with each message you send        │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ Avg Response Time: ~2s                          │
│ ↑ Shows average AI response speed              │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ Success Rate: 98%                               │
│ ↑ Percentage of successful responses           │
└─────────────────────────────────────────────────┘
```

---

## 🎯 Example Conversations

### Example 1: Health Query
```
╔══════════════════════════════════════════════════════╗
║ You                                                  ║
║ What causes high blood pressure?                    ║
╚══════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════╗
║ [📚 RAG Agent]                                       ║
║                                                      ║
║ High blood pressure (hypertension) can be caused    ║
║ by several factors:                                 ║
║                                                      ║
║ **Lifestyle Factors:**                              ║
║ • High sodium diet                                  ║
║ • Lack of physical activity                         ║
║ • Excessive alcohol consumption                     ║
║ • Smoking                                           ║
║                                                      ║
║ **Medical Conditions:**                             ║
║ • Kidney disease                                    ║
║ • Diabetes                                          ║
║ • Sleep apnea                                       ║
║                                                      ║
║ **Other Factors:**                                  ║
║ • Age (risk increases with age)                     ║
║ • Family history                                    ║
║ • Stress                                            ║
║                                                      ║
║                                             [Copy]  ║
╚══════════════════════════════════════════════════════╝
```

### Example 2: Image Analysis
```
╔══════════════════════════════════════════════════════╗
║ You                                                  ║
║ 📎 [chest-xray.jpg]                                 ║
║ Please analyze this chest X-ray                     ║
╚══════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════╗
║ [Processing...]                                      ║
║ ● ● ●                                                ║
╚══════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════╗
║ [🫁 Chest X-ray Agent]                              ║
║                                                      ║
║ The analysis of the uploaded chest X-ray image     ║
║ indicates a **POSITIVE** result for **COVID-19**.  ║
║                                                      ║
║ Confidence: 94%                                     ║
║                                                      ║
║ [View Full Image] 🖼️                                ║
║                                             [Copy]  ║
╚══════════════════════════════════════════════════════╝
```

### Example 3: Latest Research
```
╔══════════════════════════════════════════════════════╗
║ You                                                  ║
║ What's new in Alzheimer's research?                 ║
╚══════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════╗
║ [🌐 Web Search Agent]                               ║
║                                                      ║
║ Based on recent medical publications:               ║
║                                                      ║
║ **2024 Breakthrough Study:**                        ║
║ Researchers at Johns Hopkins have identified a      ║
║ new biomarker that can detect Alzheimer's up to    ║
║ 15 years before symptoms appear.                    ║
║                                                      ║
║ **Clinical Trials:**                                ║
║ Phase 3 trials of lecanemab show promising         ║
║ results in slowing cognitive decline by 27%.       ║
║                                                      ║
║ **Prevention Research:**                            ║
║ New studies suggest that Mediterranean diet        ║
║ combined with regular exercise can reduce risk     ║
║ by up to 40%.                                       ║
║                                                      ║
║ 🔗 Sources: [NIH, JAMA, Lancet]                    ║
║                                             [Copy]  ║
╚══════════════════════════════════════════════════════╝
```

---

## 🐛 Troubleshooting

### Issue: "Missing credentials" or Azure OpenAI error
**Solution:**
Your `.env` file needs API keys. Make sure you have:
```env
# Use Groq (fast & free!)
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# OR use OpenRouter
OPENROUTER_API_KEY=your_key_here

# OR use OpenAI
OPENAI_API_KEY=sk_your_key_here
```
**Note:** Variable names are case-insensitive now (both GROQ_API_KEY and groq_api_key work!)

See `API_KEY_FIX.md` for detailed instructions.

### Issue: "ModuleNotFoundError: No module named 'config'"
**Solution:**
Use the Python launcher which sets paths automatically:
```bash
python launch.py
```

Or manually set PYTHONPATH:
```bash
export PYTHONPATH="$(pwd):$PYTHONPATH"
```

### Issue: Page won't load
**Solution:**
```bash
# Check if the server is running
# You should see: "Uvicorn running on http://0.0.0.0:8000"

# If not, restart:
cd Multi-Agent-Medical-Assistant
python launch.py
```

### Issue: Images won't upload
**Check:**
- File size < 5MB ✓
- Format: PNG, JPG, or JPEG ✓
- Browser console for errors ✓

### Issue: Animations are laggy
**Solution:**
- Enable hardware acceleration in browser
- Close other heavy tabs
- Try a different browser

### Issue: Agent not responding
**Check:**
- Backend is running ✓
- API keys are configured in .env ✓
- Check terminal for error messages ✓

---

## 🎉 Tips for Best Experience

### 1. **Be Specific**
```
✗ "Tell me about diabetes"
✓ "What are the early warning signs of type 2 diabetes?"
```

### 2. **Use Image Upload for Analysis**
```
✓ Upload clear, well-lit medical images
✓ Add context in your message
✓ Click images to view full-screen
```

### 3. **Explore Different Agents**
```
Try asking the same question different ways to see which
agent provides the best answer for your needs!
```

### 4. **Copy Important Information**
```
Use the copy button to save medical information for later
reference or to share with healthcare providers.
```

### 5. **Enjoy the Visuals!**
```
Take a moment to appreciate the aurora background, the
smooth animations, and the beautiful glassmorphism effects.
```

---

## 📱 Mobile Experience

The interface is fully responsive! Try it on:
- 📱 iPhone/Android phones
- 📱 iPad/tablets
- 💻 Laptops
- 🖥️ Desktop monitors

Everything adapts beautifully to your screen size!

---

## 🌟 What Makes This Special

### Traditional Medical Chatbots:
```
┌────────────────────────┐
│ > User message         │
│                        │
│ Bot: Response          │
│                        │
│ > User message         │
│                        │
│ Bot: Response          │
└────────────────────────┘
```

### Neo-Aurora MedAgentica:
```
╔═══════════════════════════════════════════════════╗
║        🌌 Beautiful Aurora Background              ║
║     ✨ Floating Orbs & Animations ✨              ║
║                                                    ║
║  🏥 MedAgentica                                    ║
║                                                    ║
║  ┌─────────┬─────────┬─────────┬─────────┐       ║
║  │ KPI 1   │ KPI 2   │ KPI 3   │ KPI 4   │       ║
║  └─────────┴─────────┴─────────┴─────────┘       ║
║                                                    ║
║  ╭────────────────────────────────────────────╮  ║
║  │ [💬 Conversation Agent]                    │  ║
║  │ Beautiful message with agent badge         │  ║
║  │ • Markdown support                         │  ║
║  │ • Syntax highlighting                      │  ║
║  │ • Copy button                       [Copy] │  ║
║  ╰────────────────────────────────────────────╯  ║
║                                                    ║
║        ╭────────────────────────────────╮         ║
║        │ Your message with gradient bg │         ║
║        ╰────────────────────────────────╯         ║
║                                                    ║
║  [📎] [Type your message here...        ] [🚀]   ║
╚═══════════════════════════════════════════════════╝
```

---

## 🎊 Ready to Experience It?

### Launch Now:
```bash
./launch_neo_aurora.sh
```

### Then visit:
```
http://localhost:8000
```

### And prepare to be amazed! ✨

---

## 📚 More Resources

- **Full Feature List**: See `FEATURES_SHOWCASE.md`
- **Design Guide**: See `NEO_AURORA_GUIDE.md`
- **Main Documentation**: See `README.md`

---

## 🎨 Have Fun!

This isn't just a medical assistant—it's an **experience**. Enjoy the beautiful design, smooth animations, and powerful AI capabilities!

**Welcome to the future of medical AI! 🌌✨**

---

*Built with ❤️ and creativity at level 1000/100*

