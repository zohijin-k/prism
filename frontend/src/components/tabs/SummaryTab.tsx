import { PaperInfo, PaperSummary } from "../../types";

interface Props {
  summary: PaperSummary;
  paperInfo: PaperInfo | null;
}

const FIELDS: { key: keyof Omit<PaperSummary, "contribution">; label: string; color: string }[] = [
  { key: "problem",    label: "Problem",    color: "bg-red-50 border-red-200 text-red-800" },
  { key: "limitation", label: "Limitation", color: "bg-yellow-50 border-yellow-200 text-yellow-800" },
  { key: "method",     label: "Method",     color: "bg-blue-50 border-blue-200 text-blue-800" },
  { key: "result",     label: "Result",     color: "bg-green-50 border-green-200 text-green-800" },
];

function PaperInfoCard({ info }: { info: PaperInfo }) {
  if (info.extraction_error) {
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 flex gap-3">
        <svg className="w-4 h-4 text-red-500 mt-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div>
          <p className="text-sm font-medium text-red-800">PDF extraction failed</p>
          <p className="text-xs text-red-600 mt-0.5">{info.extraction_error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-lg border border-gray-200 bg-gray-50 overflow-hidden">
      {/* header row */}
      <div className="flex items-center gap-3 px-4 py-3 border-b border-gray-200">
        <svg className="w-4 h-4 text-gray-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <span className="text-sm font-medium text-gray-700 truncate flex-1">{info.filename}</span>
        <span className="text-xs text-gray-400 shrink-0">
          {info.page_count} {info.page_count === 1 ? "page" : "pages"}
        </span>
      </div>

      {/* preview */}
      <div className="px-4 py-3">
        <p className="text-[10px] font-semibold uppercase tracking-widest text-gray-400 mb-2">
          Extracted text preview
        </p>
        <p className="text-xs text-gray-600 leading-relaxed font-mono whitespace-pre-wrap break-words max-h-32 overflow-y-auto">
          {info.text_preview}
        </p>
      </div>
    </div>
  );
}

export default function SummaryTab({ summary, paperInfo }: Props) {
  return (
    <div className="space-y-6">
      {paperInfo && <PaperInfoCard info={paperInfo} />}

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {FIELDS.map(({ key, label, color }) => (
          <div key={key} className={`rounded-lg border px-4 py-3 ${color}`}>
            <p className="text-[10px] font-bold uppercase tracking-widest opacity-60 mb-1">{label}</p>
            <p className="text-sm leading-relaxed">{summary[key]}</p>
          </div>
        ))}
      </div>

      <div>
        <p className="text-xs font-semibold uppercase tracking-wide text-gray-400 mb-3">Contributions</p>
        <ul className="space-y-2">
          {summary.contribution.map((c, i) => (
            <li key={i} className="flex items-start gap-3 text-sm text-gray-800">
              <span className="mt-0.5 flex-shrink-0 w-5 h-5 rounded-full bg-prism-100 text-prism-700 text-[11px] font-bold flex items-center justify-center">
                {i + 1}
              </span>
              <span className="leading-relaxed">{c}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
