interface Props {
  plan: string[];
}

export default function PlanTab({ plan }: Props) {
  return (
    <div className="relative">
      {/* vertical line */}
      <div className="absolute left-[18px] top-6 bottom-6 w-px bg-gray-100" />
      <ol className="space-y-4">
        {plan.map((step, i) => (
          <li key={i} className="flex items-start gap-4 relative">
            <span className="flex-shrink-0 w-9 h-9 rounded-full bg-prism-600 text-white text-sm font-bold flex items-center justify-center z-10 shadow-sm">
              {i + 1}
            </span>
            <div className="flex-1 min-h-[36px] flex items-center">
              <p className="text-sm text-gray-800 leading-relaxed">{step}</p>
            </div>
          </li>
        ))}
      </ol>
    </div>
  );
}
