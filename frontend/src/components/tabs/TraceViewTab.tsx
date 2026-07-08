import { useMemo, useState } from "react";
import { ConfidenceLevel, MappingItem, PaperInfo, RepoAnalysis } from "../../types";

interface Props {
  mapping: MappingItem[];
  paperInfo: PaperInfo | null;
  repoAnalysis: RepoAnalysis;
}

// Canonical display order — matches backend paper_parser.SECTION_ORDER / mapping_engine.SECTION_DISPLAY
const CANONICAL_SECTIONS: { key: string; label: string }[] = [
  { key: "abstract", label: "Abstract" },
  { key: "introduction", label: "Introduction" },
  { key: "related_work", label: "Related Work" },
  { key: "method", label: "Method" },
  { key: "implementation_details", label: "Implementation Details" },
  { key: "experiments", label: "Experiments" },
  { key: "results", label: "Results" },
  { key: "conclusion", label: "Conclusion" },
];

const CONFIDENCE_STYLES: Record<ConfidenceLevel, string> = {
  High: "bg-green-100 text-green-700",
  Medium: "bg-yellow-100 text-yellow-700",
  Low: "bg-red-100 text-red-700",
};

// Mapping items whose paperSection isn't one of the canonical labels above — the mapping
// engine couldn't tie them to a specific section, so they can't be filtered by clicking one.
const UNLINKED = "__unlinked__";

function MappingCard({
  item,
  expanded,
  onToggle,
}: {
  item: MappingItem;
  expanded: boolean;
  onToggle: () => void;
}) {
  return (
    <div className="rounded-lg border border-gray-200 overflow-hidden">
      <button
        type="button"
        onClick={onToggle}
        className="w-full flex items-center gap-3 px-4 py-3 text-left hover:bg-gray-50 transition-colors"
      >
        <svg
          className={`w-3.5 h-3.5 text-gray-400 shrink-0 transition-transform ${expanded ? "rotate-90" : ""}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
        </svg>
        <code className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded font-mono break-all flex-1">
          {item.codeBlock}
        </code>
        <span className="text-xs text-gray-400 shrink-0 hidden sm:inline">{item.paperSection}</span>
        <span
          className={`shrink-0 px-2 py-0.5 rounded-full text-xs font-semibold ${CONFIDENCE_STYLES[item.confidence]}`}
        >
          {item.confidence}
        </span>
      </button>
      {expanded && (
        <div className="px-4 pb-4 pt-1 space-y-2 border-t border-gray-100 bg-gray-50/60">
          <p className="text-sm text-gray-700 leading-relaxed">{item.explanation}</p>
          <p className="text-xs text-gray-500">
            <span className="font-semibold text-gray-600">Reference:</span> {item.paperReference}
          </p>
          {item.evidenceSentence && (
            <p className="text-xs text-gray-500 italic">
              <span className="font-semibold not-italic text-gray-600">Evidence:</span> "{item.evidenceSentence}"
            </p>
          )}
        </div>
      )}
    </div>
  );
}

export default function TraceViewTab({ mapping, paperInfo, repoAnalysis }: Props) {
  const [selected, setSelected] = useState<string | null>(null);
  const [expanded, setExpanded] = useState<Set<number>>(new Set());

  const canonicalLabels = useMemo(() => new Set(CANONICAL_SECTIONS.map((s) => s.label)), []);

  const indexed = useMemo(() => mapping.map((item, idx) => ({ item, idx })), [mapping]);

  const counts = useMemo(() => {
    const c: Record<string, number> = {};
    mapping.forEach((m) => {
      const key = canonicalLabels.has(m.paperSection) ? m.paperSection : UNLINKED;
      c[key] = (c[key] || 0) + 1;
    });
    return c;
  }, [mapping, canonicalLabels]);

  const filtered =
    selected == null
      ? indexed
      : selected === UNLINKED
      ? indexed.filter(({ item }) => !canonicalLabels.has(item.paperSection))
      : indexed.filter(({ item }) => item.paperSection === selected);

  function toggle(idx: number) {
    setExpanded((prev) => {
      const next = new Set(prev);
      if (next.has(idx)) next.delete(idx);
      else next.add(idx);
      return next;
    });
  }

  if (mapping.length === 0) {
    return (
      <div className="rounded-lg border border-dashed border-gray-200 p-8 text-center">
        <p className="text-sm text-gray-500">
          {repoAnalysis.inputType === "none"
            ? "No code source provided — add a GitHub repo or ZIP upload to trace paper sections to their implementation."
            : "No paper-code mappings were found in the provided repository."}
        </p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-[220px_1fr] gap-4">
      {/* Left: paper sections */}
      <div className="rounded-lg border border-gray-200 overflow-hidden self-start">
        <div className="px-3 py-2.5 bg-gray-50 border-b border-gray-200">
          <span className="text-xs font-semibold uppercase tracking-wide text-gray-400">Paper Sections</span>
        </div>
        <ul className="divide-y divide-gray-100">
          <li>
            <button
              type="button"
              onClick={() => setSelected(null)}
              className={`w-full flex items-center justify-between px-3 py-2 text-left text-sm transition-colors ${
                selected === null ? "bg-prism-50 text-prism-700 font-medium" : "text-gray-600 hover:bg-gray-50"
              }`}
            >
              All sections
              <span className="text-xs text-gray-400">{mapping.length}</span>
            </button>
          </li>
          {CANONICAL_SECTIONS.map(({ key, label }) => {
            const detected = paperInfo?.sections.detected[key];
            const count = counts[label] || 0;
            if (!detected && count === 0) return null;
            return (
              <li key={key}>
                <button
                  type="button"
                  onClick={() => count > 0 && setSelected(label)}
                  disabled={count === 0}
                  className={`w-full flex items-center justify-between px-3 py-2 text-left text-sm transition-colors ${
                    selected === label
                      ? "bg-prism-50 text-prism-700 font-medium"
                      : count === 0
                      ? "text-gray-300 cursor-not-allowed"
                      : "text-gray-600 hover:bg-gray-50"
                  }`}
                >
                  {label}
                  <span className="text-xs text-gray-400">{count || "–"}</span>
                </button>
              </li>
            );
          })}
          {counts[UNLINKED] > 0 && (
            <li>
              <button
                type="button"
                onClick={() => setSelected(UNLINKED)}
                className={`w-full flex items-center justify-between px-3 py-2 text-left text-sm transition-colors ${
                  selected === UNLINKED ? "bg-prism-50 text-prism-700 font-medium" : "text-gray-600 hover:bg-gray-50"
                }`}
              >
                Not linked to a section
                <span className="text-xs text-gray-400">{counts[UNLINKED]}</span>
              </button>
            </li>
          )}
        </ul>
      </div>

      {/* Right: mapped code blocks */}
      <div className="space-y-3">
        {filtered.map(({ item, idx }) => (
          <MappingCard key={idx} item={item} expanded={expanded.has(idx)} onToggle={() => toggle(idx)} />
        ))}
      </div>
    </div>
  );
}
