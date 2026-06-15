import { ConfidenceLevel, MappingItem } from "../../types";

interface Props {
  items: MappingItem[];
}

const confidenceStyles: Record<ConfidenceLevel, string> = {
  High: "bg-green-100 text-green-700",
  Medium: "bg-yellow-100 text-yellow-700",
  Low: "bg-red-100 text-red-700",
};

export default function MappingTab({ items }: Props) {
  return (
    <div className="space-y-4">
      {items.map((item, i) => (
        <div key={i} className="rounded-lg border border-gray-200 p-4 space-y-2">
          <div className="flex items-start justify-between gap-3">
            <code className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded font-mono break-all">
              {item.codeBlock}
            </code>
            <span className={`flex-shrink-0 px-2 py-0.5 rounded-full text-xs font-semibold ${confidenceStyles[item.confidence]}`}>
              {item.confidence}
            </span>
          </div>

          <div className="flex items-center gap-2 text-xs text-gray-500">
            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <span className="font-medium text-gray-600">{item.paperSection}</span>
            <span>·</span>
            <span>{item.paperReference}</span>
          </div>

          <p className="text-sm text-gray-700">{item.explanation}</p>
        </div>
      ))}
    </div>
  );
}
