import React from 'react';
import { UserContext } from '../types';
import { Sparkles, Flame, Wifi, WifiOff, ShieldCheck, Compass, Users, Map, Activity } from 'lucide-react';

interface HeaderProps {
  user: UserContext;
  activeTab: 'mission' | 'social' | 'journey' | 'traces';
  setActiveTab: (tab: 'mission' | 'social' | 'journey' | 'traces') => void;
  onToggleOffline: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  user,
  activeTab,
  setActiveTab,
  onToggleOffline
}) => {
  const xpPercent = Math.min(100, Math.round((user.xp / user.xp_to_next_level) * 100));

  return (
    <header className="sticky top-0 z-40 bg-[#0d1611]/90 backdrop-blur-md border-b border-emerald-900/40 px-4 py-3 sm:px-6">
      <div className="max-w-5xl mx-auto flex flex-col md:flex-row md:items-center md:justify-between gap-3">
        {/* Brand */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2.5">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-green-700 flex items-center justify-center shadow-lg shadow-emerald-950/50">
              <span className="text-xl">🌱</span>
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-extrabold tracking-tight text-xl text-emerald-50">TOUCHGRASS</span>
                <span className="text-[10px] uppercase tracking-wider font-semibold bg-emerald-900/60 text-emerald-400 border border-emerald-700/50 px-2 py-0.5 rounded-full">
                  Gemma 2 Agent
                </span>
              </div>
              <p className="text-xs text-emerald-400/80 font-medium hidden sm:block">
                The app that succeeds when you stop using it
              </p>
            </div>
          </div>

          {/* Mobile Offline Toggle */}
          <button
            onClick={onToggleOffline}
            className={`md:hidden flex items-center space-x-1 px-2.5 py-1.5 rounded-full text-xs font-semibold transition-all ${
              user.offline_mode
                ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40'
                : 'bg-emerald-950/60 text-emerald-300 border border-emerald-800/40'
            }`}
          >
            {user.offline_mode ? <WifiOff className="w-3.5 h-3.5 text-amber-400" /> : <Wifi className="w-3.5 h-3.5 text-emerald-400" />}
            <span>{user.offline_mode ? 'Offline' : 'Online'}</span>
          </button>
        </div>

        {/* Stats & Actions */}
        <div className="flex items-center justify-between md:justify-end space-x-4">
          {/* XP & Level progress */}
          <div className="flex items-center space-x-3 bg-emerald-950/40 border border-emerald-800/40 px-3.5 py-1.5 rounded-xl">
            <div className="flex items-center space-x-1.5">
              <span className="text-xs font-bold bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded-md border border-emerald-500/30">
                LVL {user.level}
              </span>
              <div className="w-24 bg-emerald-950 rounded-full h-2 overflow-hidden border border-emerald-800/60">
                <div
                  className="bg-gradient-to-r from-emerald-500 to-amber-400 h-full transition-all duration-500"
                  style={{ width: `${xpPercent}%` }}
                />
              </div>
              <span className="text-[11px] font-mono text-emerald-400">
                {user.xp}/{user.xp_to_next_level} XP
              </span>
            </div>

            <div className="flex items-center space-x-1 text-amber-400 text-xs font-bold pl-2 border-l border-emerald-800/50">
              <Flame className="w-3.5 h-3.5 fill-amber-400" />
              <span>{user.streak_days}d</span>
            </div>
          </div>

          {/* Desktop Offline Mode Switch */}
          <button
            onClick={onToggleOffline}
            title={user.offline_mode ? "Simulating Trail Mode (No internet, 100% on-device Gemma inference)" : "Cloud Sync Mode active"}
            className={`hidden md:flex items-center space-x-1.5 px-3 py-1.5 rounded-full text-xs font-semibold cursor-pointer transition-all shadow-sm ${
              user.offline_mode
                ? 'bg-amber-500/20 text-amber-300 border border-amber-500/50 hover:bg-amber-500/30'
                : 'bg-emerald-900/40 text-emerald-300 border border-emerald-700/40 hover:bg-emerald-900/60'
            }`}
          >
            {user.offline_mode ? <WifiOff className="w-3.5 h-3.5 text-amber-400" /> : <Wifi className="w-3.5 h-3.5 text-emerald-400" />}
            <span>{user.offline_mode ? 'Airplane Trail Mode' : 'Cloud Sync'}</span>
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="max-w-5xl mx-auto flex items-center space-x-1 mt-2.5 pt-1.5 border-t border-emerald-900/30 text-xs font-medium">
        <button
          onClick={() => setActiveTab('mission')}
          className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg transition-all cursor-pointer ${
            activeTab === 'mission'
              ? 'bg-emerald-600 text-white font-semibold shadow-sm'
              : 'text-emerald-300/70 hover:text-emerald-100 hover:bg-emerald-950/40'
          }`}
        >
          <Compass className="w-3.5 h-3.5" />
          <span>Mission</span>
        </button>

        <button
          onClick={() => setActiveTab('social')}
          className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg transition-all cursor-pointer ${
            activeTab === 'social'
              ? 'bg-emerald-600 text-white font-semibold shadow-sm'
              : 'text-emerald-300/70 hover:text-emerald-100 hover:bg-emerald-950/40'
          }`}
        >
          <Users className="w-3.5 h-3.5" />
          <span>Social Mode</span>
          {user.level < 5 && (
            <span className="text-[10px] bg-emerald-950/80 text-amber-400 border border-amber-500/30 px-1.5 py-0.2 rounded font-mono">
              Lv 5
            </span>
          )}
        </button>

        <button
          onClick={() => setActiveTab('journey')}
          className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg transition-all cursor-pointer ${
            activeTab === 'journey'
              ? 'bg-emerald-600 text-white font-semibold shadow-sm'
              : 'text-emerald-300/70 hover:text-emerald-100 hover:bg-emerald-950/40'
          }`}
        >
          <Map className="w-3.5 h-3.5" />
          <span>Journey Card</span>
          {user.level < 10 && (
            <span className="text-[10px] bg-emerald-950/80 text-emerald-400/80 border border-emerald-700/30 px-1.5 py-0.2 rounded font-mono">
              Lv 10
            </span>
          )}
        </button>

        <button
          onClick={() => setActiveTab('traces')}
          className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg transition-all cursor-pointer ${
            activeTab === 'traces'
              ? 'bg-emerald-600 text-white font-semibold shadow-sm'
              : 'text-emerald-300/70 hover:text-emerald-100 hover:bg-emerald-950/40'
          }`}
        >
          <Activity className="w-3.5 h-3.5" />
          <span>Agent Traces</span>
        </button>
      </div>
    </header>
  );
};
