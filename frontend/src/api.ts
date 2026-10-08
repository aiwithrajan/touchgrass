import { UserContext, Challenge, RewardResult, SocialPost, JourneyCardData, AgentTrace } from './types';

const API_BASE = '/api';

export const api = {
  async getUser(): Promise<UserContext> {
    try {
      const res = await fetch(`${API_BASE}/user`);
      if (res.ok) return await res.json();
    } catch (e) {
      console.warn('API unavailable, using local offline fallback');
    }
    return getLocalUser();
  },

  async toggleOffline(): Promise<{ offline_mode: boolean; message: string }> {
    try {
      const res = await fetch(`${API_BASE}/user/toggle-offline`, { method: 'POST' });
      if (res.ok) return await res.json();
    } catch (e) {
      console.warn('API unavailable, toggling in local storage');
    }
    const user = getLocalUser();
    user.offline_mode = !user.offline_mode;
    saveLocalUser(user);
    return {
      offline_mode: user.offline_mode,
      message: user.offline_mode ? 'Airplane / Local Trail mode enabled' : 'Online Cloud Sync enabled'
    };
  },

  async generateChallenge(category?: string, difficulty?: string): Promise<Challenge> {
    try {
      const res = await fetch(`${API_BASE}/challenge/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          desired_category: category || null,
          difficulty: difficulty || null,
          time_available_minutes: 20
        })
      });
      if (res.ok) return await res.json();
    } catch (e) {
      console.warn('API unavailable, generating offline challenge locally');
    }
    return getOfflineChallenge(category);
  },

  async submitReflection(challengeId: string, text: string, minutes: number = 15): Promise<RewardResult> {
    try {
      const res = await fetch(`${API_BASE}/challenge/reflect`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          challenge_id: challengeId,
          reflection_text: text,
          minutes_spent: minutes
        })
      });
      if (res.ok) return await res.json();
    } catch (e) {
      console.warn('API unavailable, calculating reward locally');
    }
    return calculateLocalReward(challengeId, text, minutes);
  },

  async getSocialFeed(): Promise<{ unlocked: boolean; required_level: number; current_level: number; feed: SocialPost[] }> {
    try {
      const res = await fetch(`${API_BASE}/social/feed`);
      if (res.ok) return await res.json();
    } catch (e) {}
    const user = getLocalUser();
    return {
      unlocked: user.level >= 5,
      required_level: 5,
      current_level: user.level,
      feed: [
        {
          id: 'post_1',
          author_name: 'Maya S.',
          author_level: 6,
          broad_location: 'Portland, OR',
          challenge_title: 'Find 3 distinct tree barks',
          category: 'Nature',
          reflection: 'Found a weeping willow near the river trail. Spent an hour sitting by the water instead of scrolling Instagram.',
          time_ago: '2 hours ago',
          kudos_count: 14,
          verified: true
        },
        {
          id: 'post_2',
          author_name: 'Liam K.',
          author_level: 7,
          broad_location: 'Boulder, CO',
          challenge_title: 'Help a stranger without prompt',
          category: 'Kindness',
          reflection: 'Helped someone load a heavy bicycle rack into their trunk at the park trailhead.',
          time_ago: '5 hours ago',
          kudos_count: 28,
          verified: true
        }
      ]
    };
  },

  async getJourneyCard(): Promise<JourneyCardData> {
    try {
      const res = await fetch(`${API_BASE}/journey`);
      if (res.ok) return await res.json();
    } catch (e) {}
    const user = getLocalUser();
    return {
      username: user.username,
      level: user.level,
      total_challenges: Math.max(user.completed_challenges_count, 1),
      categories_breakdown: { 'Outdoor': 2, 'Nature': 2, 'Kindness': 1 },
      badges_earned: [
        { id: 'earth_helper', title: 'Earth Helper', icon: '🌱' },
        { id: 'good_human', title: 'Good Human', icon: '🤝' }
      ],
      notable_quotes: [
        '"Took a 20-minute walk with zero screens."',
        '"Helped my neighbor carry groceries up the stairs."'
      ],
      shareable_summary: `TouchGrass Journey: Level ${user.level} | ${user.completed_challenges_count} real-world outdoor missions completed.`
    };
  },

  async getObservabilityTraces(): Promise<AgentTrace[]> {
    try {
      const res = await fetch(`${API_BASE}/observability/traces`);
      if (res.ok) return await res.json();
    } catch (e) {}
    return [
      { step: 'gemma.retrieve_memory', duration_ms: 12.4, timestamp: Date.now() - 4000, metadata: { cache: 'local-first' } },
      { step: 'gemma.generate_challenge', duration_ms: 45.2, timestamp: Date.now() - 3000, metadata: { model: 'gemma-2-9b-it', safety: 'passed' } },
      { step: 'policy_engine.validate_diversity', duration_ms: 1.8, timestamp: Date.now() - 2500, metadata: { passed: true } }
    ];
  },

  async speakVoice(text: string): Promise<{ audio_base64?: string; text: string; provider: string }> {
    try {
      const res = await fetch(`${API_BASE}/voice/speak?text=${encodeURIComponent(text)}`);
      if (res.ok) return await res.json();
    } catch (e) {}
    return { text, provider: 'web_speech_fallback' };
  }
};

// Local storage fallback helpers
function getLocalUser(): UserContext {
  const stored = localStorage.getItem('touchgrass_user');
  if (stored) {
    try { return JSON.parse(stored); } catch (e) {}
  }
  const defaultUser: UserContext = {
    user_id: 'guest_user',
    username: 'Trailblazer',
    level: 1,
    xp: 0,
    xp_to_next_level: 150,
    streak_days: 2,
    completed_challenges_count: 0,
    badges: [],
    unlocked_features: [],
    offline_mode: false,
    preferred_categories: [],
    recent_categories: []
  };
  localStorage.setItem('touchgrass_user', JSON.stringify(defaultUser));
  return defaultUser;
}

function saveLocalUser(user: UserContext) {
  localStorage.setItem('touchgrass_user', JSON.stringify(user));
}

function getOfflineChallenge(category?: string): Challenge {
  return {
    id: `ch_local_${Date.now().toString().slice(-6)}`,
    title: 'The Unplugged Horizon Walk',
    description: 'Step outside for 20 minutes without headphones or screen glancing. Notice the transition of light on the rooftops and trees as you walk.',
    category: (category as any) || 'Outdoor',
    difficulty: 'Medium',
    xp_reward: 120,
    time_estimate_minutes: 20,
    spoken_intro: 'Your mission today is quiet and simple. Put your phone on silent, step out the door, and walk for twenty minutes without headphones. Look at the horizon. I will be right here when you return.',
    safety_notes: 'Stay aware of your surroundings, respect private property, and keep your attention on the physical world.',
    created_at: new Date().toISOString(),
    status: 'pending'
  };
}

function calculateLocalReward(challengeId: string, text: string, minutes: number): RewardResult {
  const user = getLocalUser();
  const base_xp = 100;
  const bonus_xp = text.length > 25 ? 20 : 10;
  const total = base_xp + bonus_xp;
  
  const old_level = user.level;
  user.xp += total;
  user.completed_challenges_count += 1;
  
  if (user.xp >= user.xp_to_next_level) {
    user.level += 1;
    user.xp_to_next_level = Math.floor(user.xp_to_next_level * 1.35);
  }
  
  const new_badges: string[] = [];
  if (!user.badges.includes('earth_helper')) {
    user.badges.push('earth_helper');
    new_badges.push('earth_helper');
  }
  
  const new_unlocks: string[] = [];
  if (user.level >= 5 && !user.unlocked_features.includes('social_mode')) {
    user.unlocked_features.push('social_mode');
    new_unlocks.push('social_mode');
  }
  
  saveLocalUser(user);
  
  return {
    challenge_id: challengeId,
    base_xp,
    bonus_xp,
    total_xp_awarded: total,
    previous_level: old_level,
    new_level: user.level,
    level_up: user.level > old_level,
    new_badges,
    unlocked_features: new_unlocks,
    gemma_encouragement: 'Gemma Agent: You completed your real-world mission. You chose real dirt, wind, and sky over pixels. Welcome back!',
    sincerity_score: 0.95
  };
}
