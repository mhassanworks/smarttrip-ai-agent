import React from "react";
import { useDarkMode } from "../hooks/useDarkMode";

export type DashboardTab =
  | "overview"
  | "trip-planner"
  | "peas"
  | "rules"
  | "negotiation"
  | "utility"
  | "bdi"
  | "knowledge"
  | "socket"
  | "security"
  | "workers"
  | "demo";

interface HeaderProps {
  activeTab: DashboardTab;
  onTabChange: (tab: DashboardTab) => void;
  onLaunchDemo: () => void;
}

export const Header: React.FC<HeaderProps> = ({ activeTab, onTabChange, onLaunchDemo }) => {
  const { isDark, toggle } = useDarkMode();

  const navItems: Array<{ id: DashboardTab; label: string; badge?: string }> = [
    { id: "overview", label: "Overview" },
    { id: "trip-planner", label: "Trip Planner" },
    { id: "peas", label: "PEAS Matrix" },
    { id: "rules", label: "Rule Engine" },
    { id: "negotiation", label: "Negotiation" },
    { id: "utility", label: "Utility (10)" },
    { id: "bdi", label: "BDI Planner" },
    { id: "knowledge", label: "Weather & Knowledge" },
    { id: "socket", label: "TCP Sockets" },
    { id: "security", label: "Security & HMAC" },
    { id: "workers", label: "Workers & Latency" },
    { id: "demo", label: "Demo Mode", badge: "LIVE" },
  ];

  return (
    <header className="bg-slate-950/95 backdrop-blur-md w-full sticky top-0 border-b border-slate-800/80 shadow-lg z-50">
      {/* Top Bar */}
      <div className="max-w-[1536px] mx-auto px-4 sm:px-6 h-16 flex items-center justify-between gap-4">
        {/* Brand */}
        <div
          onClick={() => onTabChange("overview")}
          className="flex items-center gap-3 cursor-pointer group"
        >
          <div className="h-9 w-9 rounded-xl bg-gradient-to-tr from-indigo-600 to-cyan-500 flex items-center justify-center text-white shadow-md shadow-indigo-500/30 group-hover:scale-105 transition-transform">
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-lg text-white tracking-tight group-hover:text-indigo-400 transition-colors">
                SmartTrip AI
              </span>
              <span className="hidden sm:inline-block px-2 py-0.5 text-[10px] font-bold rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 font-mono">
                AUTONOMOUS MAS
              </span>
            </div>
            <p className="text-[10px] text-slate-400 hidden sm:block -mt-0.5">
              Multi-Agent Planning & Negotiation
            </p>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-2.5">
          <button
            onClick={onLaunchDemo}
            className="hidden sm:inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-gradient-to-r from-indigo-500 to-cyan-500 hover:from-indigo-600 hover:to-cyan-600 text-white text-xs font-bold shadow-md shadow-indigo-500/25 transition-all cursor-pointer"
          >
            <span>&#9654;</span>
            <span>Run Demo</span>
          </button>

          <button
            onClick={() => onTabChange("trip-planner")}
            className="px-3.5 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold shadow-sm transition-all cursor-pointer"
          >
            New Trip Plan
          </button>

          <button
            onClick={toggle}
            className="w-8 h-8 rounded-lg flex items-center justify-center text-slate-400 hover:text-white hover:bg-slate-800 transition-colors cursor-pointer"
            title="Toggle theme"
          >
            {isDark ? "☀️" : "🌙"}
          </button>
        </div>
      </div>

      {/* Navigation Sub-bar */}
      <div className="border-t border-slate-900 bg-slate-950/70">
        <div className="max-w-[1536px] mx-auto px-4 sm:px-6">
          <nav className="flex items-center gap-1 overflow-x-auto py-2 scrollbar-none text-xs font-medium">
            {navItems.map((item) => {
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => onTabChange(item.id)}
                  className={`px-3 py-1.5 rounded-lg whitespace-nowrap transition-all flex items-center gap-1.5 cursor-pointer ${
                    isActive
                      ? "bg-indigo-600/20 text-indigo-300 font-bold border border-indigo-500/40 shadow-sm"
                      : "text-slate-400 hover:text-slate-200 hover:bg-slate-900"
                  }`}
                >
                  <span>{item.label}</span>
                  {item.badge && (
                    <span className="px-1.5 py-0.2 rounded text-[9px] font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>
        </div>
      </div>
    </header>
  );
};
