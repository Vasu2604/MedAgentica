import { useState, useRef, useEffect } from "react";
import { Send, Plus, Search, MoreVertical, Sparkles, Image, X, Loader2, Bot, Copy, Check, Menu, ChevronLeft, ChevronRight } from "lucide-react";
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
  
  if (agentName.includes('system')) {
    return { emoji: '●', name: 'SYSTEM', color: 'from-green-500 to-emerald-600', badge: 'bg-green-500/20 text-green-300 border-green-500/30' };
  } else if (agentName.includes('rag')) {
    return { emoji: '📚', name: 'RAG', color: 'from-purple-500 to-violet-600', badge: 'bg-purple-500/20 text-purple-300 border-purple-500/30' };
  } else if (agentName.includes('web') || agentName.includes('search')) {
    return { emoji: '🌐', name: 'WEB SEARCH PROCESSOR', color: 'from-blue-500 to-cyan-600', badge: 'bg-blue-500/20 text-blue-300 border-blue-500/30' };
  } else if (agentName.includes('brain') || agentName.includes('tumor')) {
    return { emoji: '🧠', name: 'BRAIN TUMOR', color: 'from-pink-500 to-rose-600', badge: 'bg-pink-500/20 text-pink-300 border-pink-500/30' };
  } else if (agentName.includes('chest') || agentName.includes('xray')) {
    return { emoji: '🫁', name: 'CHEST XRAY', color: 'from-red-500 to-orange-600', badge: 'bg-red-500/20 text-red-300 border-red-500/30' };
  } else if (agentName.includes('skin') || agentName.includes('lesion')) {
    return { emoji: '🩺', name: 'SKIN LESION', color: 'from-emerald-500 to-teal-600', badge: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30' };
  } else if (agentName.includes('conversation')) {
    return { emoji: '💬', name: 'CONVERSATION', color: 'from-green-500 to-emerald-600', badge: 'bg-green-500/20 text-green-300 border-green-500/30' };
  } else {
    return { emoji: '🤖', name: 'AI ASSISTANT', color: 'from-indigo-500 to-purple-600', badge: 'bg-indigo-500/20 text-indigo-300 border-indigo-500/30' };
  }
};

