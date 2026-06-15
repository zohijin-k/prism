interface Props {
  plan: string[];
}

export default function PlanTab({ plan }: Props) {
  return (
    <ol className="space-y-3">
      {plan.map((step, i) => (
        <li key={i} className="flex items-start gap-3">
          <span className="flex-shrink-0 w-6 h-6 rounded bg-prism-600 text-white text-xs font-bold flex items-center justify-center mt-0.5">
            {i + 1}
          </span>
          <span className="text-sm text-gray-800 pt-0.5">{step}</span>
        </li>
      ))}
    </ol>
  );
}
