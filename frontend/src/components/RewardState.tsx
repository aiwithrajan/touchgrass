import React, { useState, useEffect } from 'react';
import confetti from 'canvas-confetti';
import { Challenge, RewardResult } from '../types';
import { Sparkles, Trophy, Award, Mic, Send, ArrowRight, CheckCircle2, MessageSquare, Unlock } from 'lucide-react';

interface RewardStateProps {
  challenge: Challenge;
  rewardResult: RewardResult | null;
  onSubmitReflection: (text: string) => Promise<void>;
  onNextMission: () => void;
  submitting: boolean;
}

export const RewardState: React.FC<RewardStateProps> = ({
  challenge,
  rewardResult,
  onSubmitReflection,
  onNextMission,
  submitting
}) => {
  const [reflection, setReflection] = useState<string>('');
  const [isRecording, setIsRecording] = useState<boolean>(false);

  useEffect(() => {
    // High-energy celebratory confetti burst on arrival
    try {
      confetti({
        particleCount: 80,
        spread: 70,
        origin: { y: 0.6 },
        colors: ['#10B981', '#F59E0B', '#34D399', '#FBBF24']
      });
    } catch (e) {}
  }, []);

  // Voice speech-to-text reflection support
  const handleVoiceInput = () => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Speech recognition isn't supported in this browser. Please type your reflection.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;

    recognition.onstart = () => setIsRecording(true);
    recognition.onend = () => setIsRecording(false);
    recognition.onerror = () => setIsRecording(false);

    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      setReflection((prev) => (prev ? `${prev} ${transcript}` : transcript));
    };

    recognition.start();
  };

  const sampleReflections = [
    "I helped my neighbor carry groceries and we talked about mountain routes.",
    "Walked 20 minutes without headphones; heard cardinals and felt the autumn breeze.",
    "Found three distinct tree barks near the trail and sat in the quiet air."
  ];

  return (
    <div className="w-full max-w-2xl mx-auto space-y-6 pt-2 pb-12 animate-in zoom-in-95 duration-500">
      {/* Celebration Banner */}
      <div className="rounded-3xl bg-gradient-to-br from-[#163323] via-[#0f2418] to-[#0a1710] border border-emerald-500/40 p-6 sm:p-8 text-center space-y-4 shadow-2xl relative overflow-hidden">
        <div className="inline-flex items-center space-x-2 bg-emerald-500/20 border border-emerald-400/40 px-3.5 py-1.5 rounded-full text-emerald-300 font-bold text-xs">
          <Sparkles className="w-3.5 h-3.5 text-amber-400 animate-spin" />
          <span>MISSION ACCOMPLISHED</span>
        </div>

        <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          YOU TOUCHED GRASS.
        </h1>
        <p className="text-emerald-200/90 text-sm max-w-md mx-auto">
          Completed: <span className="font-semibold text-emerald-300">"{challenge.title}"</span>
        </p>

        {/* XP Gain Pill */}
        <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-amber-500/20 to-emerald-500/20 border border-amber-500/40 px-6 py-2.5 rounded-2xl text-amber-300 font-black text-lg shadow-inner">
          <Sparkles className="w-5 h-5 text-amber-400" />
          <span>+{rewardResult ? rewardResult.total_xp_awarded : challenge.xp_reward} XP EARNED</span>
        </div>

        {/* Level Up Banner */}
        {rewardResult?.level_up && (
          <div className="mt-4 p-4 rounded-2xl bg-gradient-to-r from-amber-500/30 to-emerald-500/30 border border-amber-400/60 flex items-center justify-center space-x-3 text-amber-200 animate-bounce">
            <Trophy className="w-6 h-6 text-amber-400" />
            <span className="font-extrabold text-sm sm:text-base">
              LEVEL UP! You reached Level {rewardResult.new_level}!
            </span>
          </div>
        )}

        {/* Milestone Unlocks */}
        {rewardResult?.unlocked_features && rewardResult.unlocked_features.length > 0 && (
          <div className="mt-2 p-3 rounded-xl bg-emerald-900/40 border border-emerald-600/40 flex items-center justify-center space-x-2 text-xs font-bold text-emerald-300">
            <Unlock className="w-4 h-4 text-emerald-400" />
            <span>Unlocked: {rewardResult.unlocked_features.map(f => f.replace('_', ' ').toUpperCase()).join(', ')}</span>
          </div>
        )}

        {/* Badge Unlocks */}
        {rewardResult?.new_badges && rewardResult.new_badges.length > 0 && (
          <div className="mt-2 flex items-center justify-center space-x-2">
            {rewardResult.new_badges.map((b) => (
              <span key={b} className="flex items-center space-x-1.5 bg-amber-500/20 border border-amber-500/40 px-3 py-1.5 rounded-xl text-xs font-bold text-amber-300">
                <Award className="w-4 h-4 text-amber-400" />
                <span>New Badge: {b.replace('_', ' ').toUpperCase()}</span>
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Reflection Input Form */}
      <div className="rounded-3xl bg-[#0f1d16] border border-emerald-800/40 p-6 space-y-4 shadow-xl">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2 text-emerald-300 font-bold text-sm">
            <MessageSquare className="w-4 h-4 text-emerald-400" />
            <span>Voice / Text Reflection</span>
          </div>
          <span className="text-[11px] text-emerald-400/70 font-semibold bg-emerald-950 px-2 py-0.5 rounded-md border border-emerald-800/40">
            Gemma AI Evaluation
          </span>
        </div>

        <p className="text-xs text-emerald-300/80 leading-relaxed">
          What happened while you were outside? Share a quick sentence to earn bonus XP and teach your Gemma Agent.
        </p>

        {/* Textbox & Mic */}
        <div className="relative">
          <textarea
            value={reflection}
            onChange={(e) => setReflection(e.target.value)}
            placeholder="e.g. I helped my neighbor carry groceries / I found an unusual weeping willow by the pond..."
            rows={3}
            className="w-full bg-[#09130d] border border-emerald-800/60 rounded-2xl p-4 text-sm text-emerald-100 placeholder-emerald-700/60 focus:outline-none focus:border-emerald-500 transition-colors"
          />

          <button
            onClick={handleVoiceInput}
            title="Speak reflection"
            className={`absolute bottom-3 right-3 p-2 rounded-xl transition-all cursor-pointer ${
              isRecording
                ? 'bg-rose-500 text-white animate-pulse'
                : 'bg-emerald-900/60 hover:bg-emerald-800/60 text-emerald-300 border border-emerald-700/40'
            }`}
          >
            <Mic className="w-4 h-4" />
          </button>
        </div>

        {/* Quick sample chips */}
        <div className="space-y-1.5">
          <span className="text-[10px] uppercase font-bold text-emerald-500/70 tracking-wider">
            Quick Examples:
          </span>
          <div className="flex flex-wrap gap-1.5">
            {sampleReflections.map((sample, idx) => (
              <button
                key={idx}
                onClick={() => setReflection(sample)}
                className="text-[11px] bg-emerald-950/60 hover:bg-emerald-900/60 text-emerald-300/80 border border-emerald-800/30 px-2.5 py-1 rounded-lg text-left transition-colors cursor-pointer"
              >
                "{sample.slice(0, 42)}..."
              </button>
            ))}
          </div>
        </div>

        {/* Submit or feedback */}
        {!rewardResult?.gemma_encouragement ? (
          <button
            onClick={() => onSubmitReflection(reflection)}
            disabled={submitting}
            className="w-full py-3.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white font-bold text-sm flex items-center justify-center space-x-2 shadow-lg shadow-emerald-950 cursor-pointer transition-all"
          >
            {submitting ? (
              <span>Gemma is evaluating reflection...</span>
            ) : (
              <>
                <Send className="w-4 h-4" />
                <span>Submit Reflection for Bonus XP</span>
              </>
            )}
          </button>
        ) : (
          <div className="p-4 rounded-2xl bg-emerald-950/70 border border-emerald-700/50 space-y-2 animate-in fade-in">
            <div className="flex items-center space-x-2 text-xs font-bold text-emerald-300">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>Gemma Evaluator Feedback (+{rewardResult.bonus_xp} Bonus XP)</span>
            </div>
            <p className="text-xs text-emerald-200/90 leading-relaxed italic">
              "{rewardResult.gemma_encouragement}"
            </p>
          </div>
        )}
      </div>

      {/* Next mission button */}
      <button
        onClick={onNextMission}
        className="w-full py-4 px-6 rounded-2xl bg-gradient-to-r from-emerald-500 to-green-600 hover:from-emerald-400 hover:to-green-500 text-black font-extrabold text-base tracking-wide flex items-center justify-center space-x-2 shadow-xl shadow-emerald-950/80 transition-all cursor-pointer transform active:scale-[0.99]"
      >
        <span>GET NEXT MISSION →</span>
      </button>
    </div>
  );
};
