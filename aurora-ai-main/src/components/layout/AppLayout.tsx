import { Link, useLocation, useNavigate } from "react-router-dom";
import { MessageSquare, LayoutDashboard, Settings, Sparkles, Menu, Plus, Zap, TrendingUp, Activity } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useState, useEffect } from "react";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";

interface AppLayoutProps {
  children: React.ReactNode;
}

const AppLayout = ({ children }: AppLayoutProps) => {
  const location = useLocation();
  const navigate = useNavigate();
  const [collapsed, setCollapsed] = useState(false);
  const [activeStats, setActiveStats] = useState({ chats: 0, agents: 6, uptime: "99.9%" });

  useEffect(() => {
    // Simulate dynamic stats
    const interval = setInterval(() => {
      setActiveStats(prev => ({
        ...prev,
        chats: Math.floor(Math.random() * 50) + 10,
      }));
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const navItems = [
    { 
      path: "/", 
      icon: MessageSquare, 
      label: "Chat",
      badge: activeStats.chats,
      description: "AI Medical Assistant"
    },
    { 
      path: "/dashboard", 
      icon: LayoutDashboard, 
      label: "Dashboard",
      description: "Analytics & Insights"
    },
    { 
      path: "/settings", 
      icon: Settings, 
      label: "Settings",
      description: "Preferences"
    },
  ];

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  const handleNewChat = () => {
    navigate("/");
    // Trigger new chat in Chat component if needed
    window.dispatchEvent(new CustomEvent('new-chat'));
  };

  return (
    <div className="flex h-screen w-full overflow-hidden bg-gradient-to-br from-slate-950 via-purple-950/10 to-slate-950">
      {/* Premium Navigation Sidebar */}
      <div
        className={cn(
          "border-r border-white/10 bg-gradient-to-b from-slate-900/95 via-slate-900/90 to-slate-900/95 backdrop-blur-xl flex flex-col transition-all duration-500 shadow-2xl shadow-black/50",
          collapsed ? "w-20" : "w-72"
        )}
      >
        {/* Logo Section with Animation */}
        <div className="h-20 border-b border-white/10 flex items-center px-4 relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-r from-purple-600/20 via-blue-600/20 to-purple-600/20 animate-gradient-x" />
          <Link to="/" className="flex items-center gap-3 relative z-10 w-full group">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-purple-600 via-blue-600 to-indigo-600 flex items-center justify-center shadow-lg shadow-purple-500/30 group-hover:scale-110 transition-transform duration-300">
              <Sparkles className="h-6 w-6 text-white" />
            </div>
            {!collapsed && (
              <div className="flex-1">
                <span className="font-bold text-xl bg-gradient-to-r from-purple-400 via-blue-400 to-purple-400 bg-clip-text text-transparent">
                  MedAgentica
                </span>
                <div className="text-xs text-purple-400/70">AI Medical Assistant</div>
              </div>
            )}
          </Link>
        </div>

        {/* Toggle Button - Sidebar Collapse/Expand */}
        <div className="p-3 border-b border-white/10">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setCollapsed(!collapsed)}
            className="w-full hover:bg-white/10 text-purple-400 hover:text-purple-300 transition-all duration-300"
            title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
          >
            <Menu className="h-5 w-5" />
          </Button>
        </div>

        {/* Navigation Items with Premium Styling */}
        <nav className="flex-1 p-3 space-y-2 overflow-y-auto">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={cn(
                "group relative flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 overflow-hidden",
                isActive(item.path)
                  ? "bg-gradient-to-r from-purple-600/30 via-blue-600/30 to-purple-600/30 border border-purple-500/50 text-white shadow-lg shadow-purple-500/25"
                  : "hover:bg-white/5 border border-transparent text-gray-300 hover:text-white"
              )}
            >
              {/* Animated background gradient */}
              <div className="absolute inset-0 bg-gradient-to-r from-purple-600/0 via-blue-600/0 to-purple-600/0 group-hover:from-purple-600/10 group-hover:via-blue-600/10 group-hover:to-purple-600/10 transition-all duration-500" />
              
              <item.icon className={cn(
                "h-5 w-5 shrink-0 relative z-10 transition-transform duration-300",
                isActive(item.path) ? "text-purple-300" : "text-gray-400 group-hover:text-purple-400 group-hover:scale-110"
              )} />
              
              {!collapsed && (
                <div className="flex-1 min-w-0 relative z-10">
                  <div className="flex items-center justify-between">
                    <span className={cn(
                      "text-sm font-medium",
                      isActive(item.path) ? "text-white" : "text-gray-300"
                    )}>
                      {item.label}
                    </span>
                    {item.badge !== undefined && (
                      <Badge className="bg-purple-500/20 text-purple-300 border-purple-500/30 text-xs px-2 py-0">
                        {item.badge}
                      </Badge>
                    )}
                  </div>
                  {item.description && (
                    <div className="text-xs text-gray-500 mt-0.5">{item.description}</div>
                  )}
                </div>
              )}
            </Link>
          ))}
        </nav>

        {/* System Stats */}
        {!collapsed && (
          <div className="p-4 border-t border-white/10 space-y-2">
            <div className="text-xs font-semibold text-purple-400 uppercase tracking-wider mb-2">
              System Status
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-2 text-gray-400">
                  <Activity className="h-3 w-3 text-green-400" />
                  <span>Uptime</span>
                </div>
                <span className="text-green-400 font-semibold">{activeStats.uptime}</span>
              </div>
              <div className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-2 text-gray-400">
                  <Zap className="h-3 w-3 text-yellow-400" />
                  <span>Agents</span>
                </div>
                <span className="text-yellow-400 font-semibold">{activeStats.agents}</span>
              </div>
            </div>
          </div>
        )}

        {/* User Section with Premium Design */}
        <div className="p-4 border-t border-white/10">
          <div
            className={cn(
              "flex items-center gap-3 p-3 rounded-xl bg-gradient-to-r from-purple-900/30 via-blue-900/30 to-purple-900/30 border border-purple-500/20 backdrop-blur-md shadow-lg transition-all duration-300 hover:border-purple-500/40 hover:shadow-purple-500/20",
              collapsed && "justify-center"
            )}
          >
            <div className="h-10 w-10 rounded-full bg-gradient-to-br from-purple-500 via-pink-500 to-rose-500 flex items-center justify-center text-white font-bold text-sm shrink-0 shadow-lg shadow-pink-500/30 relative">
              <span>User</span>
              <div className="absolute -top-1 -right-1 h-3 w-3 bg-green-400 rounded-full border-2 border-slate-900" />
            </div>
            {!collapsed && (
              <div className="flex-1 min-w-0">
                <div className="text-sm font-semibold text-white truncate">Dr. User</div>
                <div className="text-xs text-purple-400/70 truncate">Licensed Clinician</div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Main Content with Premium Background */}
      <div className="flex-1 overflow-auto relative">
        {/* Animated background effects */}
        <div className="absolute inset-0 bg-gradient-to-br from-slate-950 via-purple-950/20 to-slate-950 pointer-events-none" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-purple-900/20 via-transparent to-transparent pointer-events-none" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_bottom_left,_var(--tw-gradient-stops))] from-blue-900/20 via-transparent to-transparent pointer-events-none" />
        
        {/* Content */}
        <div className="relative z-10 h-full">
          {children}
        </div>
      </div>
    </div>
  );
};

export default AppLayout;
