import { Fragment } from "react";
import { ComparisonItem, ComparisonStatus, RepoAnalysis } from "../../types";

interface Props {
  items: ComparisonItem[];
  repoAnalysis: RepoAnalysis;
}

const statusStyles: Record<ComparisonStatus, string> = {
  Match: "bg-green-100 text-green-700",
  "Partial Match": "bg-yellow-100 text-yellow-700",
  Mismatch: "bg-red-100 text-red-700",
  "Paper Only": "bg-blue-100 text-blue-700",
  "Code Only": "bg-purple-100 text-purple-700",
  Unknown: "bg-gray-100 text-gray-500",
};

const SUMMARY_STATS: { status: ComparisonStatus; label: string; color: string }[] = [
  { status: "Match", label: "Matches", color: "text-green-600" },
  { status: "Partial Match", label: "Partial", color: "text-yellow-600" },
  { status: "Mismatch", label: "Mismatch", color: "text-red-600" },
  { status: "Unknown", label: "Unknown", color: "text-gray-500" },
];

const INPUT_TYPE_LABELS: Record<RepoAnalysis["inputType"], string> = {
  github: "GitHub URL",
  zip: "ZIP Upload",
  none: "None",
};

const HINT_GROUPS: { key: keyof Omit<RepoAnalysis["codeHints"], "config">; label: string }[] = [
  { key: "models", label: "Models" },
  { key: "backbones", label: "Backbones" },
  { key: "losses", label: "Losses" },
  { key: "optimizers", label: "Optimizers" },
  { key: "datasets", label: "Datasets" },
  { key: "metrics", label: "Metrics" },
];

function RepoAnalysisCard({ repoAnalysis }: { repoAnalysis: RepoAnalysis }) {
  const { inputType, repoName, status, fileCount, codeHints } = repoAnalysis;
  const hasHints =
    HINT_GROUPS.some((g) => codeHints[g.key].length > 0) || Object.keys(codeHints.config).length > 0;

  return (
    <div className="rounded-lg border border-gray-200 p-4 space-y-3 mb-4">
      <div className="flex items-center justify-between flex-wrap gap-2">
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold uppercase tracking-wide text-gray-400">
            Repository / Code Source
          </span>
          <span className="px-2 py-0.5 rounded-full bg-gray-100 text-gray-600 text-xs font-medium">
            {INPUT_TYPE_LABELS[inputType]}
          </span>
        </div>
        {inputType !== "none" && (
          <span className="text-xs text-gray-400">{fileCount} relevant file{fileCount === 1 ? "" : "s"}</span>
        )}
      </div>

      {repoName && <p className="text-sm font-medium text-gray-800">{repoName}</p>}
      <p className={`text-sm ${inputType === "github" ? "text-yellow-700" : "text-gray-600"}`}>{status}</p>

      {hasHints && (
        <div className="flex flex-wrap gap-x-6 gap-y-2 pt-1">
          {HINT_GROUPS.map(({ key, label }) =>
            codeHints[key].length > 0 ? (
              <div key={key}>
                <span className="text-[11px] font-semibold uppercase tracking-wide text-gray-400 mr-1.5">
                  {label}:
                </span>
                {codeHints[key].map((v) => (
                  <span
                    key={v}
                    className="inline-block mr-1.5 px-2 py-0.5 rounded-full bg-prism-100 text-prism-700 text-xs font-medium"
                  >
                    {v}
                  </span>
                ))}
              </div>
            ) : null
          )}
          {Object.keys(codeHints.config).length > 0 && (
            <div>
              <span className="text-[11px] font-semibold uppercase tracking-wide text-gray-400 mr-1.5">
                Config:
              </span>
              {Object.entries(codeHints.config).map(([k, v]) => (
                <span
                  key={k}
                  className="inline-block mr-1.5 px-2 py-0.5 rounded-full bg-gray-100 text-gray-600 text-xs font-medium"
                >
                  {k}={v}
                </span>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function AlignmentSummary({ items }: { items: ComparisonItem[] }) {
  const counts: Record<ComparisonStatus, number> = {
    Match: 0,
    "Partial Match": 0,
    Mismatch: 0,
    "Paper Only": 0,
    "Code Only": 0,
    Unknown: 0,
  };
  items.forEach((item) => {
    counts[item.status] += 1;
  });
  const extra = counts["Paper Only"] + counts["Code Only"];

  return (
    <div className="rounded-lg border border-gray-200 p-4 mb-4">
      <h3 className="text-xs font-semibold uppercase tracking-wide text-gray-400 mb-3">Paper-Code Alignment</h3>
      <div className="grid grid-cols-4 gap-3">
        {SUMMARY_STATS.map(({ status, label, color }) => (
          <div key={status}>
            <p className={`text-xl font-bold ${color}`}>{counts[status]}</p>
            <p className="text-xs text-gray-500">{label}</p>
          </div>
        ))}
      </div>
      {extra > 0 && (
        <p className="text-xs text-gray-400 mt-3">
          {counts["Paper Only"]} paper-only · {counts["Code Only"]} code-only
        </p>
      )}
    </div>
  );
}

export default function ComparisonTab({ items, repoAnalysis }: Props) {
  return (
    <div>
      <RepoAnalysisCard repoAnalysis={repoAnalysis} />
      <AlignmentSummary items={items} />
      <div className="overflow-x-auto rounded-lg border border-gray-200">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-gray-50 text-left">
              <th className="px-4 py-3 font-semibold text-gray-600 w-1/4">Item</th>
              <th className="px-4 py-3 font-semibold text-gray-600 w-1/4">Paper</th>
              <th className="px-4 py-3 font-semibold text-gray-600 w-1/4">Code</th>
              <th className="px-4 py-3 font-semibold text-gray-600 w-1/4">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {items.map((item, i) => (
              <Fragment key={i}>
                <tr className="hover:bg-gray-50 transition-colors">
                  <td className="px-4 py-3 font-medium text-gray-800 align-top">{item.item}</td>
                  <td className="px-4 py-3 text-gray-600 align-top">{item.paper}</td>
                  <td className="px-4 py-3 text-gray-600 align-top">{item.code}</td>
                  <td className="px-4 py-3 align-top">
                    <span className={`inline-block px-2 py-0.5 rounded-full text-xs font-semibold ${statusStyles[item.status]}`}>
                      {item.status}
                    </span>
                  </td>
                </tr>
                <tr className="bg-gray-50/60">
                  <td colSpan={4} className="px-4 pb-3 pt-0 text-xs text-gray-400">
                    {item.explanation}
                  </td>
                </tr>
              </Fragment>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
