import React, { useState, useEffect } from 'react';
import { Challenge } from '../types';
import { CheckCircle, Clock, ArrowLeft, EyeOff } from 'lucide-react';

interface ReleaseStateProps {
  challenge: Challenge;
  onComplete: (minutes: number) => void;
  onCancel: () => void;
}

export const ReleaseState: React.FC<ReleaseStateProps> = ({
  challenge,
  onComplete,
  onCancel
}) => {
  const [secondsElapsed, setSecondsElapsed] = useState<number>(0);
  const [dimScreen, setDimScreen] = useState<boolean>(false);

  useEffect(() => {
    const timer = setInterval(() => {
      setSecondsElapsed((prev) => prev + 1);
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const minutes = Math.floor(secondsElapsed / 60);
  const seconds = secondsElapsed % 60;
  const formattedTime = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

  return (
    <div className={`relative min-h-[75vh] flex flex-col items-center justify-between py-12 px-6 rounded-3xl transition-all duration-700 ${
      dimScreen ? 'bg-black/95 opacity-50' : 'zen-ambient border border-emerald-900/30'
    }`}>
      {/* Top minimal status */}
      <div className="w-full flex items-center justify-between text-xs text-emerald-500/70">
        <button
          onClick={onCancel}
          className="flex items-center space-x-1.5 hover:text-emerald-300 transition-colors cursor-pointer py-1 px-2.5 rounded-lg bg-emerald-950/40"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Abandon mission</span>
        </button>

        <button
          onClick={() => setDimScreen(!dimScreen)}
          className="flex items-center space-x-1.5 hover:text-emerald-300 transition-colors cursor-pointer py-1 px-2.5 rounded-lg bg-emerald-950/40"
        >
          <EyeOff className="w-3.5 h-3.5" />
          <span>{dimScreen ? 'Wake screen' : 'Dim screen'}</span>
        </button>
      </div>

      {/* Center Zen Focus Element */}
      <div className="flex flex-col items-center text-center space-y-8 my-auto max-w-lg">
        {/* Breathing Circle */}
        <div className="relative flex items-center justify-center">
          <div className="w-40 h-40 sm:w-48 sm:h-48 rounded-full border border-emerald-500/20 animate-ping absolute opacity-20" />
          <div className="w-32 h-32 sm:w-36 sm:h-36 rounded-full bg-emerald-500/10 border border-emerald-500/40 animate-pulse-subtle flex items-center justify-center backdrop-blur-sm">
            <div className="text-center">
              <span className="text-2xl sm:text-3xl font-mono font-bold text-emerald-300">
                {formattedTime}
              </span>
              <span className="block text-[10px] uppercase font-bold tracking-widest text-emerald-400/70 mt-1">
                OUTSIDE
              </span>
            </div>
          </div>
        </div>

        {/* The Zen Mantra */}
        <div className="space-y-3">
          <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-emerald-100 uppercase">
            YOU'RE OUTSIDE.
            <br />
            <span className="text-emerald-400">GO DO IT.</span>
          </h1>
          <p className="text-lg font-medium text-emerald-200/80">
            You don't need this screen.
          </p>
        </div>

        {/* Minimal Mission Reminder */}
        <div className="bg-emerald-950/40 border border-emerald-800/30 px-5 py-3 rounded-2xl text-xs text-emerald-300/90 font-medium">
          <span className="text-emerald-400 font-bold">Mission:</span> {challenge.title}
        </div>
      </div>

      {/* Bottom return action */}
      <div className="w-full max-w-md space-y-3">
        <button
          onClick={() => onComplete(Math.max(1, Math.round(secondsElapsed / 60)))}
          className="w-full py-4 px-6 rounded-2xl bg-gradient-to-r from-emerald-500 to-green-600 hover:from-emerald-400 hover:to-green-500 text-black font-extrabold text-base tracking-wide flex items-center justify-center space-x-2 shadow-2xl shadow-emerald-950/90 transition-all cursor-pointer transform active:scale-[0.98]"
        >
          <CheckCircle className="w-5 h-5" />
          <span>I'M BACK — I DID IT</span>
        </button>

        <p className="text-center text-[11px] text-emerald-500/60 font-medium">
          TouchGrass succeeds when you stop using it. Put your phone in your pocket.
        </p>
      </div>
    </div>
  );
};
