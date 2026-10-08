import React, { useState } from 'react';
import { SocialPost } from '../types';
import { Lock, Users, ShieldCheck, Heart, Sparkles, MapPin, CheckCircle2 } from 'lucide-react';

interface SocialModeProps {
  unlocked: boolean;
  requiredLevel: number;
  currentLevel: number;
  feed: SocialPost[];
}

export const SocialMode: React.FC<SocialModeProps> = ({
  unlocked,
  requiredLevel,
  currentLevel,
  feed
}) => {
  const [posts, setPosts] = useState<SocialPost[]>(feed);

  const handleKudos = (id: string) => {
    setPosts(prev => prev.map(p => {
      if (p.id === id) {
        return { ...p, kudos_count: p.kudos_count + 1 };
      }
      return p;
    }));
  };

  if (!unlocked) {
    const percent = Math.min(100, Math.round((currentLevel / requiredLevel) * 100));

    return (
      <div className="w-full max-w-xl mx-auto py-12 px-6 text-center space-y-6">
        <div className="w-20 h-20 mx-auto rounded-3xl bg-emerald-950/80 border border-emerald-600/40 flex items-center justify-center shadow-xl shadow-emerald-950/60">
          <Lock className="w-9 h-9 text-amber-400" />
        </div>

        <div className="space-y-2">
          <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            SOCIAL MODE LOCKED
          </h2>
          <p className="text-emerald-300/80 text-sm max-w-md mx-auto">
            Social connections unlock at <span className="font-bold text-amber-400">Level {requiredLevel}</span>. We prioritize personal real-world grounding before social features.
          </p>
        </div>

        {/* Level Progression Progress Bar */}
        <div className="bg-[#0f1f16] border border-emerald-800/40 p-5 rounded-2xl max-w-sm mx-auto space-y-3">
          <div className="flex justify-between text-xs font-bold text-emerald-300">
            <span>Your Progress: Level {currentLevel}</span>
            <span className="text-amber-400">Target: Level {requiredLevel}</span>
          </div>
          <div className="w-full bg-emerald-950 rounded-full h-3 overflow-hidden border border-emerald-800">
            <div
              className="bg-gradient-to-r from-emerald-500 to-amber-400 h-full transition-all duration-500"
              style={{ width: `${percent}%` }}
            />
          </div>
          <p className="text-[11px] text-emerald-500/80 italic">
            Complete a few more missions outside to unlock community challenges.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full max-w-2xl mx-auto space-y-6 pt-2 pb-12 animate-in fade-in duration-500">
      {/* Unlocked Header */}
      <div className="rounded-2xl bg-gradient-to-r from-emerald-950/80 to-[#102419] border border-emerald-700/40 p-5 flex items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-300">
            <Users className="w-5 h-5 text-emerald-400" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h2 className="text-base font-bold text-emerald-50">Community Feed</h2>
              <span className="text-[10px] bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-2 py-0.5 rounded-full font-bold">
                UNLOCKED
              </span>
            </div>
            <p className="text-xs text-emerald-300/70">
              People who also choose real-world action over endless screen feeds.
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-1 text-[11px] text-emerald-400 bg-emerald-950/80 px-2.5 py-1 rounded-lg border border-emerald-800/40">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" />
          <span>Approx city only</span>
        </div>
      </div>

      {/* Feed List */}
      <div className="space-y-4">
        {posts.map((post) => (
          <div
            key={post.id}
            className="rounded-2xl bg-[#0f1d16] border border-emerald-800/40 p-5 space-y-3.5 shadow-lg hover:border-emerald-700/60 transition-colors"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2.5">
                <div className="w-8 h-8 rounded-full bg-emerald-800/60 border border-emerald-600/40 flex items-center justify-center text-xs font-bold text-emerald-200">
                  {post.author_name[0]}
                </div>
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="text-xs font-bold text-emerald-100">{post.author_name}</span>
                    <span className="text-[10px] bg-emerald-950 text-emerald-400 border border-emerald-800/60 px-1.5 py-0.2 rounded font-mono">
                      LVL {post.author_level}
                    </span>
                  </div>
                  <div className="flex items-center space-x-1 text-[11px] text-emerald-500/80">
                    <MapPin className="w-3 h-3" />
                    <span>{post.broad_location}</span>
                    <span>•</span>
                    <span>{post.time_ago}</span>
                  </div>
                </div>
              </div>

              <span className="text-[11px] font-bold text-emerald-400/90 bg-emerald-950/80 px-2.5 py-1 rounded-full border border-emerald-800/50">
                {post.category}
              </span>
            </div>

            {/* Post Content */}
            <div className="bg-[#09130d] rounded-xl p-3.5 border border-emerald-900/40 space-y-1.5">
              <div className="text-xs font-semibold text-emerald-300 flex items-center space-x-1.5">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                <span>Mission: "{post.challenge_title}"</span>
              </div>
              <p className="text-xs text-emerald-200/80 leading-relaxed italic">
                "{post.reflection}"
              </p>
            </div>

            {/* Kudos Button */}
            <div className="flex items-center justify-between pt-1 text-xs">
              <button
                onClick={() => handleKudos(post.id)}
                className="flex items-center space-x-1.5 text-emerald-400 hover:text-emerald-200 bg-emerald-950/60 hover:bg-emerald-900/60 px-3 py-1.5 rounded-xl border border-emerald-800/30 transition-colors cursor-pointer"
              >
                <Heart className="w-3.5 h-3.5 fill-emerald-500 text-emerald-500" />
                <span>{post.kudos_count} Kudos</span>
              </button>

              <span className="text-[11px] text-emerald-500/60">
                Verified Outdoor Action ✓
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
