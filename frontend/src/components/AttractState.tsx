import React, { useState } from 'react';
import { Challenge, ChallengeCategory } from '../types';
import { Volume2, VolumeX, Sparkles, Clock, Compass, RefreshCw, ArrowRight, ShieldCheck, Footprints, Heart, Sun, Smile, Users, TreePine } from 'lucide-react';

interface AttractStateProps {
  challenge: Challenge | null;
  loading: boolean;
  onAccept: () => void;
  onRefresh: (category?: ChallengeCategory) => void;
  onSpeak: (text: string) => void;
  isSpeaking: boolean;
}

const CATEGORY_ICONS: Record<string, React.ReactNode> = {
  'Outdoor': <Footprints className="w-4 h-4 text-emerald-400" />,
  'Nature': <TreePine className="w-4 h-4 text-green-400" />,
  'Kindness': <Heart className="w-4 h-4 text-rose-400" />,
  'Happiness': <Smile className="w-4 h-4 text-amber-400" />,
  'Human Connection': <Users className="w-4 h-4 text-sky-400" />,
  'Community': <Compass className="w-4 h-4 text-indigo-400" />,
  'Health': <Sun className="w-4 h-4 text-orange-400" />,
  'Creativity': <Sparkles className="w-4 h-4 text-purple-400" />,
  'Exploration': <Compass className="w-4 h-4 text-teal-400" />
};

