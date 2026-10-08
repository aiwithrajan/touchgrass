import React, { useState } from 'react';
import { JourneyCardData, UserContext } from '../types';
import { Map, Share2, Check, Sparkles, Trophy, Award, Lock } from 'lucide-react';

interface JourneyViewProps {
  user: UserContext;
  journeyData: JourneyCardData;
}

export const JourneyView: React.FC<JourneyViewProps> = ({ user, journeyData }) => {
  const [copied, setCopied] = useState<boolean>(false);

  const handleCopy = () => {
    const text = `🌱 MY TOUCHGRASS JOURNEY\nLevel ${user.level} | ${user.completed_challenges_count} real-world outdoor missions completed.\n"Real life > Screen time."\n#TouchGrass #Hacktoberfest`;
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  const isLevel10 = user.level >= 10;

  return (
    <div className="w-full max-w-2xl mx-auto space-y-6 pt-2 pb-12 animate-in fade-in duration-500">
      {/* Banner if below Level 10 */}
      {!isLevel10 && (
        <div className="rounded-2xl bg-amber-500/10 border border-amber-500/30 p-4 flex items-center justify-between gap-3 text-xs text-amber-200">
          <div className="flex items-center space-x-2.5">
            <Lock className="w-4 h-4 text-amber-400 shrink-0" />
            <span>
              <strong>Journey Card Milestone:</strong> Official verified badges lock until <span className="underline font-bold">Level 10</span>, but you can preview and share your progress anytime!
            </span>
          </div>
          <span className="font-mono bg-amber-500/20 px-2 py-1 rounded text-[11px] font-bold shrink-0">
            {user.level}/10 LVL
          </span>
        </div>
      )}

      {/* Shareable Card Canvas */}
      <div className="rounded-3xl bg-gradient-to-br from-[#122b1e] via-[#0d1d15] to-[#09140e] border border-emerald-600/50 p-6 sm:p-8 shadow-2xl space-y-6 relative overflow-hidden">
        {/* Glow */}
        <div className="absolute top-0 right-0 w-72 h-72 bg-emerald-500/15 rounded-full blur-3xl pointer-events-none" />

        {/* Header */}
        <div className="flex items-center justify-between border-b border-emerald-800/40 pb-5">
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-emerald-500 to-green-700 flex items-center justify-center text-2xl shadow-lg shadow-emerald-950">
              🌱
            </div>
            <div>
              <div className="text-xs uppercase font-extrabold tracking-widest text-emerald-400">
                Official Journey Card
              </div>
              <h2 className="text-xl sm:text-2xl font-black text-white tracking-tight">
                {user.username}
              </h2>
            </div>
          </div>

          <div className="text-right">
            <span className="text-2xl font-black text-amber-400">LVL {user.level}</span>
            <div className="text-[11px] font-semibold text-emerald-300/80">
              {user.completed_challenges_count} Missions Completed
            </div>
          </div>
        </div>

        {/* Categories Breakdown Grid */}
        <div className="space-y-2.5">
          <span className="text-xs font-bold tracking-wider uppercase text-emerald-400/90">
            Real-World Impact Breakdown
          </span>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
            {Object.entries(journeyData.categories_breakdown).map(([cat, count]) => (
              <div
                key={cat}
                className="bg-[#0a1610]/80 border border-emerald-800/40 rounded-xl p-3 flex items-center justify-between"
              >
                <span className="text-xs font-medium text-emerald-200">{cat}</span>
                <span className="text-xs font-bold text-amber-400 bg-emerald-950 px-2 py-0.5 rounded-md border border-emerald-800/40">
                  {count}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Badges Earned */}
        <div className="space-y-2.5">
          <span className="text-xs font-bold tracking-wider uppercase text-emerald-400/90">
            Badges Earned
          </span>
          <div className="flex flex-wrap gap-2">
            {journeyData.badges_earned.length > 0 ? (
              journeyData.badges_earned.map((b) => (
                <div
                  key={b.id}
                  className="flex items-center space-x-1.5 bg-emerald-950/90 border border-emerald-700/50 px-3 py-1.5 rounded-xl text-xs font-bold text-emerald-200"
                >
                  <span>{b.icon}</span>
                  <span>{b.title}</span>
                </div>
              ))
            ) : (
              <div className="text-xs text-emerald-400/60 italic">
                Complete your first mission to earn badges like 🌱 Earth Helper and 🤝 Good Human.
              </div>
            )}
          </div>
        </div>

        {/* Real Things I Did Quotes */}
        <div className="space-y-2.5">
          <span className="text-xs font-bold tracking-wider uppercase text-emerald-400/90">
            Real Things I Did
          </span>
          <div className="space-y-2">
            {journeyData.notable_quotes.map((q, idx) => (
              <div
                key={idx}
                className="bg-[#08120c]/70 border border-emerald-800/30 rounded-xl p-3 text-xs text-emerald-200/90 italic"
              >
                {q}
              </div>
            ))}
          </div>
        </div>

        {/* Bottom card footer */}
        <div className="pt-3 border-t border-emerald-800/40 flex items-center justify-between text-[11px] text-emerald-400/70 font-mono">
          <span>Powered by Gemma 2 AI</span>
          <span>touchgrass.app</span>
        </div>
      </div>

      {/* Share / Copy Action */}
      <button
        onClick={handleCopy}
        className="w-full py-4 px-6 rounded-2xl bg-emerald-600 hover:bg-emerald-500 text-white font-extrabold text-sm flex items-center justify-center space-x-2 shadow-xl shadow-emerald-950/80 transition-all cursor-pointer transform active:scale-[0.99]"
      >
        {copied ? (
          <>
            <Check className="w-4 h-4 text-amber-300" />
            <span>COPIED TO CLIPBOARD!</span>
          </>
        ) : (
          <>
            <Share2 className="w-4 h-4" />
            <span>SHARE YOUR REAL-WORLD JOURNEY</span>
          </>
        )}
      </button>
    </div>
  );
};
