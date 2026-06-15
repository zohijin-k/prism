import { useEffect, useRef, useState } from "react";
import { analyzePaper } from "./api";
import { AnalysisResult } from "./types";
import UploadForm from "./components/UploadForm";
import ResultTabs from "./components/ResultTabs";

export default function App() {
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const resultsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (result) {
      resultsRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [result]);

  async function handleSubmit(paper: File, githubUrl?: string, codeZip?: File) {
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
    <div className="min-h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-6 h-14 flex items-center gap-3">
          <div className="flex items-center justify-center w-7 h-7 rounded-md bg-prism-600 shrink-0">
            <svg viewBox="0 0 20 20" className="w-4 h-4 text-white fill-current">
              <polygon points="10,2 2,17 18,17" />
            </svg>
          </div>
          <span className="font-semibold text-gray-900 tracking-tight">PRISM</span>
          <span className="text-gray-300 select-none">·</span>
          <span className="text-sm text-gray-500 hidden sm:block">
            Paper Reproduction &amp; Implementation Specification Manager
          </span>
        </div>
      </header>

      <main className="flex-1 max-w-4xl w-full mx-auto px-6 pb-16">
        {/* Hero */}
        <section className="pt-10 pb-8">
          <h2 className="text-2xl font-bold text-gray-900 tracking-tight">
            Analyze a research paper
          </h2>
          <p className="mt-1.5 text-sm text-gray-500 max-w-lg">
            Upload a PDF and optionally link a GitHub repo or ZIP. PRISM returns a
            structured breakdown: summary, implementation plan, components, paper-code
            alignment, and reproducibility gaps.
          </p>
        </section>

        <UploadForm onSubmit={handleSubmit} loading={loading} />

        {/* Error */}
        {error && (
          <div className="mt-6 flex gap-3 rounded-lg border border-red-200 bg-red-50 px-4 py-3">
            <svg className="w-4 h-4 text-red-500 mt-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p className="text-sm text-red-700">{error}</p>
          </div>
        )}

        {/* Loading */}
        {loading && (
          <div className="mt-8 flex flex-col items-center gap-4 py-16">
            <div className="relative w-10 h-10">
              <div className="absolute inset-0 rounded-full border-4 border-prism-100" />
              <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-prism-600 animate-spin" />
            </div>
            <div className="text-center">
              <p className="text-sm font-medium text-gray-700">Analyzing paper…</p>
              <p className="text-xs text-gray-400 mt-0.5">This usually takes a few seconds</p>
            </div>
          </div>
        )}

        {/* Results */}
        {result && (
          <div ref={resultsRef} className="mt-8 scroll-mt-20">
            <ResultTabs result={result} />
          </div>
        )}
      </main>
    </div>
  );
}
