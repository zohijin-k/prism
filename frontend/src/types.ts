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

export interface Components {
  dataset: string;
  model: string;
  backbone: string;
  loss: string;
  optimizer: string;
  metrics: string[];
  hyperparameters: Record<string, string | number>;
}

export type ComparisonStatus = "Match" | "Code Only" | "Paper Only" | "Mismatch";

export interface ComparisonItem {
  item: string;
  paper: string;
  code: string;
  status: ComparisonStatus;
}

export type ConfidenceLevel = "High" | "Medium" | "Low";

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
  comparison: ComparisonItem[];
  mapping: MappingItem[];
  missingInfo: string[];
}
