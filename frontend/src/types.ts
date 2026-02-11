// Type definitions for API
export interface DraftCreate {
  title: string;
  description: string;
  cpv?: string;
}

export interface Draft {
  id: number;
  title: string;
  description: string;
  cpv?: string;
}

export interface Notice {
  notice_id: string;
  url: string;
  title: string;
  buyer: string;
  cpv_codes: string[];
  published_date: string;
  deadline: string;
  estimated_value_nok?: number;
  procedure: string;
  duration: string;
  description_raw: string;
  description_excerpt: string;
  similarity_score: number;
}

export interface SimilarNotice {
  notice_id: string;
  score: number;
  title?: string;
  buyer?: string;
  cpv_codes?: string[];
  published_date?: string;
}

export interface QualitativeAnalysis {
  risk_management: string;
  sustainability_social_values: string;
  transparency_fair_competition: string;
  innovation_forward_thinking: string;
}

export interface Recommendation {
  decision: string;
  rationale: string;
}

export interface AnalysisResult {
  similar_notices_ranked: SimilarNotice[];
  overlap_summary: string;
  qualitative_analysis: QualitativeAnalysis;
  recommendation: Recommendation;
  confidence: number;
  caveats: string;
}

export interface AnalysisResponse {
  retrieved_notices: Notice[];
  analysis: AnalysisResult;
}

export interface AnalysisData {
  draft_id: number;
  retrieved_notices: Notice[];
  analysis: AnalysisResult;
}
