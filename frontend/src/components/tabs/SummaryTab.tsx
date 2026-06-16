import { PaperInfo, PaperSections, PaperSummary, SectionInfo } from "../../types";

interface Props {
  summary: PaperSummary;
  paperInfo: PaperInfo | null;
}

// Canonical display order — matches backend SECTION_ORDER
const CANONICAL_SECTIONS: { key: string; label: string }[] = [
  { key: "abstract",     label: "Abstract" },
  { key: "introduction", label: "Introduction" },
  { key: "related_work", label: "Related Work" },
  { key: "method",       label: "Method / Approach" },
  { key: "experiments",  label: "Experiments" },
  { key: "results",      label: "Results" },
  { key: "conclusion",   label: "Conclusion" },
];

function fmtChars(n: number): string {
  if (n >= 1000) return `${(n / 1000).toFixed(1)}K`;
  return `${n}`;
}

function PaperStructureCard({ sections }: { sections: PaperSections }) {
  const detectedCount = Object.keys(sections.detected).length;

  return (
    <div className="rounded-lg border border-gray-200 overflow-hidden">
      {/* header */}
      <div className="flex items-center justify-between px-4 py-3 bg-gray-50 border-b border-gray-200">
        <div className="flex items-center gap-2">
          <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
              d="M4 6h16M4 10h16M4 14h10M4 18h6" />
          </svg>
          <span className="text-sm font-semibold text-gray-700">Paper Structure</span>
        </div>
        <span className="text-xs text-gray-400">
          {detectedCount}/{CANONICAL_SECTIONS.length} sections detected
          {sections.total_chars > 0 && (
            <> · {fmtChars(sections.total_chars)} chars total</>
          )}
        </span>
      </div>

      {/* section rows */}
      <ul className="divide-y divide-gray-100">
        {CANONICAL_SECTIONS.map(({ key, label }) => {
          const info: SectionInfo | undefined = sections.detected[key];
          return (
            <li key={key} className="flex items-center gap-3 px-4 py-2.5">
              {/* dot indicator */}
              <span
                className={`flex-shrink-0 w-2 h-2 rounded-full ${
                  info ? "bg-prism-500" : "bg-gray-200"
                }`}
              />

              {/* section label */}
              <span
                className={`flex-1 text-sm ${
                  info ? "text-gray-800 font-medium" : "text-gray-400"
                }`}
              >
                {info ? info.header : label}
              </span>

              {/* char count badge */}
              {info ? (
                <span className="text-xs font-mono text-prism-600 bg-prism-50 px-2 py-0.5 rounded shrink-0">
                  {fmtChars(info.char_count)} chars
                </span>
              ) : (
                <span className="text-xs text-gray-300 shrink-0">not detected</span>
              )}
            </li>
          );
        })}
      </ul>
    </div>
  );
}

const SUMMARY_FIELDS: { key: keyof Omit<PaperSummary, "contribution">; label: string; color: string }[] = [
  { key: "problem",    label: "핵심 문제",  color: "bg-red-50 border-red-200 text-red-800" },
  { key: "limitation", label: "연구 한계",  color: "bg-yellow-50 border-yellow-200 text-yellow-800" },
  { key: "method",     label: "제안 방법",  color: "bg-blue-50 border-blue-200 text-blue-800" },
  { key: "result",     label: "실험 결과",  color: "bg-green-50 border-green-200 text-green-800" },
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
      {/* Real PDF data */}
      {paperInfo && (
        <>
          <PaperStructureCard sections={paperInfo.sections} />
          <PaperInfoCard info={paperInfo} />
        </>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {SUMMARY_FIELDS.map(({ key, label, color }) => (
          <div key={key} className={`rounded-lg border px-4 py-3 ${color}`}>
            <p className="text-[10px] font-bold uppercase tracking-widest opacity-60 mb-1">{label}</p>
            <p className="text-sm leading-relaxed">{summary[key]}</p>
          </div>
        ))}
      </div>

      <div>
        <p className="text-xs font-semibold uppercase tracking-wide text-gray-400 mb-3">주요 기여점</p>
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
