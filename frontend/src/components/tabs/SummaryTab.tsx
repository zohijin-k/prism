import { PaperSummary } from "../../types";

interface Props {
  summary: PaperSummary;
}

const FIELDS: { key: keyof Omit<PaperSummary, "contribution">; label: string; color: string }[] = [
  { key: "problem",    label: "Problem",    color: "bg-red-50 border-red-200 text-red-800" },
  { key: "limitation", label: "Limitation", color: "bg-yellow-50 border-yellow-200 text-yellow-800" },
  { key: "method",     label: "Method",     color: "bg-blue-50 border-blue-200 text-blue-800" },
  { key: "result",     label: "Result",     color: "bg-green-50 border-green-200 text-green-800" },
];

export default function SummaryTab({ summary }: Props) {
  return (
    <div className="space-y-6">
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
