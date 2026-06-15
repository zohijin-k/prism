import { useRef, useState } from "react";

interface Props {
  onSubmit: (paper: File, githubUrl?: string, codeZip?: File) => void;
  loading: boolean;
}

function formatBytes(bytes: number) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

interface FileChipProps {
  file: File;
  onClear: () => void;
}

function FileChip({ file, onClear }: FileChipProps) {
  return (
    <div className="flex items-center gap-2 mt-2 px-3 py-1.5 rounded-md bg-prism-50 border border-prism-200 w-fit max-w-full">
      <svg className="w-3.5 h-3.5 text-prism-600 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
          d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <span className="text-xs text-prism-700 font-medium truncate max-w-[240px]">{file.name}</span>
      <span className="text-xs text-prism-400 shrink-0">{formatBytes(file.size)}</span>
      <button
        type="button"
        onClick={(e) => { e.stopPropagation(); onClear(); }}
        className="ml-1 text-prism-400 hover:text-prism-700 transition-colors shrink-0"
        aria-label="Remove file"
      >
        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  );
}

export default function UploadForm({ onSubmit, loading }: Props) {
  const [paper, setPaper] = useState<File | null>(null);
  const [githubUrl, setGithubUrl] = useState("");
  const [codeZip, setCodeZip] = useState<File | null>(null);
  const [dragging, setDragging] = useState(false);
  const paperRef = useRef<HTMLInputElement>(null);
  const zipRef = useRef<HTMLInputElement>(null);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!paper || loading) return;
    onSubmit(paper, githubUrl.trim() || undefined, codeZip || undefined);
  }

  function handleDrop(e: React.DragEvent) {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0];
    if (file?.type === "application/pdf") setPaper(file);
  }

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-xl border border-gray-200 p-6 space-y-5 shadow-sm">
      {/* PDF upload */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Paper PDF <span className="text-red-400">*</span>
        </label>

        {paper ? (
          <div
            onClick={() => paperRef.current?.click()}
            className="flex flex-col items-center justify-center cursor-pointer rounded-xl border-2 border-prism-300 bg-prism-50 px-6 py-8 transition-colors hover:bg-prism-100"
          >
            <svg className="w-7 h-7 text-prism-500 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <FileChip file={paper} onClear={() => setPaper(null)} />
            <p className="text-xs text-gray-400 mt-2">Click to replace</p>
          </div>
        ) : (
          <div
            onClick={() => paperRef.current?.click()}
            onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
            onDragLeave={() => setDragging(false)}
            onDrop={handleDrop}
            className={`flex flex-col items-center justify-center cursor-pointer rounded-xl border-2 border-dashed px-6 py-10 transition-colors ${
              dragging
                ? "border-prism-400 bg-prism-50"
                : "border-gray-300 hover:border-prism-400 hover:bg-gray-50"
            }`}
          >
            <svg className="w-8 h-8 text-gray-300 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            <p className="text-sm font-medium text-gray-600">Drop PDF here or <span className="text-prism-600">click to browse</span></p>
            <p className="text-xs text-gray-400 mt-1">PDF files only</p>
          </div>
        )}

        <input
          ref={paperRef}
          type="file"
          accept=".pdf"
          className="hidden"
          onChange={(e) => setPaper(e.target.files?.[0] ?? null)}
        />
      </div>

      {/* Divider */}
      <div className="flex items-center gap-3">
        <div className="flex-1 h-px bg-gray-100" />
        <span className="text-xs text-gray-400 font-medium">CODE SOURCE</span>
        <span className="text-xs text-gray-400">(optional)</span>
        <div className="flex-1 h-px bg-gray-100" />
      </div>

      {/* GitHub URL + ZIP in a row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {/* GitHub URL */}
        <div>
          <label className="block text-xs font-medium text-gray-500 mb-1.5 uppercase tracking-wide">
            GitHub Repository URL
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-3 flex items-center pointer-events-none">
              <svg className="w-4 h-4 text-gray-400" fill="currentColor" viewBox="0 0 24 24">
                <path fillRule="evenodd" clipRule="evenodd"
                  d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" />
              </svg>
            </div>
            <input
              type="url"
              placeholder="https://github.com/author/repo"
              value={githubUrl}
              onChange={(e) => setGithubUrl(e.target.value)}
              className="w-full pl-9 pr-3 py-2 rounded-lg border border-gray-200 text-sm text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-prism-500 focus:border-transparent"
            />
          </div>
        </div>

        {/* ZIP */}
        <div>
          <label className="block text-xs font-medium text-gray-500 mb-1.5 uppercase tracking-wide">
            Code ZIP
          </label>
          {codeZip ? (
            <FileChip file={codeZip} onClear={() => setCodeZip(null)} />
          ) : (
            <button
              type="button"
              onClick={() => zipRef.current?.click()}
              className="flex items-center gap-2 w-full px-3 py-2 rounded-lg border border-gray-200 text-sm text-gray-500 hover:border-prism-300 hover:text-prism-600 transition-colors"
            >
              <svg className="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
              </svg>
              Upload ZIP file
            </button>
          )}
          <input
            ref={zipRef}
            type="file"
            accept=".zip"
            className="hidden"
            onChange={(e) => setCodeZip(e.target.files?.[0] ?? null)}
          />
        </div>
      </div>

      {/* Submit */}
      <button
        type="submit"
        disabled={!paper || loading}
        className="w-full flex items-center justify-center gap-2 rounded-lg bg-prism-600 text-white text-sm font-semibold py-2.5 hover:bg-prism-700 active:bg-prism-900 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
      >
        {loading ? (
          <>
            <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            Analyzing…
          </>
        ) : (
          <>
            Analyze Paper
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </>
        )}
      </button>
    </form>
  );
}
