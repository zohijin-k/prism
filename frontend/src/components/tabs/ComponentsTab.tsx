import { Components } from "../../types";

interface Props {
  components: Components;
}

const scalarFields: { key: keyof Omit<Components, "metrics" | "hyperparameters">; label: string }[] = [
  { key: "dataset", label: "Dataset" },
  { key: "model", label: "Model" },
  { key: "backbone", label: "Backbone" },
  { key: "loss", label: "Loss" },
  { key: "optimizer", label: "Optimizer" },
];

export default function ComponentsTab({ components }: Props) {
  return (
    <div className="space-y-6">
      <dl className="grid grid-cols-2 gap-x-6 gap-y-4">
        {scalarFields.map(({ key, label }) => (
          <div key={key}>
            <dt className="text-xs font-semibold uppercase tracking-wide text-gray-400 mb-0.5">{label}</dt>
            <dd className="text-sm text-gray-800">{components[key]}</dd>
          </div>
        ))}

        <div>
          <dt className="text-xs font-semibold uppercase tracking-wide text-gray-400 mb-1">Metrics</dt>
          <dd className="flex flex-wrap gap-1.5">
            {components.metrics.map((m) => (
              <span key={m} className="px-2 py-0.5 rounded-full bg-prism-100 text-prism-700 text-xs font-medium">
                {m}
              </span>
            ))}
          </dd>
        </div>
      </dl>

      <div>
        <h3 className="text-xs font-semibold uppercase tracking-wide text-gray-400 mb-2">Hyperparameters</h3>
        <div className="rounded-lg border border-gray-200 overflow-hidden">
          <table className="w-full text-sm">
            <tbody>
              {Object.entries(components.hyperparameters).map(([k, v], i) => (
                <tr key={k} className={i % 2 === 0 ? "bg-gray-50" : "bg-white"}>
                  <td className="px-4 py-2 font-medium text-gray-600 w-1/2">{k}</td>
                  <td className="px-4 py-2 text-gray-800">{String(v)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
