import React, { useState, useEffect } from "react";
import { optimizeUtility } from "../../services/smarttripApi";

export const UtilityOptimizerSection: React.FC = () => {
  const [budget, setBudget] = useState(45000);
  const [destination, setDestination] = useState("Goa");
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const runOptimization = async () => {
    setLoading(true);
    try {
      const res = await optimizeUtility({ budget, destination });
      setData(res);
      if (res?.winning_configuration) {
        setExpandedId(res.winning_configuration.config_id);
      }
    } catch (err) {
      console.error("Utility optimization error", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runOptimization();
  }, []);

  const winner = data?.winning_configuration;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="text-xs font-semibold uppercase tracking-wider text-indigo-400 mb-1">
            Assignment 6 &middot; Decision Theory & Optimization
          </div>
          <h2 className="text-2xl font-bold text-white">
            Multi-Attribute Utility Theory (10 Configurations)
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            Mathematical evaluation function ranking 10 distinct travel configurations across budget efficiency, quality rating, transit convenience, and weather suitability.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <div className="bg-slate-800 border border-slate-700 rounded-lg px-2.5 py-1.5 flex items-center gap-2 text-xs">
            <span className="text-slate-400">Budget:</span>
            <input
              type="number"
              value={budget}
              onChange={(e) => setBudget(Number(e.target.value))}
              className="w-20 bg-slate-900 border border-slate-700 text-white font-mono px-1.5 py-0.5 rounded text-xs"
            />
          </div>
          <div className="bg-slate-800 border border-slate-700 rounded-lg px-2.5 py-1.5 flex items-center gap-2 text-xs">
            <span className="text-slate-400">City:</span>
            <select
              value={destination}
              onChange={(e) => setDestination(e.target.value)}
              className="bg-slate-900 border border-slate-700 text-white px-1.5 py-0.5 rounded text-xs"
            >
              <option value="Goa">Goa</option>
              <option value="Delhi">Delhi</option>
              <option value="Mumbai">Mumbai</option>
              <option value="Jaipur">Jaipur</option>
            </select>
          </div>
          <button
            onClick={runOptimization}
            disabled={loading}
            className="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-indigo-500 to-indigo-600 hover:from-indigo-600 hover:to-indigo-700 text-white text-xs font-semibold rounded-xl shadow-lg shadow-indigo-500/20 transition-all cursor-pointer disabled:opacity-50 shrink-0"
          >
            <span className={loading ? "animate-spin" : ""}>&#9881;</span>
            {loading ? "Optimizing..." : "Recompute 10 Configurations"}
          </button>
        </div>
      </div>

      {/* Mathematical Model Card */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <span className="text-xs font-bold text-indigo-400 font-mono">MATHEMATICAL FORMULATION</span>
            <div className="text-sm font-bold text-white font-mono mt-1">
              U(c) = 0.35 &middot; U_budget(c) + 0.25 &middot; U_rating(c) + 0.20 &middot; U_convenience(c) + 0.20 &middot; U_weather(c)
            </div>
          </div>
          <div className="flex flex-wrap gap-2 text-xs font-mono">
            <span className="px-2.5 py-1 rounded bg-slate-800 text-slate-300">w_budget: 0.35</span>
            <span className="px-2.5 py-1 rounded bg-slate-800 text-slate-300">w_rating: 0.25</span>
            <span className="px-2.5 py-1 rounded bg-slate-800 text-slate-300">w_convenience: 0.20</span>
            <span className="px-2.5 py-1 rounded bg-slate-800 text-slate-300">w_weather: 0.20</span>
          </div>
        </div>
      </div>

      {/* Winning Configuration Card */}
      {winner && (
        <div className="relative overflow-hidden bg-gradient-to-r from-indigo-950 via-slate-900 to-slate-900 border-2 border-indigo-500/50 rounded-2xl p-6 shadow-xl">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <div className="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30 mb-2">
                &#9733; OPTIMAL CONFIGURATION &middot; RANK #1 WINNER
              </div>
              <h3 className="text-2xl font-bold text-white">{winner.name}</h3>
              <p className="text-xs text-indigo-300 font-medium mt-0.5">
                Archetype: {winner.archetype} &middot; Total Cost: ₹{winner.total_cost?.toLocaleString()} (Under budget by ₹{Math.abs(winner.cost_variance)?.toLocaleString()})
              </p>
            </div>

            <div className="text-right">
              <div className="text-xs text-slate-400 font-medium">AGGREGATE UTILITY SCORE</div>
              <div className="text-4xl font-extrabold text-indigo-400 font-mono mt-0.5">
                {winner.aggregate_utility} <span className="text-lg text-slate-400 font-normal">/ 100</span>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-5 pt-4 border-t border-indigo-900/60">
            <div className="bg-slate-900/60 rounded-xl p-3 border border-slate-800">
              <div className="text-[11px] text-slate-400">Budget Efficiency</div>
              <div className="text-base font-bold text-emerald-400 font-mono mt-0.5">
                {winner.sub_utilities?.budget_efficiency} / 100
              </div>
            </div>
            <div className="bg-slate-900/60 rounded-xl p-3 border border-slate-800">
              <div className="text-[11px] text-slate-400">Quality Rating</div>
              <div className="text-base font-bold text-cyan-400 font-mono mt-0.5">
                {winner.sub_utilities?.quality_rating} / 100
              </div>
            </div>
            <div className="bg-slate-900/60 rounded-xl p-3 border border-slate-800">
              <div className="text-[11px] text-slate-400">Transit Convenience</div>
              <div className="text-base font-bold text-indigo-300 font-mono mt-0.5">
                {winner.sub_utilities?.transit_convenience} / 100
              </div>
            </div>
            <div className="bg-slate-900/60 rounded-xl p-3 border border-slate-800">
              <div className="text-[11px] text-slate-400">Weather Match</div>
              <div className="text-base font-bold text-amber-300 font-mono mt-0.5">
                {winner.sub_utilities?.weather_suitability} / 100
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Ranked Table of 10 Configurations */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6">
        <h3 className="text-base font-semibold text-white mb-4">
          All 10 Ranked Travel Configurations
        </h3>

        <div className="space-y-3">
          {data?.ranked_configurations?.map((conf: any) => {
            const isExpanded = expandedId === conf.config_id;
            return (
              <div
                key={conf.config_id}
                className={`border rounded-xl transition-all ${
                  conf.rank === 1
                    ? "bg-indigo-950/30 border-indigo-500/40"
                    : "bg-slate-800/30 border-slate-800 hover:border-slate-700"
                }`}
              >
                <div
                  onClick={() => setExpandedId(isExpanded ? null : conf.config_id)}
                  className="p-4 flex flex-col md:flex-row md:items-center justify-between gap-3 cursor-pointer"
                >
                  <div className="flex items-center gap-3">
                    <span
                      className={`w-7 h-7 rounded-lg flex items-center justify-center font-bold text-xs ${
                        conf.rank === 1
                          ? "bg-amber-500 text-slate-950"
                          : conf.rank <= 3
                          ? "bg-indigo-600 text-white"
                          : "bg-slate-700 text-slate-300"
                      }`}
                    >
                      #{conf.rank}
                    </span>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-sm text-white">{conf.name}</span>
                        <span className="text-[10px] px-2 py-0.5 rounded font-mono bg-slate-700/60 text-slate-300">
                          {conf.archetype}
                        </span>
                      </div>
                      <div className="text-xs text-slate-400 font-mono mt-0.5">
                        Cost: ₹{conf.total_cost?.toLocaleString()} &middot; Variance: {conf.cost_variance > 0 ? `+₹${conf.cost_variance}` : `-₹${Math.abs(conf.cost_variance)}`}
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-4">
                    <div className="text-right">
                      <div className="text-xs font-mono font-bold text-indigo-400 text-base">
                        {conf.aggregate_utility} pts
                      </div>
                      <div className="text-[10px] text-slate-500">MAUT Score</div>
                    </div>
                    <span className="text-slate-400 text-xs">
                      {isExpanded ? "\u25B2" : "\u25BC"}
                    </span>
                  </div>
                </div>

                {isExpanded && (
                  <div className="px-4 pb-4 pt-2 border-t border-slate-800/80 bg-slate-900/50 text-xs text-slate-300 space-y-3 font-mono">
                    <div className="text-[11px] text-indigo-300">
                      {conf.formula_breakdown}
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-3 pt-2">
                      <div className="bg-slate-800/40 p-2.5 rounded-lg border border-slate-700/40">
                        <div className="text-slate-400 text-[10px] uppercase">Flight Details</div>
                        <div className="text-white font-sans font-semibold mt-0.5">{conf.details.flight.name}</div>
                        <div className="text-slate-400 mt-0.5">₹{conf.details.flight.price?.toLocaleString()} &middot; {conf.details.flight.stops} stops &middot; {conf.details.flight.duration_hours}h</div>
                      </div>

                      <div className="bg-slate-800/40 p-2.5 rounded-lg border border-slate-700/40">
                        <div className="text-slate-400 text-[10px] uppercase">Hotel Details</div>
                        <div className="text-white font-sans font-semibold mt-0.5">{conf.details.hotel.name}</div>
                        <div className="text-slate-400 mt-0.5">₹{conf.details.hotel.price?.toLocaleString()} &middot; {conf.details.hotel.stars}&#9733; ({conf.details.hotel.rating}/5.0)</div>
                      </div>

                      <div className="bg-slate-800/40 p-2.5 rounded-lg border border-slate-700/40">
                        <div className="text-slate-400 text-[10px] uppercase">Activity Package</div>
                        <div className="text-white font-sans font-semibold mt-0.5">{conf.details.activity.package}</div>
                        <div className="text-slate-400 mt-0.5">₹{conf.details.activity.price?.toLocaleString()}</div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
