export interface Contributor {
  key: string;
  kind: "transaction" | "tenant";
  party: string;
  memo: string;
  delta: number;
  share_of_actual?: number;
  share_of_variance?: number;
}

export interface VarianceCase {
  case_id: string;
  month: string;
  property: string;
  pl_line: string;
  side: string;
  budget: number;
  actual: number;
  variance: number;
  variance_pct: number | null;
  direction: string;
  material: boolean;
  materiality_rule: string;
  contributors: Contributor[];
}

export interface EvidenceDoc {
  doc_id: string;
  type: string;
  property: string;
  period: string;
  authority: number;
  title: string;
  text: string;
  bm25_score?: number;
  rrf?: number;
  linked?: boolean;
}

export interface EvidencePack {
  case_id: string;
  docs: EvidenceDoc[];
  best_bm25: number;
  linked_any: boolean;
  dense_used: boolean;
}

export interface GenerationOutput {
  case_id: string;
  mode: string;
  model_id: string;
  prompt_version: string;
  draft_comment: string;
  abstained: boolean;
  observed_facts?: string;
  drivers_confirmed?: Array<{ text: string; evidence_ids: string[] }>;
  drivers_possible?: Array<{ text: string }>;
  offsets?: Array<{ text: string; evidence_ids?: string[] }>;
  forward_note?: string;
}

export interface NumericVerdict {
  raw: string;
  value: number;
  is_pct: boolean;
  approx: boolean;
  signed: boolean;
  matched: string | null;
  ok: boolean;
}

export interface CitationVerdict {
  id: string;
  ok: boolean;
  reason: string;
}

export interface ClaimVerdict {
  text: string;
  supported: boolean;
}

export interface AbstentionVerdict {
  evidence_weak: boolean;
  abstained: boolean;
  ok: boolean;
  over_abstain: boolean;
}

export interface Verdict {
  numbers: NumericVerdict[];
  citations: CitationVerdict[];
  claims: ClaimVerdict[];
  abstention: AbstentionVerdict;
  overall: "verified" | "flagged";
}

export interface CaseRecords {
  case_id: string;
  records: Record<string, Record<number, { output: GenerationOutput; verdict: Verdict | null }>>;
}

export interface MetaInfo {
  dataset_version: string;
  model: string;
  prompt_version: string;
  materiality: Record<string, { abs: number; pct: number }>;
  months: string[];
  properties: string[];
}

export type StepId = 1 | 2 | 3 | 4 | 5;

export const STEP_LABELS: Record<StepId, string> = {
  1: "Tổng quan",
  2: "Bằng chứng",
  3: "Giải trình",
  4: "Kiểm chứng",
  5: "Quyết định",
};
