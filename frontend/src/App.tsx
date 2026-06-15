import { useState } from "react";
import { analyzePaper } from "./api";
import { AnalysisResult } from "./types";
import UploadForm from "./components/UploadForm";
import ResultTabs from "./components/ResultTabs";

export default function App() {
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(
    paper: File,
    githubUrl?: string,
    codeZip?: File
  ) {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await analyzePaper(paper, githubUrl, codeZip);
      setResult(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-white border-b border-gray-200 px-6 py-4 flex items-center gap-3">
        <div className="flex items-center justify-center w-9 h-9 rounded-lg bg-prism-600">
          <svg viewBox="0 0 24 24" className="w-5 h-5 text-white fill-current">
            <path d="M12 2L2 19h20L12 2zm0 3.5L19.5 18h-15L12 5.5z" />
          </svg>
        </div>
        <div>
          <h1 className="text-lg font-semibold tracking-tight text-gray-900">PRISM</h1>
          <p className="text-xs text-gray-500 leading-none">
            Paper Reproduction & Implementation Specification Manager
          </p>
        </div>
      </header>

      <main className="flex-1 max-w-4xl w-full mx-auto px-6 py-10 space-y-10">
        <UploadForm onSubmit={handleSubmit} loading={loading} />

        {error && (
          <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {error}
          </div>
        )}

        {loading && (
          <div className="flex flex-col items-center gap-3 py-16 text-gray-500">
            <div className="w-8 h-8 border-4 border-prism-200 border-t-prism-600 rounded-full animate-spin" />
            <p className="text-sm">Analyzing paper…</p>
          </div>
        )}

        {result && <ResultTabs result={result} />}
      </main>
    </div>
  );
}
