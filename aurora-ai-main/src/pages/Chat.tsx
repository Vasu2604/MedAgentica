import { useState, useRef, useEffect } from "react";
import { Send, Plus, Search, MoreVertical, Sparkles, Image, X, Loader2, Bot } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { apiService, type ChatResponse } from "@/lib/api";
import { toast } from "sonner";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  agent?: string;
  thinking?: string;
  suggestions?: string[];
  result_image?: string;
}

interface Conversation {
  id: string;
  title: string;
  preview: string;
  timestamp: Date;
  messages: Message[];
}

// Helper function to get agent emoji and color
const getAgentDisplay = (agent: string) => {
  const agentName = agent.toLowerCase();
  
  if (agentName.includes('rag')) {
    return { emoji: '📚', name: 'RAG Agent', color: 'bg-purple-500/20 text-purple-700 border-purple-500/30' };
  } else if (agentName.includes('web') || agentName.includes('search')) {
    return { emoji: '🌐', name: 'Web Search', color: 'bg-blue-500/20 text-blue-700 border-blue-500/30' };
  } else if (agentName.includes('brain') || agentName.includes('tumor')) {
    return { emoji: '🧠', name: 'Brain Tumor', color: 'bg-pink-500/20 text-pink-700 border-pink-500/30' };
  } else if (agentName.includes('chest') || agentName.includes('xray')) {
    return { emoji: '🫁', name: 'Chest X-ray', color: 'bg-pink-500/20 text-pink-700 border-pink-500/30' };
  } else if (agentName.includes('skin') || agentName.includes('lesion')) {
    return { emoji: '🩺', name: 'Skin Lesion', color: 'bg-pink-500/20 text-pink-700 border-pink-500/30' };
  } else if (agentName.includes('conversation')) {
    return { emoji: '💬', name: 'Conversation', color: 'bg-green-500/20 text-green-700 border-green-500/30' };
  } else {
    return { emoji: '🤖', name: 'AI Assistant', color: 'bg-gray-500/20 text-gray-700 border-gray-500/30' };
  }
};

