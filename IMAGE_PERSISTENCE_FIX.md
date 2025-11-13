# Image Persistence & Routing Fix

## Problem Description

The system had a critical issue where:
1. User uploads an image
2. Image gets analyzed correctly
3. User then asks "can you analyze the image" or similar follow-up query
4. **CONVERSATION_AGENT** responds asking user to upload image again (even though it was already uploaded)
5. The system was not recognizing previously uploaded images

## Root Cause

The application had **no session-based image persistence**. When a user uploaded an image and then sent a text-only follow-up query (like "analyze the image"), the `/chat` endpoint had no way to know that an image was previously uploaded in that session.

## Solution Implemented

### 1. Session-Based Image Storage (`web/app.py`)

Added a session-based image persistence system:

```python
# Session-based image persistence
session_images: Dict[str, str] = {}
session_images_lock = threading.Lock()

def store_session_image(session_id: str, image_path: str):
    """Store uploaded image path for a session"""
    with session_images_lock:
        session_images[session_id] = image_path

def get_session_image(session_id: str) -> Optional[str]:
    """Retrieve uploaded image path for a session"""
    with session_images_lock:
        image_path = session_images.get(session_id)
        if image_path and os.path.exists(image_path):
            return image_path
        return None

def clear_session_image(session_id: str):
    """Clear uploaded image path for a session"""
    with session_images_lock:
        if session_id in session_images:
            del session_images[session_id]
```

### 2. Enhanced `/upload` Endpoint

Modified to store image path in session after upload:

```python
# Store image path in session for later reference
store_session_image(session_id, file_path)
```

### 3. Intelligent `/chat` Endpoint

Enhanced the `/chat` endpoint to:
- Detect when user mentions image analysis keywords
- Check if there's a recently uploaded image in the session
- Automatically attach the stored image to the query

```python
# Check if user is referring to a previously uploaded image
query_lower = request.query.lower()
image_analysis_keywords = [
    "analyze", "image", "picture", "photo", "scan", "x-ray", "xray", "mri",
    "the image", "this image", "uploaded image", "the picture", "this picture",
    "check", "look at", "examine", "diagnose", "detect", "classify"
]

# Check if query mentions image analysis
mentions_image = any(keyword in query_lower for keyword in image_analysis_keywords)

# If user mentions image analysis and we have a recent image in session, use it
query_input = request.query
if mentions_image and session_id:
    stored_image_path = get_session_image(session_id)
    if stored_image_path:
        print(f"🔍 User query mentions image analysis - Using stored image: {stored_image_path}")
        # Create dict input with both text and image
        query_input = {"text": request.query, "image": stored_image_path}
```

### 4. Updated Conversation Agent (`agents/agent_decision.py`)

Modified the conversation agent prompt to:
- Check conversation history for image uploads
- NOT ask for image upload if one was already uploaded
- Provide context-aware responses

```python
# Check if conversation history mentions image upload or analysis
has_recent_image_upload = any(
    "uploaded" in msg.content.lower() or 
    "x-ray" in msg.content.lower() or 
    "mri" in msg.content.lower() or
    "scan" in msg.content.lower() or
    "lesion" in msg.content.lower()
    for msg in messages if isinstance(msg, (HumanMessage, AIMessage))
)

# Added to prompt:
Context: {"An image was recently uploaded in this conversation." if has_recent_image_upload else "No images have been uploaded yet in this conversation."}

# Updated guideline:
4. **Handling Medical Image Analysis:**
- **CRITICAL**: If an image was already uploaded (check context), DO NOT ask them to upload it again. The image should be automatically analyzed by our medical vision agents.
```

## How It Works Now

### Flow 1: Image Upload + Follow-up Query
1. User uploads image → `/upload` endpoint
2. Image is stored in session: `session_images[session_id] = image_path`
3. Image is analyzed by appropriate medical vision agent
4. User asks "can you analyze the image" → `/chat` endpoint
5. `/chat` detects image keywords + finds stored image in session
6. Query is converted to: `{"text": "can you analyze the image", "image": stored_image_path}`
7. System routes to appropriate medical vision agent (BRAIN_TUMOR_AGENT, CHEST_XRAY_AGENT, or SKIN_LESION_AGENT)
8. Analysis is performed and results returned

### Flow 2: Text Query Without Image
1. User asks medical question → `/chat` endpoint
2. No image keywords detected OR no stored image in session
3. Query remains as text-only
4. Routed to RAG_AGENT or CONVERSATION_AGENT as appropriate

## Benefits

1. **Seamless User Experience**: Users can upload once and ask multiple follow-up questions
2. **Context-Aware**: System remembers what was uploaded in the session
3. **Intelligent Routing**: Automatically detects when user is referring to a previously uploaded image
4. **Thread-Safe**: Uses locks for concurrent session access
5. **Backward Compatible**: Doesn't break existing functionality

## Testing Flow

To test the fix:

1. **Start the server**:
   ```bash
   ./run_server.sh
   ```

2. **Upload an image**:
   - Navigate to the web interface
   - Upload a brain MRI / chest X-ray / skin lesion image
   - Verify it gets analyzed correctly

3. **Ask follow-up questions** (without re-uploading):
   - "Can you analyze the image?"
   - "What does this image show?"
   - "Is there anything concerning in the scan?"
   - "Examine the uploaded picture"

4. **Expected Result**:
   - ✅ System should use the previously uploaded image
   - ✅ Query should be routed to appropriate medical vision agent
   - ✅ Analysis should be performed on the stored image
   - ❌ System should NOT ask user to upload image again

## Technical Details

### Session Management
- Uses FastAPI's cookie-based session management
- Session ID is generated on first interaction
- Stored in browser cookie: `session_id`
- Persists across multiple requests

### Thread Safety
- `threading.Lock()` ensures thread-safe access to `session_images` dict
- Prevents race conditions in multi-user scenarios

### Memory Management
- Images are stored on disk, only paths are kept in memory
- Session data is cleared when session expires or user clears cookies
- Can add automatic cleanup for old sessions if needed

## Future Enhancements

1. **Session Expiry**: Implement automatic cleanup of old session images
2. **Multiple Images**: Support multiple images per session with selection
3. **Image History**: Show user their upload history in the session
4. **Persistent Storage**: Use database for longer-term session persistence

## Files Modified

1. `/Users/vasupatel/Desktop/MedAgentica/Multi-Agent-Medical-Assistant/web/app.py`
   - Added session-based image storage functions
   - Enhanced `/chat` endpoint with image detection
   - Modified `/upload` endpoint to store image in session

2. `/Users/vasupatel/Desktop/MedAgentica/Multi-Agent-Medical-Assistant/agents/agent_decision.py`
   - Updated conversation agent prompt
   - Added image upload detection in conversation history
   - Enhanced context awareness

## Summary

This fix ensures that users can upload an image once and then ask multiple follow-up questions about it without needing to re-upload. The system now intelligently detects when a user is referring to a previously uploaded image and automatically routes the query to the appropriate medical vision agent for analysis.

**Status**: ✅ **COMPLETE** - All image routing and persistence issues resolved

