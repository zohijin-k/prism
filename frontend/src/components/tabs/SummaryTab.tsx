import { PaperSummary } from "../../types";

interface Props {
  summary: PaperSummary;
}

const fields: { key: keyof Omit<PaperSummary, "contribution">; label: string }[] = [
  { key: "problem", label: "Problem" },
  { key: "limitation", label: "Limitation" },
  { key: "method", label: "Method" },
  { key: "result", label: "Result" },
];

export default function SummaryTab({ summary }: Props) {
  return (
    <div className="space-y-5">
      {fields.map(({ key, label }) => (
        <div key={key}>
          <dt className="text-xs font-semibold uppercase tracking-wide text-gray-400 mb-1">{label}</dt>
          <dd className="text-sm text-gray-800">{summary[key]}</dd>
        </div>
      ))}

      <div>
        <dt className="text-xs font-semibold uppercase tracking-wide text-gray-400 mb-2">Contributions</dt>
        <ul className="space-y-1.5">
          {summary.contribution.map((c, i) => (
            <li key={i} className="flex items-start gap-2 text-sm text-gray-800">
              <span className="mt-0.5 flex-shrink-0 w-5 h-5 rounded-full bg-prism-100 text-prism-700 text-xs font-semibold flex items-center justify-center">
                {i + 1}
              </span>
              {c}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
