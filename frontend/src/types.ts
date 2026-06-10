export type MatchedTags = {
  scene_l1: string[];
  scene_l2: string[];
  attributes: string[];
  language: boolean;
};

export type Recommendation = {
  rank: number;
  speaker_name: string;
  vcn: string;
  gender: string;
  language: string;
  scene_l1: string[];
  scene_l2: string[];
  attributes: string[];
  matched_tags: MatchedTags;
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

export type SceneFeedbackPayload = {
  request_id: string;
  suggested_scene_l1: string[];
  suggested_scene_l2: string[];
  suggested_keywords: string;
  suggestion?: string;
};

export type TaxonomyResponse = {
  scene_l1: string[];
  scene_l2: string[];
};