export const AttractState: React.FC<AttractStateProps> = ({
  challenge,
  loading,
  onAccept,
  onRefresh,
  onSpeak,
  isSpeaking
}) => {
  const [selectedCat, setSelectedCat] = useState<string>('All');

  if (loading || !challenge) {
    return (
      <div className="flex flex-col items-center justify-center py-24 space-y-4">
        <div className="w-14 h-14 rounded-2xl bg-emerald-950/80 border border-emerald-600/40 flex items-center justify-center animate-spin">
          <RefreshCw className="w-6 h-6 text-emerald-400" />
        </div>
        <p className="text-emerald-300 font-medium text-sm animate-pulse">
          Gemma Agent is analyzing memory & crafting your mission...
        </p>
      </div>
    );
  }

  const categoryIcon = CATEGORY_ICONS[challenge.category] || <Compass className="w-4 h-4 text-emerald-400" />;

  return (
    <div className="w-full max-w-2xl mx-auto space-y-6 pt-2 pb-12 animate-in fade-in duration-500">
      {/* Category Filter Pills */}
      <div className="flex items-center space-x-2 overflow-x-auto pb-2 scrollbar-none px-1">
        {['All', 'Outdoor', 'Nature', 'Kindness', 'Happiness', 'Health', 'Community'].map((cat) => (
          <button
            key={cat}
            onClick={() => {
              setSelectedCat(cat);
              onRefresh(cat === 'All' ? undefined : (cat as ChallengeCategory));
            }}
            className={`px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition-all cursor-pointer ${
              selectedCat === cat
                ? 'bg-emerald-500 text-black shadow-md shadow-emerald-950'
                : 'bg-emerald-950/50 text-emerald-300/80 hover:text-emerald-100 hover:bg-emerald-900/60 border border-emerald-800/40'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Main Mission Card */}
      <div className="relative rounded-3xl bg-gradient-to-b from-[#13241b] to-[#0d1712] border border-emerald-700/40 shadow-2xl p-6 sm:p-8 overflow-hidden">
        {/* Glow Accent */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />

        {/* Card Header Tag */}
        <div className="flex items-center justify-between gap-2 mb-6">
          <div className="flex items-center space-x-2 bg-emerald-950/90 border border-emerald-600/40 px-3 py-1.5 rounded-xl text-xs font-bold text-emerald-300">
            {categoryIcon}
            <span className="tracking-wide">{challenge.category.toUpperCase()}</span>
          </div>

          <div className="flex items-center space-x-2">
            <span className="flex items-center space-x-1 text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40 px-3 py-1 rounded-full">
              <Sparkles className="w-3.5 h-3.5 text-amber-400" />
              <span>+{challenge.xp_reward} XP</span>
            </span>

            <span className="flex items-center space-x-1 text-xs font-medium text-emerald-400/80 bg-emerald-950/60 border border-emerald-800/40 px-2.5 py-1 rounded-full">
              <Clock className="w-3 h-3 text-emerald-400" />
              <span>~{challenge.time_estimate_minutes}m</span>
            </span>
          </div>
        </div>

        {/* Mission Content */}
        <div className="space-y-4 mb-8">
          <div className="text-xs uppercase tracking-widest font-bold text-emerald-400/90">
            Today's Mission
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-emerald-50 leading-tight tracking-tight">
            {challenge.title}
          </h1>
          <p className="text-emerald-200/90 text-sm sm:text-base leading-relaxed font-normal">
            {challenge.description}
          </p>
        </div>

        {/* Audio Narration Bar */}
        <div className="bg-[#09120c]/80 border border-emerald-800/50 rounded-2xl p-4 mb-8 flex items-center justify-between gap-4">
          <div className="flex items-center space-x-3">
            <button
              onClick={() => onSpeak(challenge.spoken_intro)}
              aria-label={isSpeaking ? "Pause Voice Narration" : "Play Voice Narration"}
              className={`w-11 h-11 rounded-xl flex items-center justify-center cursor-pointer transition-all ${
                isSpeaking
                  ? 'bg-amber-500 text-black shadow-lg shadow-amber-950 animate-pulse'
                  : 'bg-emerald-600 text-white hover:bg-emerald-500 shadow-md shadow-emerald-950'
              }`}
            >
              {isSpeaking ? <VolumeX className="w-5 h-5" /> : <Volume2 className="w-5 h-5" />}
            </button>
            <div className="flex flex-col">
              <span className="text-xs font-bold text-emerald-300 flex items-center space-x-1.5">
                <span>ElevenLabs Agent Voice</span>
                {isSpeaking && (
                  <span className="flex space-x-0.5 items-end h-3">
                    <span className="w-1 bg-amber-400 h-2 animate-bounce rounded-full" />
                    <span className="w-1 bg-amber-400 h-3 animate-bounce delay-100 rounded-full" />
                    <span className="w-1 bg-amber-400 h-1.5 animate-bounce delay-200 rounded-full" />
                  </span>
                )}
              </span>
              <span className="text-[11px] text-emerald-400/70 italic line-clamp-1">
                "{challenge.spoken_intro}"
              </span>
            </div>
          </div>

          <button
            onClick={() => onRefresh(selectedCat === 'All' ? undefined : (selectedCat as ChallengeCategory))}
            className="p-2.5 rounded-xl bg-emerald-950/60 hover:bg-emerald-900/60 text-emerald-400 border border-emerald-800/40 cursor-pointer transition-all"
            title="Ask Gemma for a different mission"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>

        {/* Safety Note */}
        <div className="flex items-center space-x-2 text-[11px] text-emerald-400/70 mb-6 bg-emerald-950/30 px-3 py-2 rounded-lg border border-emerald-900/30">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-500 shrink-0" />
          <span>{challenge.safety_notes}</span>
        </div>

        {/* Primary Action Button: I'M IN */}
        <button
          onClick={onAccept}
          className="w-full py-4 px-6 rounded-2xl bg-gradient-to-r from-emerald-500 to-green-600 hover:from-emerald-400 hover:to-green-500 text-black font-extrabold text-base tracking-wide flex items-center justify-center space-x-2.5 shadow-xl shadow-emerald-950/80 transition-all cursor-pointer transform active:scale-[0.99]"
        >
          <span>I'M IN — LET'S GO OUTSIDE</span>
          <ArrowRight className="w-5 h-5" />
        </button>
      </div>

      {/* Philosophy Footnote */}
      <p className="text-center text-xs text-emerald-400/60 font-medium">
        Principle: TouchGrass succeeds when you stop using it. Leave this screen behind.
      </p>
    </div>
  );
};
