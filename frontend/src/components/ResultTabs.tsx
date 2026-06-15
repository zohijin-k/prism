import { useState } from "react";
import { AnalysisResult } from "../types";
import SummaryTab from "./tabs/SummaryTab";
import PlanTab from "./tabs/PlanTab";
import ComponentsTab from "./tabs/ComponentsTab";
import ComparisonTab from "./tabs/ComparisonTab";
import MappingTab from "./tabs/MappingTab";
import MissingInfoTab from "./tabs/MissingInfoTab";

const TABS = [
  { id: "summary", label: "Summary" },
  { id: "plan", label: "Plan" },
  { id: "components", label: "Components" },
  { id: "comparison", label: "Comparison" },
  { id: "mapping", label: "Mapping" },
  { id: "missing", label: "Missing Info" },
] as const;

type TabId = (typeof TABS)[number]["id"];

interface Props {
  result: AnalysisResult;
}

export default function ResultTabs({ result }: Props) {
  const [active, setActive] = useState<TabId>("summary");

  return (
    <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
      {/* Tab bar */}
      <div className="flex border-b border-gray-200 overflow-x-auto">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActive(tab.id)}
            className={`px-4 py-3 text-sm font-medium whitespace-nowrap transition-colors ${
              active === tab.id
                ? "text-prism-600 border-b-2 border-prism-600 bg-prism-50"
                : "text-gray-500 hover:text-gray-800"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab content */}
      <div className="p-6">
        {active === "summary" && <SummaryTab summary={result.summary} />}
        {active === "plan" && <PlanTab plan={result.implementationPlan} />}
        {active === "components" && <ComponentsTab components={result.components} />}
        {active === "comparison" && <ComparisonTab items={result.comparison} />}
        {active === "mapping" && <MappingTab items={result.mapping} />}
        {active === "missing" && <MissingInfoTab items={result.missingInfo} />}
      </div>
    </div>
  );
}
