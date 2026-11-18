import React, { useEffect, useState } from "react";
import { fetchPeasDocs } from "../../services/smarttripApi";

export const PeasSection: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<"peas" | "environment" | "oop">("peas");
  const [selectedAgentIdx, setSelectedAgentIdx] = useState(0);

  useEffect(() => {
    async function load() {
      try {
        const d = await fetchPeasDocs();
        setData(d);
      } catch (err) {
        console.error("Failed to fetch PEAS docs", err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading || !data) {
    return (
      <div className="p-8 text-center text-slate-400">
        <div className="animate-spin w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full mx-auto mb-3" />
        Loading PEAS & Environment Specifications...
      </div>
    );
  }

  const selectedAgent = data.peas_matrix[selectedAgentIdx];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-slate-900/90 border border-slate-800 p-6 rounded-2xl">
        <div>
          <div className="text-xs font-semibold uppercase tracking-wider text-indigo-400 mb-1">
            Assignment 1 &middot; Theoretical Framework
          </div>
          <h2 className="text-2xl font-bold text-white">
            PEAS & Multi-Agent Environment Classification
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            Formal agent definitions, Russell & Norvig environment taxonomy, and Agent vs Object-Oriented paradigm comparison.
          </p>
        </div>

        {/* Sub-tabs */}
        <div className="flex bg-slate-800/80 p-1 rounded-xl border border-slate-700">
          <button
            onClick={() => setActiveTab("peas")}
            className={`px-3 py-1.5 text-xs font-medium rounded-lg transition-all cursor-pointer ${
              activeTab === "peas" ? "bg-indigo-600 text-white shadow" : "text-slate-400 hover:text-white"
            }`}
          >
            PEAS Matrix ({data.peas_matrix.length})
          </button>
          <button
            onClick={() => setActiveTab("environment")}
            className={`px-3 py-1.5 text-xs font-medium rounded-lg transition-all cursor-pointer ${
              activeTab === "environment" ? "bg-indigo-600 text-white shadow" : "text-slate-400 hover:text-white"
            }`}
          >
            Environment Taxonomy
          </button>
          <button
            onClick={() => setActiveTab("oop")}
            className={`px-3 py-1.5 text-xs font-medium rounded-lg transition-all cursor-pointer ${
              activeTab === "oop" ? "bg-indigo-600 text-white shadow" : "text-slate-400 hover:text-white"
            }`}
          >
            Agent vs OOP
          </button>
        </div>
      </div>

      {/* Tab 1: PEAS Matrix */}
      {activeTab === "peas" && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Agent Selector List */}
          <div className="lg:col-span-4 space-y-2">
            <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider px-2">
              Select Agent Persona
            </h3>
            {data.peas_matrix.map((agent: any, idx: number) => (
              <button
                key={idx}
                onClick={() => setSelectedAgentIdx(idx)}
                className={`w-full text-left p-3.5 rounded-xl border transition-all cursor-pointer ${
                  selectedAgentIdx === idx
                    ? "bg-indigo-950/70 border-indigo-500/60 shadow-lg text-white"
                    : "bg-slate-900/60 border-slate-800 text-slate-300 hover:bg-slate-800/80"
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-sm">{agent.agent}</span>
                  {selectedAgentIdx === idx && (
                    <span className="w-2 h-2 rounded-full bg-indigo-400" />
                  )}
                </div>
                <div className="text-xs text-slate-400 mt-1 truncate">{agent.role}</div>
              </button>
            ))}
          </div>

          {/* Detailed PEAS Card for Selected Agent */}
          <div className="lg:col-span-8 bg-slate-900/90 border border-slate-800 rounded-2xl p-6 space-y-6">
            <div className="border-b border-slate-800 pb-4">
              <span className="text-xs font-semibold text-indigo-400 uppercase tracking-wider">
                Agent Specification
              </span>
              <h3 className="text-2xl font-bold text-white mt-1">{selectedAgent.agent}</h3>
              <p className="text-sm text-slate-300 mt-1">{selectedAgent.role}</p>

              <div className="flex flex-wrap gap-2 mt-3">
                {selectedAgent.characteristics?.map((char: string, i: number) => (
                  <span
                    key={i}
                    className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-500/10 text-indigo-300 border border-indigo-500/20"
                  >
                    {char}
                  </span>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Performance Measure */}
              <div className="bg-slate-800/50 border border-slate-700/60 rounded-xl p-4">
                <div className="flex items-center gap-2 text-xs font-bold text-emerald-400 mb-2">
                  <span className="w-5 h-5 rounded-md bg-emerald-500/20 flex items-center justify-center">P</span>
                  <span>PERFORMANCE MEASURE</span>
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">
                  {selectedAgent.performance_measure}
                </p>
              </div>

              {/* Environment */}
              <div className="bg-slate-800/50 border border-slate-700/60 rounded-xl p-4">
                <div className="flex items-center gap-2 text-xs font-bold text-cyan-400 mb-2">
                  <span className="w-5 h-5 rounded-md bg-cyan-500/20 flex items-center justify-center">E</span>
                  <span>ENVIRONMENT</span>
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">
                  {selectedAgent.environment}
                </p>
              </div>

              {/* Actuators */}
              <div className="bg-slate-800/50 border border-slate-700/60 rounded-xl p-4">
                <div className="flex items-center gap-2 text-xs font-bold text-amber-400 mb-2">
                  <span className="w-5 h-5 rounded-md bg-amber-500/20 flex items-center justify-center">A</span>
                  <span>ACTUATORS</span>
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">
                  {selectedAgent.actuators}
                </p>
              </div>

              {/* Sensors */}
              <div className="bg-slate-800/50 border border-slate-700/60 rounded-xl p-4">
                <div className="flex items-center gap-2 text-xs font-bold text-purple-400 mb-2">
                  <span className="w-5 h-5 rounded-md bg-purple-500/20 flex items-center justify-center">S</span>
                  <span>SENSORS</span>
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">
                  {selectedAgent.sensors}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab 2: Environment Classifications */}
      {activeTab === "environment" && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {data.environment_classifications.map((item: any, idx: number) => (
            <div
              key={idx}
              className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 hover:border-indigo-500/40 transition-all"
            >
              <div className="text-xs font-semibold text-indigo-400 uppercase tracking-wider mb-1">
                {item.dimension}
              </div>
              <div className="text-lg font-bold text-white mb-2">{item.classification}</div>
              <p className="text-xs text-slate-300 leading-relaxed">{item.justification}</p>
            </div>
          ))}
        </div>
      )}

      {/* Tab 3: Autonomous Agent vs OOP Comparison */}
      {activeTab === "oop" && (
        <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-800 text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  <th className="py-3 px-4 w-1/4">Evaluation Dimension</th>
                  <th className="py-3 px-4 w-3/8 text-indigo-400">Autonomous Agent (MAS)</th>
                  <th className="py-3 px-4 w-3/8 text-slate-300">Object-Oriented Programming (OOP)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-xs text-slate-300">
                {data.agent_vs_oop.map((row: any, i: number) => (
                  <tr key={i} className="hover:bg-slate-800/30 transition-colors">
                    <td className="py-4 px-4 font-semibold text-white">{row.dimension}</td>
                    <td className="py-4 px-4 bg-indigo-950/20 text-indigo-200 leading-relaxed">
                      {row.autonomous_agent}
                    </td>
                    <td className="py-4 px-4 text-slate-400 leading-relaxed">
                      {row.oop_object}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
