import { useState } from "react";
import { AnalysisResult } from "../types";
import SummaryTab from "./tabs/SummaryTab";
import PlanTab from "./tabs/PlanTab";
import ComponentsTab from "./tabs/ComponentsTab";
import ComparisonTab from "./tabs/ComparisonTab";
import TraceViewTab from "./tabs/TraceViewTab";
import MissingInfoTab from "./tabs/MissingInfoTab";

const TABS = [
  { id: "summary",    label: "Summary",     icon: "M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" },
  { id: "plan",       label: "Plan",        icon: "M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" },
  { id: "components", label: "Components",  icon: "M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z" },
  { id: "comparison", label: "Comparison",  icon: "M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" },
  { id: "trace",      label: "Trace View",  icon: "M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" },
  { id: "missing",    label: "Missing Info",icon: "M12 9v2m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" },
] as const;

type TabId = (typeof TABS)[number]["id"];

function getBadge(result: AnalysisResult, id: TabId): number | null {
  if (id === "comparison") return result.comparison.filter((c) => c.status !== "Match").length || null;
  if (id === "trace") return result.mapping.length || null;
  if (id === "missing") return result.missingInfo.length || null;
  return null;
}

interface Props {
  result: AnalysisResult;
}

export default function ResultTabs({ result }: Props) {
  const [active, setActive] = useState<TabId>("summary");

  return (
    <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
      {/* Tab bar */}
      <div className="flex border-b border-gray-200 overflow-x-auto scrollbar-hide">
        {TABS.map((tab) => {
          const badge = getBadge(result, tab.id);
          const isActive = active === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActive(tab.id)}
              className={`relative flex items-center gap-1.5 px-4 py-3 text-sm font-medium whitespace-nowrap transition-colors shrink-0 ${
                isActive
                  ? "text-prism-600"
                  : "text-gray-500 hover:text-gray-800 hover:bg-gray-50"
              }`}
            >
              <svg className="w-3.5 h-3.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={tab.icon} />
              </svg>
              {tab.label}
              {badge !== null && (
                <span className={`px-1.5 py-0.5 rounded-full text-[10px] font-bold leading-none ${
                  isActive ? "bg-prism-100 text-prism-700" : "bg-gray-100 text-gray-500"
                }`}>
                  {badge}
                </span>
              )}
              {isActive && (
                <span className="absolute bottom-0 left-0 right-0 h-0.5 bg-prism-600 rounded-t" />
              )}
            </button>
          );
        })}
      </div>

      {/* Content */}
      <div className="p-6">
        {active === "summary"    && <SummaryTab    summary={result.summary} paperInfo={result.paperInfo} />}
        {active === "plan"       && <PlanTab        plan={result.implementationPlan} />}
        {active === "components" && <ComponentsTab  components={result.components} />}
        {active === "comparison" && <ComparisonTab  items={result.comparison} repoAnalysis={result.repoAnalysis} />}
        {active === "trace"      && <TraceViewTab   mapping={result.mapping} paperInfo={result.paperInfo} repoAnalysis={result.repoAnalysis} />}
        {active === "missing"    && <MissingInfoTab items={result.missingInfo} />}
      </div>
    </div>
  );
}
