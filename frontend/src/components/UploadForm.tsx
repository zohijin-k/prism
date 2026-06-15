import { useRef, useState } from "react";

interface Props {
  onSubmit: (paper: File, githubUrl?: string, codeZip?: File) => void;
  loading: boolean;
}

export default function UploadForm({ onSubmit, loading }: Props) {
  const [paper, setPaper] = useState<File | null>(null);
  const [githubUrl, setGithubUrl] = useState("");
  const [codeZip, setCodeZip] = useState<File | null>(null);
  const paperRef = useRef<HTMLInputElement>(null);
  const zipRef = useRef<HTMLInputElement>(null);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!paper) return;
    onSubmit(paper, githubUrl || undefined, codeZip || undefined);
  }

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-xl border border-gray-200 p-6 space-y-5">
      <h2 className="text-base font-semibold text-gray-800">Analyze a Paper</h2>

      {/* PDF upload */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1.5">
          Paper PDF <span className="text-red-500">*</span>
        </label>
        <div
          onClick={() => paperRef.current?.click()}
          className="flex items-center gap-3 cursor-pointer rounded-lg border-2 border-dashed border-gray-300 hover:border-prism-400 transition-colors px-4 py-5"
        >
          <svg className="w-5 h-5 text-gray-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
              d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
          </svg>
          <span className="text-sm text-gray-500">
            {paper ? paper.name : "Click to upload PDF"}
          </span>
        </div>
        <input
          ref={paperRef}
          type="file"
          accept=".pdf"
          className="hidden"
          onChange={(e) => setPaper(e.target.files?.[0] ?? null)}
        />
      </div>

      {/* GitHub URL */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1.5">
          GitHub Repository URL <span className="text-gray-400 font-normal">(optional)</span>
        </label>
        <input
          type="url"
          placeholder="https://github.com/author/repo"
          value={githubUrl}
          onChange={(e) => setGithubUrl(e.target.value)}
          className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-prism-500 focus:border-transparent"
        />
      </div>

      {/* ZIP upload */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1.5">
          Code ZIP <span className="text-gray-400 font-normal">(optional)</span>
        </label>
        <div
          onClick={() => zipRef.current?.click()}
          className="flex items-center gap-3 cursor-pointer rounded-lg border-2 border-dashed border-gray-300 hover:border-prism-400 transition-colors px-4 py-3"
        >
          <svg className="w-5 h-5 text-gray-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
              d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
          </svg>
          <span className="text-sm text-gray-500">
            {codeZip ? codeZip.name : "Click to upload ZIP"}
          </span>
        </div>
        <input
          ref={zipRef}
          type="file"
          accept=".zip"
          className="hidden"
          onChange={(e) => setCodeZip(e.target.files?.[0] ?? null)}
        />
      </div>

      <button
        type="submit"
        disabled={!paper || loading}
        className="w-full rounded-lg bg-prism-600 text-white text-sm font-medium py-2.5 hover:bg-prism-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? "Analyzing…" : "Analyze"}
      </button>
    </form>
  );
}