const Chat = () => {
  const [conversations, setConversations] = useState<Conversation[]>([
    {
      id: "1",
      title: "New Conversation",
      preview: "Start chatting with the AI assistant...",
      timestamp: new Date(),
      messages: [
        {
          id: "welcome",
          role: "assistant",
          content: "Hello! I'm your AI-powered Medical Assistant. I can help you with:\n\n- **Medical Information**: Ask about symptoms, conditions, and treatments\n- **Image Analysis**: Upload medical images (X-rays, MRI scans, skin lesions)\n- **Web Research**: Get the latest medical research and guidelines\n- **General Health**: Discuss health concerns and get guidance\n\nHow can I assist you today?",
          timestamp: new Date(),
          agent: "CONVERSATION_AGENT",
        },
      ],
    },
  ]);
  
  const [selectedChat, setSelectedChat] = useState<string>("1");
  const [input, setInput] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [uploadedImages, setUploadedImages] = useState<File[]>([]);
  const [imagePreviewUrls, setImagePreviewUrls] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const currentConversation = conversations.find((c) => c.id === selectedChat);
  const messages = currentConversation?.messages || [];

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() && uploadedImages.length === 0) return;

    setIsLoading(true);

    try {
      // If there's an image, handle upload separately
      if (uploadedImages.length > 0) {
        await handleImageUpload();
        return;
      }

      // Create user message
      const userMessage: Message = {
        id: Date.now().toString(),
        role: "user",
        content: input,
        timestamp: new Date(),
      };

      // Add user message to conversation
      setConversations((prev) =>
        prev.map((conv) =>
          conv.id === selectedChat
            ? {
                ...conv,
                messages: [...conv.messages, userMessage],
                preview: input.slice(0, 50),
                timestamp: new Date(),
              }
            : conv
        )
      );

      setInput("");

      // Send to backend
      const response: ChatResponse = await apiService.sendMessage(input);

      // Create assistant message
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response.response,
        timestamp: new Date(),
        agent: response.agent,
        thinking: response.thinking,
        suggestions: response.suggestions,
        result_image: response.result_image,
      };

      // Add assistant message to conversation
      setConversations((prev) =>
        prev.map((conv) =>
          conv.id === selectedChat
            ? { ...conv, messages: [...conv.messages, assistantMessage] }
            : conv
        )
      );
    } catch (error) {
      console.error("Error sending message:", error);
      toast.error("Failed to send message. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleImageUpload = async () => {
    if (uploadedImages.length === 0) return;

    try {
      // Create user message with image
      const userMessage: Message = {
        id: Date.now().toString(),
        role: "user",
        content: input || "Please analyze this medical image.",
        timestamp: new Date(),
      };

      // Add user message to conversation
      setConversations((prev) =>
        prev.map((conv) =>
          conv.id === selectedChat
            ? {
                ...conv,
                messages: [...conv.messages, userMessage],
                preview: "Image uploaded",
                timestamp: new Date(),
              }
            : conv
        )
      );

      setInput("");

      // Upload to backend (only first image for now)
      const response = await apiService.uploadImage(uploadedImages[0], input);

      // Create assistant message
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response.response,
        timestamp: new Date(),
        agent: response.agent,
        thinking: response.thinking,
        suggestions: response.suggestions,
        result_image: response.result_image,
      };

      // Add assistant message to conversation
      setConversations((prev) =>
        prev.map((conv) =>
          conv.id === selectedChat
            ? { ...conv, messages: [...conv.messages, assistantMessage] }
            : conv
        )
      );

      // Clear uploaded images
      setUploadedImages([]);
      setImagePreviewUrls([]);
    } catch (error) {
      console.error("Error uploading image:", error);
      toast.error("Failed to upload image. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const filteredConversations = conversations.filter((conv) =>
    conv.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files) {
      const fileArray = Array.from(files);
      setUploadedImages(fileArray);
      
      // Create preview URLs
      const urls = fileArray.map((file) => URL.createObjectURL(file));
      setImagePreviewUrls(urls);
    }
  };

  const removeImage = (index: number) => {
    setUploadedImages(uploadedImages.filter((_, i) => i !== index));
    
    // Revoke old URL to prevent memory leaks
    URL.revokeObjectURL(imagePreviewUrls[index]);
    setImagePreviewUrls(imagePreviewUrls.filter((_, i) => i !== index));
  };

  const handleNewChat = () => {
    const newId = (conversations.length + 1).toString();
    const newConv: Conversation = {
      id: newId,
      title: "New Conversation",
      preview: "Start chatting...",
      timestamp: new Date(),
      messages: [
        {
          id: "welcome-" + newId,
          role: "assistant",
          content: "Hello! How can I help you today?",
          timestamp: new Date(),
          agent: "CONVERSATION_AGENT",
        },
      ],
    };
    
    setConversations([newConv, ...conversations]);
    setSelectedChat(newId);
  };

  const handleSuggestionClick = (suggestion: string) => {
    setInput(suggestion);
  };

  return (
    <div className="flex h-screen w-full overflow-hidden">
      {/* Left Sidebar - Conversations */}
      <div className="w-80 border-r border-border bg-sidebar flex flex-col">
        <div className="p-4 border-b border-border">
          <Button
            className="w-full justify-start gap-2 glass-card hover:bg-primary/10"
            variant="outline"
            onClick={handleNewChat}
          >
            <Plus className="h-4 w-4" />
            New Chat
          </Button>
        </div>

        <div className="p-4 border-b border-border">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search conversations..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 glass-card"
            />
          </div>
        </div>

        <ScrollArea className="flex-1">
          <div className="p-3 space-y-1">
            <div className="text-xs font-semibold text-muted-foreground px-3 py-2">
              Conversations
            </div>
            {filteredConversations.map((conv) => (
              <button
                key={conv.id}
                onClick={() => setSelectedChat(conv.id)}
                className={`w-full text-left p-3 rounded-xl transition-all hover-lift group ${
                  selectedChat === conv.id
                    ? "bg-primary/10 border border-primary/20"
                    : "hover:bg-muted/50"
                }`}
              >
                <div className="flex items-start justify-between gap-2">
                  <div className="flex-1 min-w-0">
                    <div className="font-medium text-sm truncate mb-1">
                      {conv.title}
                    </div>
                    <div className="text-xs text-muted-foreground truncate">
                      {conv.preview}
                    </div>
                  </div>
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity"
                      >
                        <MoreVertical className="h-3 w-3" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem>Rename</DropdownMenuItem>
                      <DropdownMenuItem>Archive</DropdownMenuItem>
                      <DropdownMenuItem className="text-destructive">
                        Delete
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
              </button>
            ))}
          </div>
        </ScrollArea>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Chat Header */}
        <div className="h-16 border-b border-border px-6 flex items-center justify-between glass-card">
          <div className="flex items-center gap-3">
            <Sparkles className="h-5 w-5 text-primary" />
            <div>
              <h2 className="font-semibold">{currentConversation?.title || "Chat"}</h2>
              <p className="text-xs text-muted-foreground">Multi-Agent Medical Assistant</p>
            </div>
          </div>
        </div>

        {/* Messages */}
        <ScrollArea className="flex-1 p-6">
          <div className="max-w-3xl mx-auto space-y-6 animate-fade-in">
            {messages.map((message) => {
              const agentDisplay = message.agent ? getAgentDisplay(message.agent) : null;
              
              return (
                <div
                  key={message.id}
                  className={`flex gap-4 ${
                    message.role === "user" ? "flex-row-reverse" : ""
                  }`}
                >
                  <Avatar className="h-8 w-8 shrink-0">
                    <AvatarFallback
                      className={
                        message.role === "assistant"
                          ? "bg-gradient-primary text-primary-foreground"
                          : "bg-muted"
                      }
                    >
                      {message.role === "assistant" ? <Bot className="h-4 w-4" /> : "U"}
                    </AvatarFallback>
                  </Avatar>
                  <div
                    className={`flex-1 space-y-2 ${
                      message.role === "user" ? "flex flex-col items-end" : ""
                    }`}
                  >
                    {/* Agent Badge */}
                    {agentDisplay && (
                      <Badge variant="outline" className={`${agentDisplay.color} border`}>
                        <span className="mr-1">{agentDisplay.emoji}</span>
                        {agentDisplay.name}
                      </Badge>
                    )}
                    
                    {/* Thinking Process */}
                    {message.thinking && (
                      <div className="text-xs text-muted-foreground italic px-4 py-2 rounded-lg bg-muted/50">
                        {message.thinking}
                      </div>
                    )}
                    
                    {/* Message Content */}
                    <div
                      className={`inline-block p-4 rounded-2xl glass-card ${
                        message.role === "user"
                          ? "bg-primary/10 border-primary/20"
                          : ""
                      }`}
                    >
                      <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
                      
                      {/* Result Image */}
                      {message.result_image && (
                        <div className="mt-3">
                          <img
                            src={message.result_image}
                            alt="Analysis Result"
                            className="rounded-lg border border-border max-w-md"
                          />
                        </div>
                      )}
                    </div>
                    
                    {/* Suggestions */}
                    {message.suggestions && message.suggestions.length > 0 && (
                      <div className="flex flex-wrap gap-2 mt-2">
                        {message.suggestions.map((suggestion, idx) => (
                          <Button
                            key={idx}
                            variant="outline"
                            size="sm"
                            onClick={() => handleSuggestionClick(suggestion)}
                            className="text-xs glass-card"
                          >
                            {suggestion}
                          </Button>
                        ))}
                      </div>
                    )}
                    
                    <div className="text-xs text-muted-foreground px-1">
                      {message.timestamp.toLocaleTimeString()}
                    </div>
                  </div>
                </div>
              );
            })}
            
            {/* Loading Indicator */}
            {isLoading && (
              <div className="flex gap-4">
                <Avatar className="h-8 w-8 shrink-0">
                  <AvatarFallback className="bg-gradient-primary text-primary-foreground">
                    <Bot className="h-4 w-4" />
                  </AvatarFallback>
                </Avatar>
                <div className="flex-1">
                  <div className="inline-block p-4 rounded-2xl glass-card">
                    <Loader2 className="h-4 w-4 animate-spin" />
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>
        </ScrollArea>

        {/* Input Area */}
        <div className="border-t border-border p-6 glass-card">
          <div className="max-w-3xl mx-auto">
            {/* Image Preview */}
            {imagePreviewUrls.length > 0 && (
              <div className="mb-4 flex flex-wrap gap-2">
                {imagePreviewUrls.map((url, index) => (
                  <div key={index} className="relative group">
                    <img
                      src={url}
                      alt={`Upload ${index + 1}`}
                      className="h-20 w-20 object-cover rounded-lg border border-border"
                    />
                    <button
                      onClick={() => removeImage(index)}
                      className="absolute -top-2 -right-2 h-6 w-6 bg-destructive text-destructive-foreground rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                      <X className="h-3 w-3" />
                    </button>
                  </div>
                ))}
              </div>
            )}

            <div className="relative">
              <Textarea
                placeholder="Type your message... (⌘ + Enter to send)"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
                    e.preventDefault();
                    handleSend();
                  }
                }}
                disabled={isLoading}
                className="min-h-[80px] pr-24 resize-none glass-card"
              />
              <div className="absolute right-2 bottom-2 flex gap-2">
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleImageSelect}
                  accept="image/png,image/jpeg,image/jpg"
                  multiple
                  className="hidden"
                />
                <Button
                  size="icon"
                  variant="outline"
                  onClick={() => fileInputRef.current?.click()}
                  disabled={isLoading}
                  className="h-10 w-10 glass-card"
                >
                  <Image className="h-4 w-4" />
                </Button>
                <Button
                  size="icon"
                  onClick={handleSend}
                  disabled={(!input.trim() && uploadedImages.length === 0) || isLoading}
                  className="h-10 w-10 bg-primary hover:bg-primary/90 transition-colors"
                >
                  {isLoading ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <Send className="h-4 w-4" />
                  )}
                </Button>
              </div>
            </div>
            <div className="mt-2 text-xs text-muted-foreground text-center">
              Press ⌘ + Enter to send • / for commands
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat;
