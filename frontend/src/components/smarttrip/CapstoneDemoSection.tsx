import React, { useState, useEffect } from "react";
import { runCapstoneDemo, fetchDemoHistory } from "../../services/smarttripApi";

export const CapstoneDemoSection: React.FC = () => {
  const [destination, setDestination] = useState("Goa");
  const [budget, setBudget] = useState(45000);
  const [travelerType, setTravelerType] = useState("couple");
  const [demoResult, setDemoResult] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [running, setRunning] = useState(false);

  const loadHistory = async () => {
    try {
      const data = await fetchDemoHistory();
      setHistory(data);
    } catch (err) {
      console.error("History fetch error", err);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const handleRunDemo = async () => {
    setRunning(true);
    try {
      const res = await runCapstoneDemo({
        origin: "DEL",
        destination,
        budget,
        traveler_type: travelerType,
        interests: ["beach", "culture", "relaxation"],
      });
      setDemoResult(res);
      await loadHistory();
    } catch (err) {
      console.error("Demo run error", err);
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 p-8 border border-indigo-500/30 shadow-2xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 relative z-10">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 mb-3">
              ASSIGNMENT 10 &middot; UNIFIED CAPSTONE LIFECYCLE
            </div>
            <h2 className="text-3xl font-extrabold text-white">
              One-Click End-to-End System Demonstration
            </h2>
            <p className="mt-2 text-slate-300 max-w-2xl text-sm leading-relaxed">
              Executes all 10 curricular assignments in a single unified autonomous pipeline: Rule inference &rarr; Weather &rarr; BDI Replanning &rarr; TCP Sockets &rarr; Concurrency &rarr; Multi-Agent Negotiation &rarr; MAUT Utility &rarr; HMAC Audit &rarr; SQLite Persistence.
            </p>
          </div>

          <button
            onClick={handleRunDemo}
            disabled={running}
            className="inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl bg-gradient-to-r from-indigo-500 via-indigo-600 to-cyan-500 hover:from-indigo-600 hover:to-cyan-600 text-white font-bold text-sm shadow-xl shadow-indigo-500/25 transition-all cursor-pointer disabled:opacity-50 shrink-0"
          >
            <span className={running ? "animate-spin text-lg" : "text-lg"}>&#9654;</span>
            {running ? "Executing Complete Lifecycle..." : "Run Complete Capstone Demo"}
          </button>
        </div>
      </div>

      {/* Input parameters */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 bg-slate-900/90 border border-slate-800 rounded-2xl p-5">
        <div>
          <label className="text-xs font-medium text-slate-400 block mb-1">Target Destination</label>
          <select
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
            className="w-full bg-slate-800 border border-slate-700 text-sm text-white rounded-lg px-3 py-2"
          >
            <option value="Goa">Goa (Beach & Relaxation)</option>
            <option value="Delhi">Delhi (Heritage & Culture)</option>
            <option value="Mumbai">Mumbai (Coastal Metropolis)</option>
            <option value="Jaipur">Jaipur (Royal Heritage)</option>
          </select>
        </div>

        <div>
          <label className="text-xs font-medium text-slate-400 block mb-1">Trip Budget (INR)</label>
          <input
            type="number"
            value={budget}
            onChange={(e) => setBudget(Number(e.target.value))}
            className="w-full bg-slate-800 border border-slate-700 text-sm font-mono text-white rounded-lg px-3 py-2"
          />
        </div>

        <div>
          <label className="text-xs font-medium text-slate-400 block mb-1">Traveler Persona</label>
          <select
            value={travelerType}
            onChange={(e) => setTravelerType(e.target.value)}
            className="w-full bg-slate-800 border border-slate-700 text-sm text-white rounded-lg px-3 py-2"
          >
            <option value="couple">Couple / Romantic</option>
            <option value="solo">Solo Backpacker</option>
            <option value="family">Family with Kids</option>
          </select>
        </div>
      </div>

      {/* Execution Step Log */}
      {demoResult?.execution_steps_log && (
        <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-base font-semibold text-white">
                10-Stage Autonomous Execution Trace
              </h3>
              <p className="text-xs text-slate-400">
                Total pipeline execution time: <span className="text-emerald-400 font-mono font-bold">{demoResult.total_execution_time_ms} ms</span> &middot; Demo ID: <span className="font-mono text-indigo-300">{demoResult.demo_id}</span>
              </p>
            </div>
            <span className="px-3 py-1 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
              ALL 10 MODULES VERIFIED
            </span>
          </div>

          <div className="space-y-2.5">
            {demoResult.execution_steps_log.map((step: any) => (
              <div
                key={step.step}
                className="bg-slate-800/40 border border-slate-700/50 rounded-xl p-3.5 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs"
              >
                <div className="flex items-start gap-3">
                  <span className="w-6 h-6 rounded-md bg-indigo-600 flex items-center justify-center font-bold text-white text-[11px] shrink-0 mt-0.5">
                    {step.step}
                  </span>
                  <div>
                    <div className="font-bold text-white text-sm">{step.module_name}</div>
                    <div className="text-slate-300 mt-0.5 font-sans">{step.summary}</div>
                  </div>
                </div>

                <div className="flex items-center gap-3 shrink-0 font-mono text-[11px]">
                  <span className="text-slate-400">{step.duration_ms} ms</span>
                  <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold">
                    {step.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Final Synthesized Itinerary Card */}
      {demoResult?.assignment_modules?.["10_capstone_synthesis"]?.final_itinerary && (
        (() => {
          const it = demoResult.assignment_modules["10_capstone_synthesis"].final_itinerary;
          return (
            <div className="bg-gradient-to-br from-indigo-950/60 to-slate-900 border-2 border-indigo-500/40 rounded-2xl p-6 shadow-xl">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-4 mb-4">
                <div>
                  <div className="text-xs font-bold text-indigo-400 uppercase tracking-wider">
                    Synthesized Travel Plan &middot; Persisted to SQLite
                  </div>
                  <h3 className="text-2xl font-bold text-white mt-1">
                    {it.trip_request?.origin} &rarr; {it.trip_request?.destination} Expedition
                  </h3>
                  <p className="text-xs text-slate-400 mt-0.5">
                    Database Record ID: <span className="font-mono text-cyan-300 font-bold">{it.id}</span>
                  </p>
                </div>

                <div className="text-right">
                  <div className="text-xs text-slate-400 font-medium">TOTAL ITINERARY COST</div>
                  <div className="text-3xl font-extrabold text-white font-mono mt-0.5">
                    ₹{it.total_cost?.toLocaleString()}
                  </div>
                  <div className="text-xs text-emerald-400">
                    MAUT Utility Score: {it.utility_score} / 100
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-slate-900/70 p-4 rounded-xl border border-slate-800">
                  <div className="text-[11px] font-bold text-indigo-300 uppercase">Selected Flight</div>
                  <div className="text-sm font-bold text-white mt-1">{it.flight?.name}</div>
                  <div className="text-xs text-slate-400 font-mono mt-0.5">
                    Fare: ₹{it.flight?.price?.toLocaleString()} &middot; {it.flight?.stops} stops
                  </div>
                </div>

                <div className="bg-slate-900/70 p-4 rounded-xl border border-slate-800">
                  <div className="text-[11px] font-bold text-cyan-300 uppercase">Selected Accommodation</div>
                  <div className="text-sm font-bold text-white mt-1">{it.hotel?.name}</div>
                  <div className="text-xs text-slate-400 font-mono mt-0.5">
                    Cost: ₹{it.hotel?.price?.toLocaleString()} &middot; {it.hotel?.stars}&#9733;
                  </div>
                </div>

                <div className="bg-slate-900/70 p-4 rounded-xl border border-slate-800">
                  <div className="text-[11px] font-bold text-emerald-300 uppercase">Curated Activity Package</div>
                  <div className="text-sm font-bold text-white mt-1">{it.activities?.[0]?.package}</div>
                  <div className="text-xs text-slate-400 font-mono mt-0.5">
                    Activities: ₹{it.activities?.[0]?.price?.toLocaleString()}
                  </div>
                </div>
              </div>
            </div>
          );
        })()
      )}

      {/* Persisted History Table */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6">
        <h3 className="text-base font-semibold text-white mb-3">
          Saved Trip & Demo History (SQLite Database Persistence)
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 font-semibold uppercase tracking-wider">
                <th className="py-2.5 px-3">Trip ID</th>
                <th className="py-2.5 px-3">Route</th>
                <th className="py-2.5 px-3 text-right">Total Cost</th>
                <th className="py-2.5 px-3">Dates</th>
                <th className="py-2.5 px-3">Status</th>
                <th className="py-2.5 px-3">Created At</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-mono">
              {history.length > 0 ? (
                history.map((t: any) => (
                  <tr key={t.id} className="hover:bg-slate-800/40">
                    <td className="py-3 px-3 text-indigo-300 font-bold">{t.id}</td>
                    <td className="py-3 px-3 text-white font-sans">{t.origin} &rarr; {t.destination}</td>
                    <td className="py-3 px-3 text-right font-bold text-emerald-400">₹{t.total_cost?.toLocaleString()}</td>
                    <td className="py-3 px-3 text-slate-400">{t.start_date} to {t.end_date}</td>
                    <td className="py-3 px-3">
                      <span className="px-2 py-0.5 rounded text-[10px] bg-indigo-500/20 text-indigo-300 font-sans font-semibold">
                        {t.best_effort ? "Best Effort" : "Within Budget"}
                      </span>
                    </td>
                    <td className="py-3 px-3 text-slate-500">{t.created_at?.slice(0, 19).replace("T", " ")}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={6} className="py-8 text-center text-slate-500">
                    No stored itineraries yet. Run the demo above to generate and persist records.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
