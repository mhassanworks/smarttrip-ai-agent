import React, { useState, useEffect } from "react";
import { runNegotiation } from "../../services/smarttripApi";

export const NegotiationSection: React.FC = () => {
  const [budget, setBudget] = useState(45000);
  const [data, setData] = useState<any>(null);
  const [running, setRunning] = useState(false);

  const executeNegotiation = async () => {
    setRunning(true);
    try {
      const res = await runNegotiation({ budget, max_rounds: 3, force_overage: true });
      setData(res);
    } catch (err) {
      console.error("Negotiation error", err);
    } finally {
      setRunning(false);
    }
  };

  useEffect(() => {
    executeNegotiation();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="text-xs font-semibold uppercase tracking-wider text-indigo-400 mb-1">
            Assignment 5 &middot; Multi-Agent Negotiation & Consensus
          </div>
          <h2 className="text-2xl font-bold text-white">
            Multi-Turn Proposal & Bidding Protocol
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            Flight, Hotel, and Activity agents submit iterative bids. The Budget Arbiter evaluates package variance and orchestrates concessions to achieve consensus.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="bg-slate-800 border border-slate-700 rounded-lg px-2.5 py-1.5 flex items-center gap-1.5 text-xs">
            <span className="text-slate-400">Budget:</span>
            <input
              type="number"
              value={budget}
              onChange={(e) => setBudget(Number(e.target.value))}
              className="w-20 bg-slate-900 border border-slate-700 text-white font-mono px-1.5 py-0.5 rounded text-xs"
            />
          </div>
          <button
            onClick={executeNegotiation}
            disabled={running}
            className="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-indigo-500 to-indigo-600 hover:from-indigo-600 hover:to-indigo-700 text-white text-xs font-semibold rounded-xl shadow-lg shadow-indigo-500/20 transition-all cursor-pointer disabled:opacity-50"
          >
            <span className={running ? "animate-spin" : ""}>&#9878;</span>
            {running ? "Simulating Bidding..." : "Run Negotiation Simulation"}
          </button>
        </div>
      </div>

      {/* Outcome Banner */}
      {data && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5">
            <div className="text-xs font-medium text-slate-400">NEGOTIATION STATUS</div>
            <div className="text-lg font-bold text-emerald-400 mt-2 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              {data.status.replace("_", " ")}
            </div>
            <div className="text-xs text-slate-500 mt-1">
              Concluded in {data.rounds_executed} of {data.max_rounds} rounds
            </div>
          </div>

          <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5">
            <div className="text-xs font-medium text-slate-400">FINAL AGREED COST</div>
            <div className="text-2xl font-bold text-white font-mono mt-2">
              ₹{data.final_package_cost?.toLocaleString()}
            </div>
            <div className="text-xs text-emerald-400 mt-1">
              Surplus: ₹{Math.abs(data.budget_delta)?.toLocaleString()} under budget
            </div>
          </div>

          <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5">
            <div className="text-xs font-medium text-slate-400">TOTAL CONCESSIONS ACHIEVED</div>
            <div className="text-2xl font-bold text-cyan-400 font-mono mt-2">
              ₹{data.total_concessions_achieved?.toLocaleString()}
            </div>
            <div className="text-xs text-slate-500 mt-1">
              Savings negotiated by Budget Arbiter
            </div>
          </div>

          <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5">
            <div className="text-xs font-medium text-slate-400">FINAL PACKAGE SPLIT</div>
            <div className="text-xs text-slate-300 font-mono mt-2 space-y-0.5">
              <div>Flight: ₹{data.final_selection?.flight?.proposed_cost?.toLocaleString()}</div>
              <div>Hotel: ₹{data.final_selection?.hotel?.proposed_cost?.toLocaleString()}</div>
              <div>Activity: ₹{data.final_selection?.activity?.proposed_cost?.toLocaleString()}</div>
            </div>
          </div>
        </div>
      )}

      {/* Rounds Progression Timeline */}
      {data?.rounds_history && (
        <div className="space-y-4">
          <h3 className="text-base font-semibold text-white">Multi-Turn Negotiation Rounds</h3>

          <div className="space-y-4">
            {data.rounds_history.map((round: any, idx: number) => (
              <div
                key={idx}
                className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 space-y-4"
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
                  <div className="flex items-center gap-3">
                    <span className="w-7 h-7 rounded-lg bg-indigo-600 flex items-center justify-center font-bold text-xs text-white">
                      R{round.round_number}
                    </span>
                    <div>
                      <h4 className="text-sm font-semibold text-white">
                        Round {round.round_number} Proposals & Bids
                      </h4>
                      <p className="text-xs text-slate-400">
                        Combined Proposal: ₹{round.total_proposed?.toLocaleString()} &middot; Variance: {round.variance > 0 ? `+₹${round.variance}` : `-₹${Math.abs(round.variance)}`}
                      </p>
                    </div>
                  </div>

                  <span
                    className={`px-3 py-1 rounded-full text-xs font-semibold ${
                      round.consensus_reached
                        ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30"
                        : "bg-amber-500/20 text-amber-300 border border-amber-500/30"
                    }`}
                  >
                    {round.consensus_reached ? "Consensus Approved" : "Over-budget: Concession Demanded"}
                  </span>
                </div>

                {/* Arbiter Action Message */}
                <div className="bg-slate-800/60 border border-slate-700/60 rounded-xl p-3 text-xs text-indigo-300 flex items-center gap-2">
                  <span className="font-bold text-slate-400">Arbiter Action:</span>
                  <span>{round.arbiter_action}</span>
                </div>

                {/* Domain Agent Bids Grid */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                  {round.bids?.map((bid: any, bIdx: number) => (
                    <div
                      key={bIdx}
                      className="bg-slate-800/30 border border-slate-700/50 rounded-xl p-4 space-y-2"
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-bold text-slate-200">{bid.agent_id}</span>
                        <span className="text-[10px] px-2 py-0.5 rounded font-mono uppercase bg-slate-700 text-slate-300">
                          {bid.tier}
                        </span>
                      </div>
                      <div className="text-xs text-indigo-200 font-medium">
                        {bid.specification}
                      </div>
                      <div className="flex items-center justify-between text-xs pt-1">
                        <span className="font-mono font-bold text-white">
                          ₹{bid.proposed_cost?.toLocaleString()}
                        </span>
                        {bid.concession_made > 0 && (
                          <span className="text-emerald-400 text-[11px] font-mono">
                            -₹{bid.concession_made} concession
                          </span>
                        )}
                      </div>
                      <div className="text-[11px] text-slate-400 italic pt-1 border-t border-slate-800">
                        &ldquo;{bid.rationale}&rdquo;
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
