export type ChallengeCategory = 
  | 'Outdoor'
  | 'Nature'
  | 'Kindness'
  | 'Happiness'
  | 'Human Connection'
  | 'Community'
  | 'Health'
  | 'Creativity'
  | 'Exploration';

export type DifficultyLevel = 'Easy' | 'Medium' | 'Hard';

export interface Challenge {
  id: string;
  title: string;
  description: string;
  category: ChallengeCategory;
  difficulty: DifficultyLevel;
  xp_reward: number;
  time_estimate_minutes: number;
  spoken_intro: string;
  safety_notes: string;
  created_at: string;
  status: 'pending' | 'accepted' | 'completed' | 'skipped';
}

export interface UserContext {
  user_id: string;
  username: string;
  level: number;
  xp: number;
  xp_to_next_level: number;
  streak_days: number;
  completed_challenges_count: number;
  badges: string[];
  unlocked_features: string[];
  offline_mode: boolean;
  preferred_categories: ChallengeCategory[];
  recent_categories: string[];
}

export interface RewardResult {
  challenge_id: string;
  base_xp: number;
  bonus_xp: number;
  total_xp_awarded: number;
  previous_level: number;
  new_level: number;
  level_up: boolean;
  new_badges: string[];
  unlocked_features: string[];
  gemma_encouragement: string;
  sincerity_score: number;
}

export interface SocialPost {
  id: string;
  author_name: string;
  author_level: number;
  broad_location: string;
  challenge_title: string;
  category: string;
  reflection: string;
  time_ago: string;
  kudos_count: number;
  verified: boolean;
}

export interface JourneyCardData {
  username: string;
  level: number;
  total_challenges: number;
  categories_breakdown: Record<string, number>;
  badges_earned: Array<{ id: string; title: string; icon: string }>;
  notable_quotes: string[];
  shareable_summary: string;
}

export interface AgentTrace {
  step: string;
  duration_ms: number;
  timestamp: number;
  metadata: Record<string, any>;
}
