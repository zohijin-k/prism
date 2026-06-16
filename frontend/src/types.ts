export interface SectionInfo {
  header: string;
  char_count: number;
  preview: string;
}

export interface PaperSections {
  detected: Record<string, SectionInfo>;
  total_chars: number;
}

export interface PaperInfo {
  filename: string;
  page_count: number;
  text_preview: string;
  extraction_error: string | null;
  sections: PaperSections;
}

export interface PaperSummary {
  problem: string;
  limitation: string;
  method: string;
  result: string;
  contribution: string[];
}

export type ConfidenceLevel = "High" | "Medium" | "Low";

export interface ComponentField {
  value: string;
  source: string | null;
  confidence: ConfidenceLevel;
  found: boolean;
  matchedSentence?: string | null;
  score?: number | null;
}

export interface MetricsField {
  value: string[];
  source: string | null;
  confidence: ConfidenceLevel;
  found: boolean;
  matchedSentence?: string | null;
  score?: number | null;
}

export interface HyperparametersField {
  value: Record<string, string>;
  source: string | null;
  confidence: ConfidenceLevel;
  found: boolean;
  matchedSentence?: string | null;
  score?: number | null;
}

export interface Components {
  dataset: ComponentField;
  model: ComponentField;
  backbone: ComponentField;
  loss: ComponentField;
  optimizer: ComponentField;
  metrics: MetricsField;
  hyperparameters: HyperparametersField;
}

export type RepoInputType = "github" | "zip" | "none";

export interface CodeHints {
  models: string[];
  backbones: string[];
  losses: string[];
  optimizers: string[];
  datasets: string[];
  metrics: string[];
  config: Record<string, string>;
}

export interface RepoAnalysis {
  inputType: RepoInputType;
  repoName: string | null;
  status: string;
  relevantFiles: string[];
  fileCount: number;
  codeHints: CodeHints;
}

export type ComparisonStatus = "Match" | "Partial Match" | "Mismatch" | "Paper Only" | "Code Only" | "Unknown";

export interface ComparisonItem {
  item: string;
  paper: string;
  code: string;
  status: ComparisonStatus;
  confidence: ConfidenceLevel;
  explanation: string;
}

export interface MappingItem {
  codeBlock: string;
  paperSection: string;
  paperReference: string;
  explanation: string;
  confidence: ConfidenceLevel;
}

export interface AnalysisResult {
  paperInfo: PaperInfo | null;
  summary: PaperSummary;
  implementationPlan: string[];
  components: Components;
  repoAnalysis: RepoAnalysis;
  comparison: ComparisonItem[];
  mapping: MappingItem[];
  missingInfo: string[];
}