// Format text content to remove ALL markdown symbols and render cleanly with styled underlines
const formatMessageContent = (content: string): string => {
  // Remove all markdown bold syntax (**text** or __text__)
  let formatted = content.replace(/\*\*(.*?)\*\*/g, '$1');
  formatted = formatted.replace(/__(.*?)__/g, '$1');
  
  // Remove all markdown italic syntax (*text* or _text_)
  formatted = formatted.replace(/\*(.*?)\*/g, '$1');
  formatted = formatted.replace(/_(.*?)_/g, '$1');
  
  // Remove markdown headers (# ## ###)
  formatted = formatted.replace(/^#{1,6}\s+/gm, '');
  
  // Remove markdown code blocks (```code```)
  formatted = formatted.replace(/```[\s\S]*?```/g, '');
  
  // Remove markdown inline code (`code`)
  formatted = formatted.replace(/`([^`]+)`/g, '$1');
  
  // Remove markdown links but keep text [text](url) -> text
  formatted = formatted.replace(/\[([^\]]+)\]\([^\)]+\)/g, '$1');
  
  // Remove markdown images but keep alt text ![alt](url) -> alt
  formatted = formatted.replace(/!\[([^\]]+)\]\([^\)]+\)/g, '$1');
  
  // Remove markdown strikethrough (~~text~~)
  formatted = formatted.replace(/~~(.*?)~~/g, '$1');
  
  // Remove any remaining standalone * or ** symbols
  formatted = formatted.replace(/\*\*/g, '');
  formatted = formatted.replace(/\*/g, '');
  
  return formatted.trim();
};

// Component to render message content with styled underlines and bullet points
const MessageContent = ({ content }: { content: string }) => {
  const formatted = formatMessageContent(content);
  
  // Split by lines and process underlines
  const lines = formatted.split('\n');
  
  return (
    <div className="space-y-3">
      {lines.map((line, index) => {
        const trimmedLine = line.trim();
        
        // Check if line has underlines (___text___)
        const underlineMatch = trimmedLine.match(/^___([^_]+)___$/);
        if (underlineMatch) {
          return (
            <div
              key={index}
              className="text-xl font-bold text-purple-300 mt-6 mb-3 pb-3 border-b-2 border-purple-500/40 flex items-center gap-2"
            >
              <div className="h-1 w-1 rounded-full bg-purple-400" />
              {underlineMatch[1]}
            </div>
          );
        }
        
        // Check if line starts with a number (section heading)
        const numberedHeading = trimmedLine.match(/^(\d+\.\s+)(.+)$/);
        if (numberedHeading) {
          return (
            <div key={index} className="text-lg font-semibold text-white mt-4 mb-2 flex items-center gap-2">
              <span className="text-purple-400">{numberedHeading[1]}</span>
              <span className="text-purple-300">{numberedHeading[2]}</span>
            </div>
          );
        }
        
        // Check if line is a bullet point (starts with -)
        if (trimmedLine.startsWith('-')) {
          const bulletText = trimmedLine.substring(1).trim();
          return (
            <div key={index} className="flex items-start gap-3 text-base leading-relaxed text-gray-200 pl-2">
              <div className="h-1.5 w-1.5 rounded-full bg-purple-400 mt-2 shrink-0" />
              <span className="flex-1">{bulletText}</span>
            </div>
          );
        }
        
        // Check if line is a sub-bullet (starts with A) or B))
        const subBulletMatch = trimmedLine.match(/^([A-Z]\))\s+(.+)$/);
        if (subBulletMatch) {
          return (
            <div key={index} className="flex items-start gap-3 text-base font-semibold text-purple-200 mt-2 pl-4">
              <span className="text-purple-400 shrink-0">{subBulletMatch[1]}</span>
              <span className="flex-1">{subBulletMatch[2]}</span>
            </div>
          );
        }
        
        // Regular paragraph line
        if (trimmedLine.length > 0) {
          return (
            <div key={index} className="text-base leading-relaxed text-gray-200">
              {trimmedLine}
            </div>
          );
        }
        
        // Empty line for spacing
        return <div key={index} className="h-2" />;
      })}
    </div>
  );
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
          content: "👋 Welcome to MedAgentica! I'm your AI medical assistant powered by multiple specialized agents:\n\n💬 Conversation Agent - General health discussions\n\n📚 RAG Agent - Medical knowledge queries\n\n🌐 Web Search Agent - Latest medical research\n\n🧠 Brain Tumor Agent - MRI analysis\n\n🫁 Chest X-ray Agent - COVID-19 detection\n\n🩺 Skin Lesion Agent - Skin condition analysis\n\nHow can I assist you today?",
          timestamp: new Date(),
          agent: "SYSTEM",
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
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [editingConversationId, setEditingConversationId] = useState<string | null>(null);
  const [editingTitle, setEditingTitle] = useState<string>("");
  const fileInputRef = useRef<HTMLInputElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const currentConversation = conversations.find((c) => c.id === selectedChat);
  const messages = currentConversation?.messages || [];

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Listen for new-chat event from AppLayout
  useEffect(() => {
    const handleNewChatEvent = () => {
      const newId = Date.now().toString();
      const newConv: Conversation = {
        id: newId,
        title: `Chat ${conversations.length + 1}`,
        preview: "New conversation",
        timestamp: new Date(),
        messages: [
          {
            id: "welcome-" + newId,
            role: "assistant",
            content: "👋 Welcome to MedAgentica! I'm your AI medical assistant powered by multiple specialized agents:\n\n💬 Conversation Agent - General health discussions\n\n📚 RAG Agent - Medical knowledge queries\n\n🌐 Web Search Agent - Latest medical research\n\n🧠 Brain Tumor Agent - MRI analysis\n\n🫁 Chest X-ray Agent - COVID-19 detection\n\n🩺 Skin Lesion Agent - Skin condition analysis\n\nHow can I assist you today?",
            timestamp: new Date(),
            agent: "SYSTEM",
          },
        ],
      };
      
      setConversations((prev) => [newConv, ...prev]);
      setSelectedChat(newId);
    };
    
    window.addEventListener('new-chat', handleNewChatEvent);
    return () => window.removeEventListener('new-chat', handleNewChatEvent);
  }, [conversations.length]);

  const handleCopy = (messageId: string, content: string) => {
    navigator.clipboard.writeText(formatMessageContent(content));
    setCopiedId(messageId);
    setTimeout(() => setCopiedId(null), 2000);
    toast.success("Message copied to clipboard!");
  };

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
          content: "👋 Welcome to MedAgentica! I'm your AI medical assistant powered by multiple specialized agents:\n\n💬 Conversation Agent - General health discussions\n\n📚 RAG Agent - Medical knowledge queries\n\n🌐 Web Search Agent - Latest medical research\n\n🧠 Brain Tumor Agent - MRI analysis\n\n🫁 Chest X-ray Agent - COVID-19 detection\n\n🩺 Skin Lesion Agent - Skin condition analysis\n\nHow can I assist you today?",
          timestamp: new Date(),
          agent: "SYSTEM",
        },
      ],
    };
    
    setConversations([newConv, ...conversations]);
    setSelectedChat(newId);
  };

  const handleSuggestionClick = (suggestion: string) => {
    setInput(suggestion);
  };

  const handleRenameConversation = (convId: string) => {
    const conv = conversations.find(c => c.id === convId);
    if (conv) {
      setEditingConversationId(convId);
      setEditingTitle(conv.title);
    }
  };

  const handleSaveRename = () => {
    if (editingConversationId && editingTitle.trim()) {
      setConversations(prev =>
        prev.map(conv =>
          conv.id === editingConversationId
            ? { ...conv, title: editingTitle.trim() }
            : conv
        )
      );
      setEditingConversationId(null);
      setEditingTitle("");
    }
  };

  const handleCancelRename = () => {
    setEditingConversationId(null);
    setEditingTitle("");
  };

  const handleArchiveConversation = (convId: string) => {
    // For now, we'll just remove it from the list (you can implement archive logic later)
    setConversations(prev => {
      const filtered = prev.filter(conv => conv.id !== convId);
      if (selectedChat === convId) {
        setSelectedChat(filtered.length > 0 ? filtered[0].id : "");
      }
      return filtered;
    });
    toast.success("Conversation archived");
  };

  const handleDeleteConversation = (convId: string) => {
    if (window.confirm("Are you sure you want to delete this conversation? This action cannot be undone.")) {
      setConversations(prev => {
        const filtered = prev.filter(conv => conv.id !== convId);
        if (selectedChat === convId) {
          setSelectedChat(filtered.length > 0 ? filtered[0].id : "");
        }
        return filtered;
      });
      toast.success("Conversation deleted");
    }
  };

  return (
    <div className="flex h-screen w-full overflow-hidden relative">
      {/* Premium Animated Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-slate-950 via-purple-950/20 to-slate-950 pointer-events-none" />
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-purple-900/20 via-transparent to-transparent pointer-events-none" />
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_bottom_left,_var(--tw-gradient-stops))] from-blue-900/20 via-transparent to-transparent pointer-events-none" />
      
      {/* Animated Particles */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {[...Array(20)].map((_, i) => (
          <div
            key={i}
            className="absolute w-1 h-1 bg-purple-500/30 rounded-full animate-pulse"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 3}s`,
              animationDuration: `${2 + Math.random() * 3}s`,
            }}
          />
        ))}
      </div>

      {/* Left Sidebar - Conversations */}
      <div className={`${sidebarCollapsed ? 'w-12' : 'w-80'} border-r border-white/10 backdrop-blur-xl bg-slate-950/40 flex flex-col relative z-10 transition-all duration-300 overflow-visible`}>
        {/* Sidebar Toggle Button - Attached to sidebar edge */}
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
          className="absolute -right-5 top-1/2 -translate-y-1/2 z-50 bg-gradient-to-r from-purple-600/90 to-blue-600/90 border-2 border-purple-500/50 hover:from-purple-700/90 hover:to-blue-700/90 transition-all duration-300 shadow-xl shadow-purple-500/30 hover:shadow-purple-500/50 hover:scale-110 h-10 w-10 rounded-full"
          title={sidebarCollapsed ? "Show conversations" : "Hide conversations"}
        >
          {sidebarCollapsed ? (
            <ChevronRight className="h-5 w-5 text-white" />
          ) : (
            <ChevronLeft className="h-5 w-5 text-white" />
          )}
        </Button>

        {/* Sidebar Content */}
        <div className={sidebarCollapsed ? 'opacity-0 pointer-events-none overflow-hidden' : 'opacity-100 flex flex-col flex-1'}>
        {!sidebarCollapsed && (
          <>
            <div className="p-4 border-b border-white/10">
              <Button
                className="w-full justify-start gap-2 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 border-0 shadow-lg shadow-purple-500/25 transition-all duration-300 hover:shadow-purple-500/50 hover:scale-[1.02]"
                onClick={handleNewChat}
              >
                <Plus className="h-4 w-4" />
                <span className="font-semibold">New Chat</span>
              </Button>
            </div>

            <div className="p-4 border-b border-white/10">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-purple-400" />
                <Input
                  placeholder="Search conversations..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10 bg-white/5 border-white/10 focus:border-purple-500/50 focus:ring-purple-500/25 text-white placeholder:text-gray-500 transition-all duration-300"
                />
              </div>
            </div>

            <ScrollArea className="flex-1">
              <div className="p-3 space-y-2">
                <div className="text-xs font-semibold text-purple-400 px-3 py-2 uppercase tracking-wider">
                  Conversations
                </div>
                {filteredConversations.length === 0 ? (
                  <div className="text-center text-gray-500 text-sm py-8">
                    {searchQuery ? "No conversations found" : "No conversations yet"}
                  </div>
                ) : (
                  filteredConversations.map((conv) => (
                    <div
                      key={conv.id}
                      className={`w-full text-left p-3 rounded-xl transition-all duration-300 group relative overflow-hidden ${
                        selectedChat === conv.id
                          ? "bg-gradient-to-r from-purple-600/30 to-blue-600/30 border border-purple-500/50 shadow-lg shadow-purple-500/25"
                          : "hover:bg-white/5 border border-transparent"
                      }`}
                    >
                      {editingConversationId === conv.id ? (
                        <div className="flex items-center gap-2">
                          <Input
                            value={editingTitle}
                            onChange={(e) => setEditingTitle(e.target.value)}
                            onKeyDown={(e) => {
                              if (e.key === "Enter") handleSaveRename();
                              if (e.key === "Escape") handleCancelRename();
                            }}
                            className="flex-1 bg-white/10 border-white/20 text-white text-sm"
                            autoFocus
                          />
                          <Button
                            size="icon"
                            variant="ghost"
                            onClick={handleSaveRename}
                            className="h-6 w-6 text-green-400 hover:text-green-300"
                          >
                            <Check className="h-3 w-3" />
                          </Button>
                          <Button
                            size="icon"
                            variant="ghost"
                            onClick={handleCancelRename}
                            className="h-6 w-6 text-red-400 hover:text-red-300"
                          >
                            <X className="h-3 w-3" />
                          </Button>
                        </div>
                      ) : (
                        <>
                          <button
                            onClick={() => setSelectedChat(conv.id)}
                            className="w-full text-left"
                          >
                            <div className="flex items-start justify-between gap-2 relative z-10">
                              <div className="flex-1 min-w-0">
                                <div className="font-medium text-sm truncate mb-1 text-white">
                                  {conv.title}
                                </div>
                                <div className="text-xs text-gray-400 truncate">
                                  {conv.preview}
                                </div>
                              </div>
                            </div>
                          </button>
                          <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                              <Button
                                variant="ghost"
                                size="icon"
                                className="absolute top-2 right-2 h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity hover:bg-white/10"
                                onClick={(e) => e.stopPropagation()}
                              >
                                <MoreVertical className="h-3 w-3 text-gray-400" />
                              </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="end" className="bg-slate-900/95 backdrop-blur-xl border-white/10 z-50">
                              <DropdownMenuItem 
                                className="text-white hover:bg-white/10 cursor-pointer"
                                onSelect={(e) => {
                                  e.preventDefault();
                                  handleRenameConversation(conv.id);
                                }}
                              >
                                Rename
                              </DropdownMenuItem>
                              <DropdownMenuItem 
                                className="text-white hover:bg-white/10 cursor-pointer"
                                onSelect={(e) => {
                                  e.preventDefault();
                                  handleArchiveConversation(conv.id);
                                }}
                              >
                                Archive
                              </DropdownMenuItem>
                              <DropdownMenuItem 
                                className="text-red-400 hover:bg-red-500/10 cursor-pointer"
                                onSelect={(e) => {
                                  e.preventDefault();
                                  handleDeleteConversation(conv.id);
                                }}
                              >
                                Delete
                              </DropdownMenuItem>
                            </DropdownMenuContent>
                          </DropdownMenu>
                        </>
                      )}
                    </div>
                  ))
                )}
              </div>
            </ScrollArea>
          </>
        )}
        </div>
      </div>
      

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col relative z-10">
        {/* Chat Header */}
        <div className="h-16 border-b border-white/10 backdrop-blur-xl bg-slate-950/40 px-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full blur-md opacity-50" />
              <Sparkles className="h-5 w-5 text-purple-400 relative z-10" />
            </div>
            <div>
              <h2 className="font-bold text-white">{currentConversation?.title || "Chat"}</h2>
              <p className="text-xs text-purple-400">Multi-Agent Medical Assistant</p>
            </div>
          </div>
        </div>

        {/* Messages */}
        <ScrollArea className="flex-1 p-6">
          <div className="max-w-4xl mx-auto space-y-6">
            {messages.map((message) => {
              const agentDisplay = message.agent ? getAgentDisplay(message.agent) : null;
              
              return (
                <div
                  key={message.id}
                  className={`flex gap-4 animate-in slide-in-from-bottom-4 duration-500 ${
                    message.role === "user" ? "flex-row-reverse" : ""
                  }`}
                >
                  <Avatar className="h-12 w-12 shrink-0 ring-2 ring-white/20 shadow-lg">
                    <AvatarFallback
                      className={
                        message.role === "assistant"
                          ? "bg-gradient-to-br from-purple-600 via-blue-600 to-indigo-600 text-white text-sm font-semibold shadow-lg shadow-purple-500/30"
                          : "bg-gradient-to-br from-purple-500 via-pink-500 to-rose-500 text-white text-sm font-semibold shadow-lg shadow-pink-500/30"
                      }
                    >
                      {message.role === "assistant" ? <Bot className="h-6 w-6" /> : "User"}
                    </AvatarFallback>
                  </Avatar>
                  <div
                    className={`flex-1 space-y-2 ${
                      message.role === "user" ? "flex flex-col items-end" : ""
                    }`}
                  >
                    {/* Agent Badge */}
                    {agentDisplay && (
                      <Badge 
                        variant="outline" 
                        className={`${agentDisplay.badge} border-2 backdrop-blur-md font-bold px-4 py-2 text-sm shadow-lg hover:scale-105 transition-transform duration-300`}
                      >
                        <span className="mr-2 text-lg">{agentDisplay.emoji}</span>
                        {agentDisplay.name} AGENT
                      </Badge>
                    )}
                    
                    {/* Thinking Process */}
                    {message.thinking && (
                      <div className="text-sm text-purple-300 italic px-5 py-3 rounded-xl bg-gradient-to-r from-purple-950/50 to-blue-950/50 border-2 border-purple-500/30 backdrop-blur-md shadow-lg">
                        {formatMessageContent(message.thinking)}
                      </div>
                    )}
                    
                    {/* Message Content */}
                    <div
                      className={`group relative inline-block p-6 rounded-3xl backdrop-blur-xl transition-all duration-500 hover:shadow-2xl ${
                        message.role === "user"
                          ? "bg-gradient-to-br from-purple-600 via-blue-600 to-indigo-600 text-white shadow-2xl shadow-purple-500/40 hover:shadow-purple-500/60"
                          : "bg-gradient-to-br from-slate-900/90 via-slate-800/80 to-slate-900/90 border-2 border-white/20 text-white hover:bg-slate-800/90 hover:border-purple-500/30 shadow-xl shadow-black/20"
                      }`}
                    >
                      <MessageContent content={message.content} />
                      
                      {/* Result Image */}
                      {message.result_image && (
                        <div className="mt-3">
                          <img
                            src={message.result_image}
                            alt="Analysis Result"
                            className="rounded-lg border border-white/20 max-w-md shadow-xl hover:scale-[1.02] transition-transform duration-300 cursor-pointer"
                          />
                        </div>
                      )}

                      {/* Copy Button */}
                      {message.role === "assistant" && (
                        <Button
                          size="icon"
                          variant="ghost"
                          className="absolute top-2 right-2 h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity hover:bg-white/20"
                          onClick={() => handleCopy(message.id, message.content)}
                        >
                          {copiedId === message.id ? (
                            <Check className="h-3 w-3 text-green-400" />
                          ) : (
                            <Copy className="h-3 w-3 text-gray-400" />
                          )}
                        </Button>
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
                            className="text-xs bg-white/5 border-white/20 hover:bg-white/10 hover:border-purple-500/50 text-white transition-all duration-300 hover:scale-105"
                          >
                            {formatMessageContent(suggestion)}
                          </Button>
                        ))}
                      </div>
                    )}
                    
                    <div className="text-sm text-gray-400 px-2 font-light">
                      {message.timestamp.toLocaleTimeString()}
                    </div>
                  </div>
                </div>
              );
            })}
            
            {/* Loading Indicator */}
            {isLoading && (
              <div className="flex gap-4 animate-in slide-in-from-bottom-4">
                <Avatar className="h-10 w-10 shrink-0 ring-2 ring-white/10">
                  <AvatarFallback className="bg-gradient-to-br from-purple-600 to-blue-600 text-white">
                    <Bot className="h-5 w-5" />
                  </AvatarFallback>
                </Avatar>
                <div className="flex-1">
                  <div className="inline-block p-4 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-xl">
                    <div className="flex gap-2">
                      <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                      <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                      <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                    </div>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>
        </ScrollArea>

        {/* Input Area */}
        <div className="border-t border-white/10 backdrop-blur-xl bg-slate-950/40 p-6">
          <div className="max-w-4xl mx-auto">
            {/* Image Preview */}
            {imagePreviewUrls.length > 0 && (
              <div className="mb-4 flex flex-wrap gap-2">
                {imagePreviewUrls.map((url, index) => (
                  <div key={index} className="relative group">
                    <img
                      src={url}
                      alt={`Upload ${index + 1}`}
                      className="h-20 w-20 object-cover rounded-lg border border-white/20"
                    />
                    <button
                      onClick={() => removeImage(index)}
                      className="absolute -top-2 -right-2 h-6 w-6 bg-red-500 hover:bg-red-600 text-white rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-300 shadow-lg"
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
                className="min-h-[100px] pr-28 resize-none bg-white/10 border-2 border-white/20 focus:border-purple-500/70 focus:ring-2 focus:ring-purple-500/40 text-white text-base placeholder:text-gray-400 rounded-2xl transition-all duration-300 shadow-lg backdrop-blur-sm"
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
                  className="h-10 w-10 bg-white/5 border-white/20 hover:bg-white/10 hover:border-purple-500/50 transition-all duration-300 hover:scale-110"
                >
                  <Image className="h-4 w-4 text-purple-400" />
                </Button>
                <Button
                  size="icon"
                  onClick={handleSend}
                  disabled={(!input.trim() && uploadedImages.length === 0) || isLoading}
                  className="h-10 w-10 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 border-0 shadow-lg shadow-purple-500/25 transition-all duration-300 hover:shadow-purple-500/50 hover:scale-110 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isLoading ? (
                    <Loader2 className="h-4 w-4 animate-spin text-white" />
                  ) : (
                    <Send className="h-4 w-4 text-white" />
                  )}
                </Button>
              </div>
            </div>
            <div className="mt-2 text-xs text-gray-500 text-center">
              Press ⌘ + Enter to send • / for commands
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat;
