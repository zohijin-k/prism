interface Props {
  items: string[];
}

export default function MissingInfoTab({ items }: Props) {
  if (items.length === 0) {
    return (
      <p className="text-sm text-gray-400 text-center py-8">
        No reproducibility gaps detected.
      </p>
    );
  }

  return (
    <ul className="space-y-2.5">
      {items.map((item, i) => (
        <li key={i} className="flex items-start gap-3 rounded-lg border border-yellow-100 bg-yellow-50 px-4 py-3">
          <svg className="w-4 h-4 text-yellow-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
              d="M12 9v2m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
          </svg>
          <span className="text-sm text-yellow-800 leading-relaxed">{item}</span>
        </li>
      ))}
    </ul>
  );
}
