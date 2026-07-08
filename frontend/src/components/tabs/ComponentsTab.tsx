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
  implementation_details: "Implementation Details",
  experiments: "Experiments",
  results: "Results",
  conclusion: "Conclusion",
  title: "Title",
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
  matchedSentence,
  score,
  children,
}: {
  label: string;
  confidence: ConfidenceLevel;
  source: string | null;
  found: boolean;
  matchedSentence?: string | null;
  score?: number | null;
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
        <div className="text-[11px] text-gray-400 space-y-0.5">
          <p>
            Source: <span className="font-medium text-gray-500">{sourceLabel(source)}</span>
            {typeof score === "number" && (
              <>
                {" "}
                &middot; Score: <span className="font-medium text-gray-500">{score}</span>
              </>
            )}
          </p>
          {matchedSentence && (
            <p className="italic text-gray-400">Evidence: "{matchedSentence}"</p>
          )}
        </div>
      )}
    </div>
  );
}

function ScalarField({
  label,
  field,
  secondary,
}: {
  label: string;
  field: ComponentField;
  secondary?: string | null;
}) {
  return (
    <FieldShell
      label={label}
      confidence={field.confidence}
      source={field.source}
      found={field.found}
      matchedSentence={field.matchedSentence}
      score={field.score}
    >
      {field.found ? (
        <div>
          <p className="text-sm text-gray-800">{field.value}</p>
          {secondary && <p className="text-xs text-gray-400 mt-0.5">{secondary}</p>}
        </div>
      ) : (
        <div>
          <p className="text-sm text-gray-400 italic">Not found in paper</p>
          <p className="text-xs text-gray-400 mt-0.5">Default: {field.value}</p>
        </div>
      )}
    </FieldShell>
  );
}

function ReferencedModelsCard({ models }: { models: string[] }) {
  if (models.length === 0) return null;
  return (
    <div className="rounded-lg border border-gray-200 p-4 space-y-2">
      <span className="text-xs font-semibold uppercase tracking-wide text-gray-400">Referenced Models</span>
      <p className="text-[11px] text-gray-400">Cited as baselines in Related Work — not the proposed model.</p>
      <div className="flex flex-wrap gap-1.5">
        {models.map((m) => (
          <span key={m} className="px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-500">
            {m}
          </span>
        ))}
      </div>
    </div>
  );
}

function MetricsCard({ field }: { field: MetricsField }) {
  return (
    <FieldShell
      label="Metrics"
      confidence={field.confidence}
      source={field.source}
      found={field.found}
      matchedSentence={field.matchedSentence}
      score={field.score}
    >
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
    <FieldShell
      label="Hyperparameters"
      confidence={field.confidence}
      source={field.source}
      found={field.found}
      matchedSentence={field.matchedSentence}
      score={field.score}
    >
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
        <ScalarField label="Model" field={components.model} secondary={components.expandedModelName} />
        <ScalarField label="Task" field={components.task} />
        <ScalarField label="Dataset" field={components.dataset} />
        <ScalarField label="Backbone" field={components.backbone} />
        <ScalarField label="Loss" field={components.loss} />
        <ScalarField label="Optimizer" field={components.optimizer} />
      </div>
      <ReferencedModelsCard models={components.referencedModels} />
      <MetricsCard field={components.metrics} />
      <HyperparametersCard field={components.hyperparameters} />
    </div>
  );
}
