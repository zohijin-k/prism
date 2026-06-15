import { AnalysisResult } from "./types";

export async function analyzePaper(
  paper: File,
  githubUrl?: string,
  codeZip?: File
): Promise<AnalysisResult> {
  const form = new FormData();
  form.append("paper", paper);
  if (githubUrl) form.append("github_url", githubUrl);
  if (codeZip) form.append("code_zip", codeZip);

  const res = await fetch("/api/analyze", { method: "POST", body: form });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Analysis failed (${res.status}): ${text}`);
  }

  return res.json() as Promise<AnalysisResult>;
}
