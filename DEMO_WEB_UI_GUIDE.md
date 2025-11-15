# 🎨 Agentic RAG Web Interface - User Guide

## Overview

A beautiful, modern web interface for your Agentic RAG system, featuring a clean chat UI similar to ChatGPT with:

- **Sidebar**: Conversation history and management
- **Modern Chat Interface**: Clean, professional design
- **Real-time Responses**: Powered by the 4-agent RAG workflow
- **Message Actions**: Copy, regenerate, and view metadata
- **Responsive Design**: Works on desktop and mobile

---

## 🚀 Quick Start

### 1. Make sure your `.env` is configured

```bash
PINECONE_API_KEY=pcsk_your_key_here
PINECONE_INDEX_NAME=medagentica
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

### 2. Run the web interface

```bash
python demo_agentic_rag_web.py
```

### 3. Open your browser

Navigate to: **http://localhost:8001**

---

## ✨ Features

### Sidebar
- **🏥 MedRAG A.I+** - Professional branding
- **✚ New chat** - Create new conversations
- **Conversation History** - Access past chats
- **🗑️ Clear All** - Remove all conversations

### Chat Interface
- **Empty State** - Friendly welcome message
- **User Messages** - Purple gradient avatar
- **Assistant Messages** - Pink gradient avatar
- **Message Actions**:
  - 📋 **Copy** - Copy message to clipboard
  - 🔄 **Regenerate** - Get a new response
  - ℹ️ **Info** - View metadata (confidence, sources, etc.)

### Input Area
- **Auto-resizing** textarea
- **Enter to send** (Shift+Enter for new line)
- **Send button** with hover effects

---

## 🎨 Design Features

### Color Scheme
- **Primary**: Indigo (#6366f1)
- **Background**: Light gray (#f8f9fa)
- **Sidebar**: Dark slate (#2c3e50)
- **Messages**: White with subtle borders

### Typography
- **Font**: System font stack (SF Pro, Segoe UI, Roboto)
- **Headings**: Bold, clear hierarchy
- **Body**: Comfortable reading size (15px)

### Animations
- **Fade in** - New messages
- **Loading dots** - Animated while processing
- **Hover effects** - Smooth transitions

---

## 🔧 API Endpoints

The backend provides these endpoints:

- `GET /` - Serve HTML interface
- `GET /api/conversations` - List all conversations
- `POST /api/conversations/new` - Create new conversation
- `GET /api/conversations/{id}` - Get conversation messages
- `DELETE /api/conversations` - Clear all conversations
- `POST /api/chat` - Send message and get response
- `POST /api/regenerate` - Regenerate last response

---

## 💬 Usage Examples

### Starting a Conversation

1. Click **✚ New chat** in sidebar
2. Type your medical question in the input box
3. Press **Enter** or click the send button (➤)
4. Wait for the AI to process (you'll see loading dots)
5. View the response with metadata

### Example Questions

- "What are the symptoms of diabetes?"
- "How does insulin work in the body?"
- "Explain the difference between Type 1 and Type 2 diabetes"
- "What are the treatment options for hypertension?"

### Using Message Actions

**Copy a Message**:
- Click the 📋 **Copy** button below any assistant message
- The message text is copied to your clipboard

**Regenerate Response**:
- Click 🔄 **Regenerate** to get a different answer
- The system will re-query with the same question

**View Metadata**:
- Click ℹ️ **Info** to see:
  - Confidence score (0-100%)
  - Number of documents retrieved
  - Query type (factual, procedural, etc.)
  - Query complexity (simple, moderate, complex)

---

## 🎯 Comparison: CLI vs Web Interface

### CLI Demo (`interactive_demo.py`)

**Pros**:
- ✅ Lightweight, terminal-based
- ✅ Shows detailed logs
- ✅ Debug mode available
- ✅ Good for development

**Cons**:
- ❌ Basic text interface
- ❌ No conversation history
- ❌ No visual formatting

### Web UI (`demo_agentic_rag_web.py`)

**Pros**:
- ✅ Beautiful, modern interface
- ✅ Conversation management
- ✅ Message history
- ✅ Copy/regenerate features
- ✅ Responsive design
- ✅ Better UX for demos

**Cons**:
- ❌ Requires web browser
- ❌ More complex setup

---

## 📱 Responsive Design

The interface works on:
- 💻 **Desktop** (recommended): Full sidebar and chat
- 📱 **Tablet**: Optimized layout
- 📱 **Mobile**: Sidebar can be toggled

---

## 🔒 Data Storage

**Current Implementation**:
- Conversations stored in memory
- Data cleared when server restarts

**For Production**:
- Consider using a database (PostgreSQL, MongoDB)
- Add user authentication
- Persist conversation history

---

## 🚀 Next Steps

### Enhancements You Can Add

1. **User Authentication**
   - Login/signup system
   - User-specific conversations

2. **Database Integration**
   - PostgreSQL or MongoDB
   - Persistent storage

3. **Advanced Features**
   - Export conversations (PDF, MD)
   - Search within conversations
   - Favorite/bookmark messages
   - Share conversations

4. **Customization**
   - Theme switcher (light/dark)
   - Font size adjustment
   - Custom avatars

5. **Analytics**
   - Query statistics
   - Response time tracking
   - Popular topics

---

## 🐛 Troubleshooting

### Issue: "RAG system not initialized"

**Solution**:
```bash
# Check your .env file
cat .env

# Ensure these are set:
PINECONE_API_KEY=pcsk_...
GROQ_API_KEY=gsk_...
```

### Issue: Port 8001 already in use

**Solution**:
```bash
# Kill the process using port 8001
lsof -ti:8001 | xargs kill -9

# Or change the port in demo_agentic_rag_web.py
# Line: uvicorn.run(app, host="0.0.0.0", port=8002)
```

### Issue: Messages not appearing

**Solution**:
- Check browser console for errors (F12)
- Ensure backend is running
- Verify API key in .env file
- Check terminal for error messages

---

## 🎉 Enjoy!

You now have a beautiful, production-ready web interface for your Agentic RAG system!

**Tips**:
- Try different types of medical questions
- Use the regenerate feature to compare responses
- Check metadata to see how the system is reasoning
- Explore conversation history in the sidebar

---

**Built with ❤️ using FastAPI, modern HTML/CSS/JS**

*For more information, see the main README.md*

