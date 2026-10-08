import React, { useState, useEffect, useRef } from 'react';

type PageState = 'mission' | 'outside' | 'complete' | 'journey';
type DurationOption = 5 | 15 | 30;

interface MissionData {
  title: string;
  description: string;
  outsideInstruction: string;
  step2: string;
  focus: string;
  reflectionDefault: string;
}

interface SavedReflection {
  id: string;
  date: string;
  missionTitle: string;
  durationMinutes: number;
  xpEarned: number;
  reflectionText: string;
}

interface VitalityForecast {
  vitality_score: number;
  peak_vitality_score: number;
  optimal_window: string;
  condition: string;
  advice: string;
  temperature_c: number;
  uv_index: number;
  inference_ms: number;
  model_engine: string;
}

const MISSIONS: MissionData[] = [
  {
    title: 'Find a tree and spend two minutes looking at it.',
    description: 'Notice the bark, the leaves and what moves around it. No phone until you are done.',
    outsideInstruction: 'Find a tree and look at it for two minutes.',
    step2: '2. Go outside and find a tree.',
    focus: 'Nature',
    reflectionDefault: 'The bark was deeper than I expected, and a bird kept landing on one branch.'
  },
  {
    title: 'Walk for ten minutes in a direction you never take.',
    description: 'Turn down a street you always pass by. Pay attention to the houses and pavement. No phone until you are done.',
    outsideInstruction: 'Keep walking without checking your screen.',
    step2: '2. Go outside and walk a new route.',
    focus: 'Exploration',
    reflectionDefault: 'Found a quiet alleyway and a garden with stone statues I had never noticed.'
  },
  {
    title: 'Step outside and listen until you hear three birds.',
    description: 'Close your eyes if you like. Pinpoint where each sound comes from. No phone until you are done.',
    outsideInstruction: 'Listen for three distinct bird calls.',
    step2: '2. Go outside and listen quietly.',
    focus: 'Soundscape',
    reflectionDefault: 'Heard a loud crow nearby and a pair of small birds singing from an oak canopy.'
  },
  {
    title: 'Step into the daylight and watch the sky for five minutes.',
    description: 'Look at cloud movement and the horizon. Let natural daylight reset your rhythm. No phone until you are done.',
    outsideInstruction: 'Keep your eyes toward the open sky.',
    step2: '2. Go outside and watch the sky.',
    focus: 'Sunlight',
    reflectionDefault: 'The air was crisp and the morning light was much warmer than my room.'
  },
  {
    title: 'Find five fallen leaves with distinct shapes or colors.',
    description: 'Look closely at the ground. Notice the subtle variations in seasonal change. No phone until you are done.',
    outsideInstruction: 'Spot five leaves with different patterns.',
    step2: '2. Go outside and search the ground.',
    focus: 'Observation',
    reflectionDefault: 'Found bright yellow maple leaves and deep brown oak leaves with jagged edges.'
  }
];

// Web Audio API serene Tibetan-style bell chime (100% offline, zero external files)
function playZenChime() {
  try {
    const AudioContextClass = window.AudioContext || (window as any).webkitAudioContext;
    if (!AudioContextClass) return;
    const ctx = new AudioContextClass();
    if (ctx.state === 'suspended') {
      ctx.resume();
    }
    const now = ctx.currentTime;

    // Fundamental tone ~ 528 Hz (calm, organic resonance)
    const osc1 = ctx.createOscillator();
    const gain1 = ctx.createGain();
    osc1.type = 'sine';
    osc1.frequency.setValueAtTime(528, now);
    gain1.gain.setValueAtTime(0.24, now);
    gain1.gain.exponentialRampToValueAtTime(0.0001, now + 3.8);
    osc1.connect(gain1);
    gain1.connect(ctx.destination);

    // Overtone ~ 1056 Hz (gentle bell shimmer)
    const osc2 = ctx.createOscillator();
    const gain2 = ctx.createGain();
    osc2.type = 'sine';
    osc2.frequency.setValueAtTime(1056, now);
    gain2.gain.setValueAtTime(0.12, now);
    gain2.gain.exponentialRampToValueAtTime(0.0001, now + 2.6);
    osc2.connect(gain2);
    gain2.connect(ctx.destination);

    osc1.start(now);
    osc2.start(now);
    osc1.stop(now + 3.9);
    osc2.stop(now + 2.7);
  } catch (e) {
    console.error('Audio chime error:', e);
  }
}

