import { ComparisonItem, ComparisonStatus } from "../../types";

interface Props {
  items: ComparisonItem[];
}

const statusStyles: Record<ComparisonStatus, string> = {
  Match: "bg-green-100 text-green-700",
  "Code Only": "bg-blue-100 text-blue-700",
  "Paper Only": "bg-yellow-100 text-yellow-700",
  Mismatch: "bg-red-100 text-red-700",
};

export default function ComparisonTab({ items }: Props) {
  return (
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
            <tr key={i} className="hover:bg-gray-50 transition-colors">
              <td className="px-4 py-3 font-medium text-gray-800">{item.item}</td>
              <td className="px-4 py-3 text-gray-600">{item.paper}</td>
              <td className="px-4 py-3 text-gray-600">{item.code}</td>
              <td className="px-4 py-3">
                <span className={`inline-block px-2 py-0.5 rounded-full text-xs font-semibold ${statusStyles[item.status]}`}>
                  {item.status}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
