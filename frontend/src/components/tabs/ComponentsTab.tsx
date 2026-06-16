import { ReactNode } from "react";
import {
  ComponentField,
  Components,
  ConfidenceLevel,
  HyperparametersField,
  MetricsField,
} from "../../types";

interface Props {
  components: Components;
}

const CONFIDENCE_STYLES: Record<ConfidenceLevel, string> = {
  High: "bg-green-100 text-green-700",
  Medium: "bg-yellow-100 text-yellow-700",
  Low: "bg-gray-100 text-gray-500",
};

const SECTION_LABELS: Record<string, string> = {
  abstract: "Abstract",
  introduction: "Introduction",
  related_work: "Related Work",
  method: "Method",
  experiments: "Experiments",
  results: "Results",
  conclusion: "Conclusion",
};

function sourceLabel(source: string | null): string {
  if (!source) return "full text";
  return SECTION_LABELS[source] ?? source;
}

function FieldShell({
  label,
  confidence,
  source,
  found,
  children,
}: {
  label: string;
  confidence: ConfidenceLevel;
  source: string | null;
  found: boolean;
  children: ReactNode;
}) {
  return (
    <div className="rounded-lg border border-gray-200 p-4 space-y-2">
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold uppercase tracking-wide text-gray-400">{label}</span>
        <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${CONFIDENCE_STYLES[confidence]}`}>
          {confidence}
        </span>
      </div>
      {children}
      {found && (
        <p className="text-[11px] text-gray-400">
          Source: <span className="font-medium text-gray-500">{sourceLabel(source)}</span>
        </p>
      )}
    </div>
  );
}

function ScalarField({ label, field }: { label: string; field: ComponentField }) {
  return (
    <FieldShell label={label} confidence={field.confidence} source={field.source} found={field.found}>
      {field.found ? (
        <p className="text-sm text-gray-800">{field.value}</p>
      ) : (
        <div>
          <p className="text-sm text-gray-400 italic">Not found in paper</p>
          <p className="text-xs text-gray-400 mt-0.5">Default: {field.value}</p>
        </div>
      )}
    </FieldShell>
  );
}

function MetricsCard({ field }: { field: MetricsField }) {
  return (
    <FieldShell label="Metrics" confidence={field.confidence} source={field.source} found={field.found}>
      {!field.found && <p className="text-sm text-gray-400 italic">Not found in paper — showing defaults</p>}
      <div className="flex flex-wrap gap-1.5">
        {field.value.map((m) => (
          <span
            key={m}
            className={`px-2 py-0.5 rounded-full text-xs font-medium ${
              field.found ? "bg-prism-100 text-prism-700" : "bg-gray-100 text-gray-400"
            }`}
          >
            {m}
          </span>
        ))}
      </div>
    </FieldShell>
  );
}

function HyperparametersCard({ field }: { field: HyperparametersField }) {
  const entries = Object.entries(field.value);
  return (
    <FieldShell label="Hyperparameters" confidence={field.confidence} source={field.source} found={field.found}>
      {!field.found && <p className="text-sm text-gray-400 italic mb-1">Not found in paper — showing defaults</p>}
      <div className="rounded-md border border-gray-100 overflow-hidden">
        <table className="w-full text-sm">
          <tbody>
            {entries.map(([k, v], i) => (
              <tr key={k} className={i % 2 === 0 ? "bg-gray-50" : "bg-white"}>
                <td className="px-3 py-1.5 font-medium text-gray-600 w-1/2">{k}</td>
                <td className={`px-3 py-1.5 ${field.found ? "text-gray-800" : "text-gray-400"}`}>{v}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </FieldShell>
  );
}

export default function ComponentsTab({ components }: Props) {
  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <ScalarField label="Dataset" field={components.dataset} />
        <ScalarField label="Model" field={components.model} />
        <ScalarField label="Backbone" field={components.backbone} />
        <ScalarField label="Loss" field={components.loss} />
        <ScalarField label="Optimizer" field={components.optimizer} />
      </div>
      <MetricsCard field={components.metrics} />
      <HyperparametersCard field={components.hyperparameters} />
    </div>
  );
}