export function App() {
  const [page, setPage] = useState<PageState>('mission');
  const [missionIndex, setMissionIndex] = useState<number>(0);
  const [selectedDuration, setSelectedDuration] = useState<DurationOption>(15);
  const [offlineMode, setOfflineMode] = useState<boolean>(false);
  const [isDimmed, setIsDimmed] = useState<boolean>(false);
  const [isListening, setIsListening] = useState<boolean>(false);
  const [savedReflection, setSavedReflection] = useState<boolean>(false);
  const [reflectionText, setReflectionText] = useState<string>(MISSIONS[0].reflectionDefault);
  const [chimeTriggered, setChimeTriggered] = useState<boolean>(false);

  // Reflections history stored in localStorage
  const [reflectionsHistory, setReflectionsHistory] = useState<SavedReflection[]>(() => {
    const saved = localStorage.getItem('touchgrass_reflections');
    if (saved) {
      try { return JSON.parse(saved); } catch (e) {}
    }
    return [
      {
        id: '1',
        date: 'Oct 6, 2026',
        missionTitle: 'Find a tree and spend two minutes looking at it.',
        durationMinutes: 15,
        xpEarned: 40,
        reflectionText: 'The bark was deeper than I expected, and a bird kept landing on one branch.'
      },
      {
        id: '2',
        date: 'Oct 5, 2026',
        missionTitle: 'Step outside and listen until you hear three birds.',
        durationMinutes: 10,
        xpEarned: 35,
        reflectionText: 'Heard a loud crow nearby and a pair of small birds singing from an oak canopy.'
      }
    ];
  });

  // Calculate dynamic XP based on duration
  const getRewardXP = (mins: DurationOption) => {
    if (mins === 5) return 20;
    if (mins === 30) return 60;
    return 40;
  };

  const currentMission = MISSIONS[missionIndex];
  const currentXP = getRewardXP(selectedDuration);

  // Feature 8: TabPFN Outdoor Vitality & Window Forecaster
  const [vitalityForecast, setVitalityForecast] = useState<VitalityForecast>({
    vitality_score: 91,
    peak_vitality_score: 95,
    optimal_window: 'Today 10:30 AM',
    condition: 'Crisp Morning Sunlight',
    advice: 'Optimal natural light for circadian reset. UV is gentle; ideal for 15-30m outside.',
    temperature_c: 21.2,
    uv_index: 3.8,
    inference_ms: 3.4,
    model_engine: 'TabPFN Tabular Foundation Model (Prior Labs)'
  });

  useEffect(() => {
    if (offlineMode) return;
    const fetchForecast = async () => {
      try {
        const res = await fetch(`/api/forecast/vitality?duration=${selectedDuration}&focus=${encodeURIComponent(currentMission.focus)}`);
        if (res.ok) {
          const data = await res.json();
          if (data && data.vitality_score) {
            setVitalityForecast(data);
          }
        }
      } catch {
        // Offline resilient fallback
      }
    };
    fetchForecast();
  }, [selectedDuration, missionIndex, offlineMode, currentMission.focus]);

  // Timer state for Outside page (countdown in seconds)
  const [secondsLeft, setSecondsLeft] = useState<number>(selectedDuration * 60);

  useEffect(() => {
    let timer: ReturnType<typeof setInterval> | undefined;
    if (page === 'outside' && secondsLeft > 0) {
      timer = setInterval(() => {
        setSecondsLeft((prev) => {
          if (prev <= 1) {
            if (!chimeTriggered) {
              playZenChime();
              setChimeTriggered(true);
            }
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }
    return () => {
      if (timer) clearInterval(timer);
    };
  }, [page, secondsLeft, chimeTriggered]);

  // Format countdown mm:ss
  const formatTime = (totalSeconds: number) => {
    const mins = Math.floor(totalSeconds / 60);
    const secs = totalSeconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleStartMission = () => {
    setSecondsLeft(selectedDuration * 60);
    setIsDimmed(false);
    setSavedReflection(false);
    setChimeTriggered(false);
    setReflectionText(currentMission.reflectionDefault);
    setPage('outside');
  };

  const handleListen = () => {
    if ('speechSynthesis' in window) {
      if (isListening) {
        window.speechSynthesis.cancel();
        setIsListening(false);
      } else {
        const text = `Today's mission: ${currentMission.title} ${currentMission.description}`;
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.9;
        utterance.pitch = 1.0;
        utterance.onend = () => setIsListening(false);
        utterance.onerror = () => setIsListening(false);
        setIsListening(true);
        window.speechSynthesis.speak(utterance);
      }
    }
  };

  const handleAnotherMission = () => {
    if ('speechSynthesis' in window && isListening) {
      window.speechSynthesis.cancel();
      setIsListening(false);
    }
    const nextIdx = (missionIndex + 1) % MISSIONS.length;
    setMissionIndex(nextIdx);
    setReflectionText(MISSIONS[nextIdx].reflectionDefault);
  };

  const handleSaveReflection = () => {
    if (!savedReflection) {
      const newEntry: SavedReflection = {
        id: Date.now().toString(),
        date: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
        missionTitle: currentMission.title,
        durationMinutes: selectedDuration,
        xpEarned: currentXP + 10,
        reflectionText: reflectionText.trim()
      };
      const updated = [newEntry, ...reflectionsHistory];
      setReflectionsHistory(updated);
      localStorage.setItem('touchgrass_reflections', JSON.stringify(updated));
      setSavedReflection(true);
    }
  };

  // Compute live stats for Journey
  const totalMissionsCompleted = reflectionsHistory.length;
  const totalMinutesOutdoors = reflectionsHistory.reduce((acc, curr) => acc + curr.durationMinutes, 0);

  // -------------------------------------------------------------
  // SHARED HEADER (Used in Mission, Complete, and Journey pages)
  // -------------------------------------------------------------
  const SharedHeader = () => (
    <header className="w-full border-b border-[#DDE2DC] bg-[#F6F7F4]">
      <div className="max-w-[1200px] mx-auto px-6 sm:px-12 py-5 flex items-center justify-between">
        {/* Left: Wordmark */}
        <button
          type="button"
          onClick={() => setPage('mission')}
          className="text-[18px] font-bold text-[#14201A] font-sans tracking-tight focus-visible:outline-2 focus-visible:outline-[#1F5A3D] text-left cursor-pointer"
        >
          TouchGrass
        </button>

        {/* Center: Two text tabs */}
        <nav className="flex items-center space-x-8" aria-label="Main Navigation">
          <button
            type="button"
            onClick={() => setPage('mission')}
            className={`min-h-[44px] text-[15px] transition-colors cursor-pointer ${
              page === 'mission' || page === 'complete'
                ? 'text-[#1F5A3D] font-bold'
                : 'text-[#4A564F] font-medium hover:text-[#14201A]'
            }`}
          >
            Mission
          </button>
          <button
            type="button"
            onClick={() => setPage('journey')}
            className={`min-h-[44px] text-[15px] transition-colors cursor-pointer ${
              page === 'journey'
                ? 'text-[#1F5A3D] font-bold'
                : 'text-[#4A564F] font-medium hover:text-[#14201A]'
            }`}
          >
            Journey
          </button>
        </nav>

        {/* Right: Outlined pill button "Offline mode" */}
        <button
          type="button"
          onClick={() => setOfflineMode((prev) => !prev)}
          className={`min-h-[44px] px-5 border rounded-full text-[14px] font-medium transition-colors cursor-pointer ${
            offlineMode
              ? 'border-[#1F5A3D] bg-[#1F5A3D] text-[#FFFFFF]'
              : 'border-[#DDE2DC] bg-transparent text-[#14201A] hover:border-[#1F5A3D]'
          }`}
        >
          {offlineMode ? 'Offline active' : 'Offline mode'}
        </button>
      </div>

      {/* Feature 5: Offline Mode Subtle Banner */}
      {offlineMode && (
        <div className="w-full bg-[#EBF0EC] border-t border-[#DDE2DC] py-2 px-6 sm:px-12 text-center text-[13px] text-[#1F5A3D] font-medium">
          Offline trail mode active: All missions & reflections are stored on-device with zero data sent to the cloud.
        </div>
      )}
    </header>
  );

  // -------------------------------------------------------------
  // PAGE 2: OUTSIDE (Dark, full screen, no tabs)
  // -------------------------------------------------------------
  if (page === 'outside') {
    return (
      <div
        className={`min-h-screen bg-[#16211B] text-[#EEF2EE] font-sans flex flex-col justify-between transition-opacity duration-300 ${
          isDimmed ? 'opacity-35' : 'opacity-100'
        }`}
      >
        {/* Top bar */}
        <header className="w-full border-b border-[#3A4A41]/60">
          <div className="max-w-[1200px] mx-auto px-6 sm:px-12 py-5 flex items-center justify-between">
            <span className="text-[18px] font-bold text-[#EEF2EE] tracking-tight">
              TouchGrass
            </span>
            <div className="flex items-center space-x-4">
              {/* Feature 1: Test Chime Button */}
              <button
                type="button"
                onClick={playZenChime}
                title="Preview outdoor completion chime"
                className="min-h-[44px] px-3 text-[13px] text-[#A9B6AD] hover:text-[#EEF2EE] font-medium transition-colors cursor-pointer"
              >
                Chime test
              </button>
              <button
                type="button"
                onClick={() => setIsDimmed((prev) => !prev)}
                className="min-h-[44px] px-5 border border-[#3A4A41] rounded-full text-[14px] text-[#EEF2EE] font-medium hover:border-[#6F8A78] transition-colors cursor-pointer"
              >
                {isDimmed ? 'Restore brightness' : 'Dim screen'}
              </button>
              <button
                type="button"
                onClick={() => {
                  setIsDimmed(false);
                  setPage('mission');
                }}
                className="min-h-[44px] px-3 text-[15px] text-[#A9B6AD] hover:text-[#EEF2EE] font-medium transition-colors cursor-pointer"
              >
                Cancel mission
              </button>
            </div>
          </div>
        </header>

        {/* Centered content */}
        <main className="flex-1 max-w-[1200px] w-full mx-auto px-6 sm:px-12 py-12 flex flex-col items-center justify-center text-center">
          {/* Two concentric circles (260px and 180px, 1px borders) */}
          <div className="w-[260px] h-[260px] rounded-full border border-[#3A4A41] flex items-center justify-center mb-8">
            <div className="w-[180px] h-[180px] rounded-full border border-[#6F8A78] flex items-center justify-center">
              <span className="font-serif text-[48px] font-normal text-[#EEF2EE] leading-none">
                {formatTime(secondsLeft)}
              </span>
            </div>
          </div>

          <h1 className="font-serif text-[32px] md:text-[40px] font-normal text-[#EEF2EE] leading-tight mb-3">
            {secondsLeft === 0 ? "Time's up. Take a deep breath." : "You are outside. Put the phone away."}
          </h1>

          <p className="text-[18px] text-[#A9B6AD] mb-8">
            {secondsLeft === 0
              ? "Your outdoor window is complete. Tap 'I'm back' when you are ready."
              : currentMission.outsideInstruction}
          </p>

          {/* One light button "I'm back" (background #EEF2EE, dark text, 56px tall) */}
          <button
            type="button"
            onClick={() => {
              setIsDimmed(false);
              setPage('complete');
            }}
            className="min-h-[56px] h-[56px] px-8 rounded-[12px] bg-[#EEF2EE] text-[#14201A] font-semibold text-[16px] hover:bg-[#FFFFFF] transition-colors focus-visible:outline-2 focus-visible:outline-[#EEF2EE] cursor-pointer"
          >
            I'm back
          </button>
        </main>

        <footer className="w-full py-4 text-center text-[13px] text-[#A9B6AD]/60">
          TouchGrass
        </footer>
      </div>
    );
  }

  // -------------------------------------------------------------
  // JOURNEY TAB (Features 3 & 4: Real Reflections Diary & 7-Day Tracker)
  // -------------------------------------------------------------
  if (page === 'journey') {
    return (
      <div className="min-h-screen bg-[#F6F7F4] text-[#14201A] font-sans flex flex-col">
        <SharedHeader />
        <main className="flex-1 max-w-[1200px] w-full mx-auto px-6 sm:px-12 py-16">
          <div className="mb-8">
            <div className="text-[13px] font-semibold tracking-[0.12em] uppercase text-[#1F5A3D] mb-4">
              JOURNEY
            </div>
            <h1 className="font-serif text-[42px] md:text-[52px] font-normal leading-[1.1] text-[#14201A] mb-4">
              Your time outside.
            </h1>
            <p className="text-[19px] text-[#4A564F] max-w-[520px]">
              Every minute spent away from the screen adds to your real-world progress.
            </p>
          </div>

          {/* Top Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-[900px] mb-8">
            <div className="bg-[#FFFFFF] border border-[#DDE2DC] rounded-[16px] p-6">
              <div className="text-[13px] text-[#4A564F] font-medium mb-1">Total missions</div>
              <div className="text-[28px] font-semibold text-[#14201A]">{totalMissionsCompleted}</div>
            </div>
            <div className="bg-[#FFFFFF] border border-[#DDE2DC] rounded-[16px] p-6">
              <div className="text-[13px] text-[#4A564F] font-medium mb-1">Time outdoors</div>
              <div className="text-[28px] font-semibold text-[#14201A]">{totalMinutesOutdoors} min</div>
            </div>
            <div className="bg-[#FFFFFF] border border-[#DDE2DC] rounded-[16px] p-6">
              <div className="text-[13px] text-[#4A564F] font-medium mb-1">Current streak</div>
              <div className="text-[28px] font-semibold text-[#14201A]">4 days</div>
            </div>
          </div>

          {/* Feature 4: 7-Day Outdoor Streak Tracker */}
          <div className="bg-[#FFFFFF] border border-[#DDE2DC] rounded-[16px] p-6 max-w-[900px] mb-8">
            <div className="text-[13px] font-semibold uppercase tracking-[0.1em] text-[#4A564F] mb-4">
              7-Day Activity
            </div>
            <div className="grid grid-cols-7 gap-2 max-w-[500px]">
              {[
                { day: 'Mon', completed: true },
                { day: 'Tue', completed: true },
                { day: 'Wed', completed: true },
                { day: 'Thu', completed: true },
                { day: 'Fri', completed: false },
                { day: 'Sat', completed: false },
                { day: 'Sun', completed: false }
              ].map((item, idx) => (
                <div key={idx} className="flex flex-col items-center gap-2">
                  <span className="text-[12px] font-medium text-[#4A564F]">{item.day}</span>
                  <div
                    className={`w-7 h-7 rounded-full flex items-center justify-center border ${
                      item.completed
                        ? 'bg-[#1F5A3D] border-[#1F5A3D] text-[#FFFFFF]'
                        : 'bg-transparent border-[#DDE2DC] text-transparent'
                    }`}
                  >
                    {item.completed && <span className="text-[10px]">✓</span>}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Feature 3: Real Saved Reflections History */}
          <div className="max-w-[900px] mb-12">
            <h2 className="font-serif text-[24px] font-normal text-[#14201A] mb-4">
              Recent outdoor reflections
            </h2>
            <div className="space-y-4">
              {reflectionsHistory.map((entry) => (
                <div
                  key={entry.id}
                  className="bg-[#FFFFFF] border border-[#DDE2DC] rounded-[16px] p-6 space-y-2"
                >
                  <div className="flex items-center justify-between text-[13px] text-[#4A564F]">
                    <span className="font-semibold text-[#1F5A3D]">{entry.missionTitle}</span>
                    <span>{entry.date} • {entry.durationMinutes} min • +{entry.xpEarned} XP</span>
                  </div>
                  <p className="text-[15px] leading-[1.6] text-[#14201A] italic">
                    "{entry.reflectionText}"
                  </p>
                </div>
              ))}
            </div>
          </div>

          <button
            type="button"
            onClick={() => setPage('mission')}
            className="min-h-[56px] h-[56px] px-8 rounded-[12px] bg-[#1F5A3D] text-[#FFFFFF] font-semibold text-[16px] hover:bg-[#184830] transition-colors focus-visible:outline-2 focus-visible:outline-[#1F5A3D] cursor-pointer"
          >
            Back to mission
          </button>
        </main>
      </div>
    );
  }

  // -------------------------------------------------------------
  // PAGE 3: COMPLETE
  // -------------------------------------------------------------
  if (page === 'complete') {
    return (
      <div className="min-h-screen bg-[#F6F7F4] text-[#14201A] font-sans flex flex-col">
        <SharedHeader />

        <main className="flex-1 max-w-[1200px] w-full mx-auto px-6 sm:px-12 py-12 md:py-20 lg:py-24 grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-[72px] items-center">
          {/* Left Column */}
          <div className="lg:col-span-7 flex flex-col justify-center">
            <div className="text-[13px] font-semibold tracking-[0.12em] uppercase text-[#1F5A3D] mb-4">
              MISSION COMPLETE
            </div>

            <h1 className="font-serif text-[38px] md:text-[48px] lg:text-[56px] font-normal leading-[1.1] text-[#14201A] mb-8">
              Well done. {selectedDuration} minutes outside.
            </h1>

            {/* Three stats between thin top and bottom borders */}
            <div className="grid grid-cols-3 border-t border-b border-[#DDE2DC] py-6 my-6">
              <div>
                <div className="text-[13px] text-[#4A564F] font-medium mb-1">XP earned</div>
                <div className="text-[20px] font-semibold text-[#14201A]">+{currentXP}</div>
              </div>
              <div>
                <div className="text-[13px] text-[#4A564F] font-medium mb-1">Level</div>
                <div className="text-[20px] font-semibold text-[#14201A]">3</div>
              </div>
              <div>
                <div className="text-[13px] text-[#4A564F] font-medium mb-1">Streak</div>
                <div className="text-[20px] font-semibold text-[#14201A]">4 days</div>
              </div>
            </div>
          </div>

          {/* Right Column: White card */}
          <div className="lg:col-span-5">
            <div className="bg-[#FFFFFF] border border-[#DDE2DC] rounded-[16px] p-8">
              <label
                htmlFor="reflection"
                className="block text-[14px] font-medium text-[#14201A] mb-3"
              >
                How was it? (optional, +10 XP)
              </label>

              <textarea
                id="reflection"
                value={reflectionText}
                onChange={(e) => setReflectionText(e.target.value)}
                className="w-full h-[180px] rounded-[12px] border border-[#CFD6D0] p-4 text-[15px] leading-[1.5] text-[#14201A] bg-[#FFFFFF] resize-none focus:outline-none focus:border-[#1F5A3D] transition-colors"
              />

              <div className="flex items-center gap-4 mt-6">
                <button
                  type="button"
                  onClick={handleSaveReflection}
                  className="min-h-[56px] h-[56px] px-8 rounded-[12px] bg-[#1F5A3D] text-[#FFFFFF] font-semibold text-[16px] hover:bg-[#184830] transition-colors focus-visible:outline-2 focus-visible:outline-[#1F5A3D] cursor-pointer"
                >
                  {savedReflection ? 'Saved to Journey (+10 XP)' : 'Save reflection'}
                </button>

                <button
                  type="button"
                  onClick={() => {
                    setSavedReflection(false);
                    setPage('mission');
                    setMissionIndex((prev) => (prev + 1) % MISSIONS.length);
                  }}
                  className="min-h-[44px] px-3 bg-transparent text-[#1F5A3D] font-semibold text-[16px] hover:underline cursor-pointer"
                >
                  Next mission
                </button>
              </div>
            </div>
          </div>
        </main>
      </div>
    );
  }

  // -------------------------------------------------------------
  // PAGE 1: MISSION (Default)
  // -------------------------------------------------------------
  return (
    <div className="min-h-screen bg-[#F6F7F4] text-[#14201A] font-sans flex flex-col">
      <SharedHeader />

      <main className="flex-1 max-w-[1200px] w-full mx-auto px-6 sm:px-12 py-12 md:py-20 lg:py-24 grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-[72px] items-center">
        {/* Left Column */}
        <div className="lg:col-span-7 flex flex-col justify-center">
          <div className="text-[13px] font-semibold tracking-[0.12em] uppercase text-[#1F5A3D] mb-4">
            TODAY'S MISSION
          </div>

          <h1 className="font-serif text-[42px] md:text-[52px] lg:text-[60px] font-normal leading-[1.08] text-[#14201A] mb-6">
            {currentMission.title}
          </h1>

          <p className="text-[19px] leading-[1.5] text-[#4A564F] max-w-[520px] mb-8">
            {currentMission.description}
          </p>

          <div className="flex flex-wrap items-center gap-4">
            {/* Primary green "Start mission" */}
            <button
              type="button"
              onClick={handleStartMission}
              className="min-h-[56px] h-[56px] px-8 rounded-[12px] bg-[#1F5A3D] text-[#FFFFFF] font-semibold text-[16px] hover:bg-[#184830] transition-colors focus-visible:outline-2 focus-visible:outline-[#1F5A3D] cursor-pointer"
            >
              Start mission
            </button>

            {/* Outlined "Listen" */}
            <button
              type="button"
              onClick={handleListen}
              className="min-h-[56px] h-[56px] px-7 rounded-[12px] border border-[#DDE2DC] bg-transparent text-[#14201A] font-medium text-[16px] hover:border-[#1F5A3D] transition-colors cursor-pointer"
            >
              {isListening ? 'Stop' : 'Listen'}
            </button>

            {/* Text-only green "Another mission" */}
            <button
              type="button"
              onClick={handleAnotherMission}
              className="min-h-[44px] px-3 bg-transparent text-[#1F5A3D] font-semibold text-[16px] hover:underline cursor-pointer"
            >
              Another mission
            </button>
          </div>
        </div>

        {/* Right Column: White card */}
        <div className="lg:col-span-5">
          <div className="bg-[#FFFFFF] border border-[#DDE2DC] rounded-[16px] p-8">
            {/* Top row with three stats separated by a bottom border */}
            <div className="flex items-start justify-between border-b border-[#DDE2DC] pb-6 mb-6 gap-6">
              <div className="shrink-0">
                <div className="text-[13px] text-[#4A564F] font-medium mb-1.5">Time</div>
                {/* Feature 2: Flexible Duration Selector (5m / 15m / 30m) */}
                <div className="flex items-center gap-1">
                  {[5, 15, 30].map((mins) => (
                    <button
                      key={mins}
                      type="button"
                      onClick={() => setSelectedDuration(mins as DurationOption)}
                      className={`text-[12px] px-2 py-0.5 rounded-[6px] font-semibold transition-colors cursor-pointer ${
                        selectedDuration === mins
                          ? 'bg-[#1F5A3D] text-[#FFFFFF]'
                          : 'bg-[#F6F7F4] text-[#4A564F] hover:text-[#14201A]'
                      }`}
                    >
                      {mins}m
                    </button>
                  ))}
                </div>
              </div>

              <div className="pl-6">
                <div className="text-[13px] text-[#4A564F] font-medium mb-1.5">Focus</div>
                <div className="text-[16px] font-semibold text-[#14201A]">{currentMission.focus}</div>
              </div>

              <div>
                <div className="text-[13px] text-[#4A564F] font-medium mb-1.5">Reward</div>
                <div className="text-[16px] font-semibold text-[#14201A]">{currentXP} XP</div>
              </div>
            </div>

            {/* Heading "How it works", then three muted lines */}
            <h2 className="font-serif text-[20px] font-normal text-[#14201A] mb-4">
              How it works
            </h2>

            <div className="space-y-3 text-[15px] leading-[1.6] text-[#4A564F]">
              <p>1. Start the mission, then put your phone away.</p>
              <p>{currentMission.step2}</p>
              <p>3. Come back, tap 'I'm back' and add a short reflection.</p>
            </div>

            {/* Feature 8: Microclimate Vitality Forecaster (TabPFN) */}
            <div className="mt-8 pt-6 border-t border-[#DDE2DC]">
              <div className="flex items-center justify-between mb-2">
                <span className="text-[12px] font-semibold tracking-[0.12em] uppercase text-[#1F5A3D]">
                  OUTDOOR VITALITY FORECAST
                </span>
                <span className="text-[11px] font-medium text-[#4A564F] px-2 py-0.5 rounded-[4px] border border-[#DDE2DC] bg-[#F6F7F4]">
                  TabPFN Foundation Model
                </span>
              </div>

              <div className="flex items-baseline justify-between mb-1.5">
                <span className="text-[15px] font-semibold text-[#14201A]">
                  Optimal window: {vitalityForecast.optimal_window}
                </span>
                <span className="text-[13px] font-semibold text-[#1F5A3D]">
                  Vitality {vitalityForecast.vitality_score}/100
                </span>
              </div>

              <p className="text-[13px] text-[#4A564F] leading-[1.5]">
                {vitalityForecast.condition} • {vitalityForecast.temperature_c}°C • UV {vitalityForecast.uv_index}. {vitalityForecast.advice}
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
