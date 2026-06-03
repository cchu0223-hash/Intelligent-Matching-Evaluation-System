export type Recommendation = {
  rank: number;
  speaker_name: string;
  vcn: string;
  gender: string;
  language: string;
  scene_l1: string[];
  scene_l2: string[];
  attributes: string[];
  tech_desc: string;
  audio_url: string | null;
  score: number | null;
  reason: string | null;
  debug: Record<string, unknown>;
};

export type RecommendResponse = {
  request_id: string;
  task_type: string;
  mode: string;
  stage: string;
  debug_tags: Record<string, unknown>;
  recommendations: Recommendation[];
  llm_error: string | null;
};

export type FeedbackPayload = {
  request_id: string;
  vcn: string;
  speaker_name: string;
  rank: number;
  rating: number;
  suggestion?: string;
};
