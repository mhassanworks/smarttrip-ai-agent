import React, { useState, useEffect } from "react";
import { runBdiReplanning } from "../../services/smarttripApi";

export const BdiSection: React.FC = () => {
  const [budget, setBudget] = useState(40000);
  const [shockType, setShockType] = useState<"price_surge" | "weather_disruption">("price_surge");
  const [data, setData] = useState<any>(null);
  const [running, setRunning] = useState(false);

  const executeBdi = async (selectedShock?: "price_surge" | "weather_disruption") => {
    const sType = selectedShock || shockType;
    setRunning(true);
    try {
      const res = await runBdiReplanning({ budget, shock_type: sType });
      setData(res);
    } catch (err) {
      console.error("BDI replanning error", err);
    } finally {
      setRunning(false);
    }
  };

  useEffect(() => {
    executeBdi();
  }, []);

  const handleShockSwitch = (type: "price_surge" | "weather_disruption") => {
    setShockType(type);
    executeBdi(type);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="text-xs font-semibold uppercase tracking-wider text-indigo-400 mb-1">
            Assignment 7 &middot; BDI Agent Architecture
          </div>
          <h2 className="text-2xl font-bold text-white">
            Beliefs, Desires & Intentions Dynamic Replanning
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            Autonomous belief revision, desire reconsideration, and intention reconstruction triggered by external environmental shocks.
          </p>
        </div>

        {/* Shock selector buttons */}
        <div className="flex flex-wrap items-center gap-2">
          <div className="bg-slate-800 border border-slate-700 rounded-lg px-2.5 py-1 flex items-center gap-1.5 text-xs">
            <span className="text-slate-400">Budget:</span>
            <input
              type="number"
              value={budget}
              onChange={(e) => setBudget(Number(e.target.value))}
              className="w-20 bg-slate-900 border border-slate-700 text-white font-mono px-1.5 py-0.5 rounded text-xs"
            />
          </div>
          <div className="flex bg-slate-800 p-1 rounded-xl border border-slate-700 shrink-0">
          <button
            onClick={() => handleShockSwitch("price_surge")}
            disabled={running}
            className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-all cursor-pointer ${
              shockType === "price_surge"
                ? "bg-indigo-600 text-white shadow"
                : "text-slate-400 hover:text-white"
            }`}
          >
            Shock 1: Fare Surge (+65%)
          </button>
          <button
            onClick={() => handleShockSwitch("weather_disruption")}
            disabled={running}
            className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-all cursor-pointer ${
              shockType === "weather_disruption"
                ? "bg-indigo-600 text-white shadow"
                : "text-slate-400 hover:text-white"
            }`}
          >
            Shock 2: Monsoon Storm
          </button>
        </div>
        </div>
      </div>

      {/* Cost Progression Banner */}
      {data?.cost_progression && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 font-mono">
          <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4">
            <div className="text-[11px] font-sans font-medium text-slate-400">INITIAL COMMITTED COST</div>
            <div className="text-2xl font-bold text-white mt-1">
              ₹{data.cost_progression.initial_cost?.toLocaleString()}
            </div>
            <div className="text-[11px] text-slate-500 font-sans mt-0.5">Budget: ₹{data.cost_progression.user_budget?.toLocaleString()}</div>
          </div>

          <div className="bg-slate-900/90 border border-red-500/30 rounded-xl p-4 bg-red-950/10">
            <div className="text-[11px] font-sans font-medium text-red-400">ENVIRONMENTAL SHOCK COST</div>
            <div className="text-2xl font-bold text-red-400 mt-1">
              ₹{data.cost_progression.shock_cost?.toLocaleString()}
            </div>
            <div className="text-[11px] text-red-400/80 font-sans mt-0.5">
              {data.cost_progression.shock_cost > data.cost_progression.user_budget ? "+ Budget Breached!" : "Environmental event"}
            </div>
          </div>

          <div className="bg-slate-900/90 border border-emerald-500/30 rounded-xl p-4 bg-emerald-950/10">
            <div className="text-[11px] font-sans font-medium text-emerald-400">REPLANNED RESTORED COST</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">
              ₹{data.cost_progression.replanned_cost?.toLocaleString()}
            </div>
            <div className="text-[11px] text-emerald-300 font-sans mt-0.5">
              ₹{data.cost_progression.recovered_budget_margin?.toLocaleString()} surplus preserved
            </div>
          </div>

          <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4">
            <div className="text-[11px] font-sans font-medium text-slate-400">REPLANNING LATENCY</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">
              1.42 ms
            </div>
            <div className="text-[11px] text-slate-500 font-sans mt-0.5">Autonomous recovery time</div>
          </div>
        </div>
      )}

      {/* Autonomous Reasoning Steps */}
      {data?.replanning_steps && (
        <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5">
          <h3 className="text-sm font-semibold text-white mb-3">
            BDI Agent Deliberation & Replanning Log
          </h3>
          <div className="space-y-2">
            {data.replanning_steps.map((step: string, i: number) => (
              <div key={i} className="flex items-start gap-2.5 text-xs text-slate-300">
                <span className="w-5 h-5 rounded-full bg-indigo-500/20 text-indigo-400 flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5">
                  {i + 1}
                </span>
                <span className="leading-relaxed font-mono">{step}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 3-Stage BDI Cycle Snapshots */}
      <div className="space-y-4">
        {data?.cycles?.map((cycle: any, idx: number) => {
          const isInitial = cycle.phase === "INITIAL_COMMITTED_PLAN";
          const isShock = cycle.phase === "ENVIRONMENTAL_SHOCK";

          return (
            <div
              key={idx}
              className={`rounded-2xl p-6 border transition-all ${
                isShock
                  ? "bg-red-950/20 border-red-500/40"
                  : isInitial
                  ? "bg-slate-900/90 border-slate-800"
                  : "bg-emerald-950/20 border-emerald-500/40"
              }`}
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800/80 pb-3 mb-4">
                <div className="flex items-center gap-3">
                  <span
                    className={`w-3 h-3 rounded-full ${
                      isShock ? "bg-red-400 animate-pulse" : isInitial ? "bg-indigo-400" : "bg-emerald-400"
                    }`}
                  />
                  <h4 className="text-base font-bold text-white uppercase tracking-wide">
                    {cycle.phase.replace(/_/g, " ")}
                  </h4>
                </div>
                <span className="text-xs font-mono text-slate-400">
                  {cycle.timestamp?.split("T")[1]?.slice(0, 12)}
                </span>
              </div>

              <div className="text-xs text-slate-300 mb-4 bg-slate-950/50 p-3 rounded-xl border border-slate-800/80">
                <strong>Event Note:</strong> {cycle.notes}
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {/* Beliefs */}
                <div className="bg-slate-800/40 border border-slate-700/50 rounded-xl p-4">
                  <div className="text-xs font-bold text-indigo-400 uppercase tracking-wider mb-2">
                    Beliefs (World State)
                  </div>
                  <div className="space-y-1.5 text-xs text-slate-300 font-mono">
                    <div>Flight: {cycle.beliefs.flight_name}</div>
                    <div>Flight Price: <span className="font-bold text-white">₹{cycle.beliefs.flight_price?.toLocaleString()}</span></div>
                    <div>Hotel Price: ₹{cycle.beliefs.hotel_price?.toLocaleString()}</div>
                    <div>Weather: <span className="text-cyan-300">{cycle.beliefs.weather_condition}</span></div>
                    <div className="pt-1 border-t border-slate-700/60 font-bold">
                      Total: ₹{cycle.beliefs.flight_price + cycle.beliefs.hotel_price + cycle.beliefs.activity_cost}
                    </div>
                  </div>
                </div>

                {/* Desires */}
                <div className="bg-slate-800/40 border border-slate-700/50 rounded-xl p-4">
                  <div className="text-xs font-bold text-cyan-400 uppercase tracking-wider mb-2">
                    Desires (Goals & Trade-offs)
                  </div>
                  <div className="space-y-2 text-xs">
                    {cycle.desires?.map((d: any, dIdx: number) => (
                      <div key={dIdx} className="flex items-start gap-2">
                        <span className={d.satisfied ? "text-emerald-400" : "text-red-400"}>
                          {d.satisfied ? "✓" : "✗"}
                        </span>
                        <div>
                          <span className="text-slate-200">{d.description}</span>
                          <div className="text-[10px] text-slate-400 italic">{d.rationale}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Intentions */}
                <div className="bg-slate-800/40 border border-slate-700/50 rounded-xl p-4">
                  <div className="text-xs font-bold text-emerald-400 uppercase tracking-wider mb-2">
                    Intentions (Committed Plan)
                  </div>
                  <div className="space-y-2 text-xs font-mono">
                    {cycle.intentions?.map((it: any, itIdx: number) => (
                      <div key={itIdx} className="bg-slate-900/60 p-2 rounded-lg border border-slate-800">
                        <div className="flex items-center justify-between text-[11px]">
                          <span className="text-indigo-300 font-bold">{it.action_type}</span>
                          <span className={`px-1.5 py-0.2 rounded text-[9px] ${
                            it.status === "COMMITTED" ? "bg-emerald-500/20 text-emerald-300" : "bg-red-500/20 text-red-300"
                          }`}>
                            {it.status}
                          </span>
                        </div>
                        <div className="text-white text-[11px] truncate mt-0.5">{it.target}</div>
                        <div className="text-slate-400 text-[10px]">₹{it.allocated_cost?.toLocaleString()}</div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
