import React, { useState, useEffect } from "react";
import { evaluateRules } from "../../services/smarttripApi";

export const RuleEngineSection: React.FC = () => {
  const [budget, setBudget] = useState(45000);
  const [travelerType, setTravelerType] = useState("couple");
  const [destination, setDestination] = useState("Goa");
  const [interests, setInterests] = useState<string[]>(["beach", "culture"]);
  const [passengers, setPassengers] = useState(2);
  const [result, setResult] = useState<any>(null);
  const [evaluating, setEvaluating] = useState(false);

  const availableInterests = ["beach", "culture", "mountains", "adventure", "watersports", "relaxation", "nightlife"];

  const toggleInterest = (tag: string) => {
    if (interests.includes(tag)) {
      setInterests(interests.filter((i) => i !== tag));
    } else {
      setInterests([...interests, tag]);
    }
  };

  const runEvaluation = async () => {
    setEvaluating(true);
    try {
      const data = await evaluateRules({
        origin: "DEL",
        destination,
        budget,
        traveler_type: travelerType,
        interests,
        passengers,
      });
      setResult(data);
    } catch (err) {
      console.error("Rule evaluation error", err);
    } finally {
      setEvaluating(false);
    }
  };

  // Run initial evaluation on mount
  useEffect(() => {
    runEvaluation();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl">
        <div className="text-xs font-semibold uppercase tracking-wider text-indigo-400 mb-1">
          Assignment 2 &middot; Knowledge & Decision Logic
        </div>
        <h2 className="text-2xl font-bold text-white">Condition-Action Rule Engine</h2>
        <p className="text-sm text-slate-400 mt-1">
          Forward-chaining inference engine applying prioritized travel preference rules, budget allocation shifts, and destination suitability matching.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Controls Card */}
        <div className="lg:col-span-5 bg-slate-900/90 border border-slate-800 rounded-2xl p-6 space-y-5">
          <h3 className="text-base font-semibold text-white border-b border-slate-800 pb-3">
            Inference Fact Inputs
          </h3>

          <div>
            <label className="block text-xs font-medium text-slate-400 mb-2">
              Traveler Persona
            </label>
            <div className="grid grid-cols-2 gap-2">
              {[
                { id: "solo", label: "Solo Backpacker" },
                { id: "couple", label: "Couple / Romantic" },
                { id: "family", label: "Family with Kids" },
                { id: "luxury", label: "Executive VIP" },
              ].map((t) => (
                <button
                  key={t.id}
                  type="button"
                  onClick={() => setTravelerType(t.id)}
                  className={`py-2 px-3 rounded-lg text-xs font-medium border text-left transition-all cursor-pointer ${
                    travelerType === t.id
                      ? "bg-indigo-600 border-indigo-500 text-white shadow"
                      : "bg-slate-800/60 border-slate-700 text-slate-300 hover:bg-slate-800"
                  }`}
                >
                  {t.label}
                </button>
              ))}
            </div>
          </div>

          <div>
            <div className="flex justify-between text-xs font-medium text-slate-400 mb-1">
              <span>Passenger Count</span>
              <span className="text-white font-mono">{passengers} Guests</span>
            </div>
            <div className="flex gap-2">
              {[1, 2, 4, 6].map((num) => (
                <button
                  key={num}
                  type="button"
                  onClick={() => setPassengers(num)}
                  className={`flex-1 py-1 rounded text-xs font-mono font-medium border ${
                    passengers === num
                      ? "bg-indigo-600 border-indigo-500 text-white"
                      : "bg-slate-800 border-slate-700 text-slate-400 hover:text-white"
                  }`}
                >
                  {num}
                </button>
              ))}
            </div>
          </div>

          <div>
            <div className="flex justify-between text-xs font-medium text-slate-400 mb-1">
              <span>Trip Budget (INR)</span>
              <span className="text-indigo-400 font-bold font-mono">₹{budget.toLocaleString()}</span>
            </div>
            <input
              type="range"
              min="15000"
              max="150000"
              step="5000"
              value={budget}
              onChange={(e) => setBudget(Number(e.target.value))}
              className="w-full accent-indigo-500 cursor-pointer"
            />
            <div className="flex justify-between text-[11px] text-slate-500 mt-1">
              <span>₹15K (Ultra-Budget)</span>
              <span>₹80K (Standard)</span>
              <span>₹150K (Luxury)</span>
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1.5">
              Destination City
            </label>
            <select
              value={destination}
              onChange={(e) => setDestination(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-indigo-500"
            >
              <option value="Goa">Goa (Coastal & Beaches)</option>
              <option value="Delhi">Delhi (Historic Mughal Heritage)</option>
              <option value="Mumbai">Mumbai (Coastal Metropolis)</option>
              <option value="Jaipur">Jaipur (Royal Palaces & UNESCO)</option>
              <option value="Manali">Manali (Northern Alpine Mountains)</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-400 mb-2">
              Interest Tags
            </label>
            <div className="flex flex-wrap gap-1.5">
              {availableInterests.map((interest) => (
                <button
                  key={interest}
                  type="button"
                  onClick={() => toggleInterest(interest)}
                  className={`px-2.5 py-1 rounded-md text-xs font-medium border transition-all cursor-pointer ${
                    interests.includes(interest)
                      ? "bg-indigo-500/20 border-indigo-500 text-indigo-300"
                      : "bg-slate-800/40 border-slate-700/60 text-slate-400 hover:text-slate-200"
                  }`}
                >
                  {interest}
                </button>
              ))}
            </div>
          </div>

          <button
            onClick={runEvaluation}
            disabled={evaluating}
            className="w-full py-2.5 px-4 rounded-xl bg-gradient-to-r from-indigo-500 to-indigo-600 hover:from-indigo-600 hover:to-indigo-700 text-white font-semibold text-sm shadow-md transition-all cursor-pointer disabled:opacity-50"
          >
            {evaluating ? "Evaluating Condition Rules..." : "Re-evaluate Condition-Action Rules"}
          </button>
        </div>

        {/* Results Card */}
        <div className="lg:col-span-7 space-y-5">
          {/* Ceilings Breakdown */}
          {result?.budget_ceilings && (
            <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5">
              <h3 className="text-sm font-semibold text-white mb-3">
                Inferred Category Budget Ceilings
              </h3>
              <div className="grid grid-cols-3 gap-3 text-center">
                <div className="bg-slate-800/60 border border-slate-700/60 rounded-xl p-3">
                  <div className="text-xs text-slate-400">Flight Ceiling</div>
                  <div className="text-lg font-bold text-indigo-400 font-mono mt-1">
                    ₹{result.budget_ceilings.flight?.toLocaleString()}
                  </div>
                  <div className="text-[11px] text-slate-500 mt-0.5">
                    {Math.round((result.budget_ceilings.flight / budget) * 100)}% of total
                  </div>
                </div>

                <div className="bg-slate-800/60 border border-slate-700/60 rounded-xl p-3">
                  <div className="text-xs text-slate-400">Hotel Ceiling</div>
                  <div className="text-lg font-bold text-cyan-400 font-mono mt-1">
                    ₹{result.budget_ceilings.hotel?.toLocaleString()}
                  </div>
                  <div className="text-[11px] text-slate-500 mt-0.5">
                    {Math.round((result.budget_ceilings.hotel / budget) * 100)}% of total
                  </div>
                </div>

                <div className="bg-slate-800/60 border border-slate-700/60 rounded-xl p-3">
                  <div className="text-xs text-slate-400">Activity Ceiling</div>
                  <div className="text-lg font-bold text-emerald-400 font-mono mt-1">
                    ₹{result.budget_ceilings.activity?.toLocaleString()}
                  </div>
                  <div className="text-[11px] text-slate-500 mt-0.5">
                    {Math.round((result.budget_ceilings.activity / budget) * 100)}% of total
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Applied Rules List */}
          <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-semibold text-white">
                Fired Rules ({result?.applied_rules?.length ?? 0})
              </h3>
              <span className="text-xs text-indigo-400 font-mono">
                Forward-chaining matched
              </span>
            </div>

            <div className="space-y-2.5">
              {result?.applied_rules?.map((rule: any, i: number) => (
                <div
                  key={i}
                  className="bg-slate-800/40 border border-slate-700/60 rounded-xl p-3.5 flex items-start justify-between gap-4"
                >
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-mono font-bold text-indigo-300">
                        {rule.rule_id}
                      </span>
                      <span className="text-xs px-2 py-0.5 rounded-full font-medium bg-slate-700 text-slate-200">
                        {rule.category}
                      </span>
                    </div>
                    <div className="text-sm font-semibold text-white mt-1">{rule.name}</div>
                    <div className="text-xs text-slate-400 mt-0.5">{rule.description}</div>
                  </div>
                  <span className="text-xs font-mono px-2 py-1 bg-indigo-950/80 text-indigo-300 border border-indigo-700/40 rounded-md shrink-0">
                    P: {rule.priority}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Recommended Tags & Alerts */}
          {result && (
            <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4">
              {result.recommended_tags?.length > 0 && (
                <div>
                  <h4 className="text-xs font-medium text-slate-400 mb-2">
                    Inferred Recommendation Tags
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {result.recommended_tags.map((tag: string, i: number) => (
                      <span
                        key={i}
                        className="px-2.5 py-1 rounded-full text-xs font-medium bg-cyan-500/10 text-cyan-300 border border-cyan-500/20"
                      >
                        #{tag}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {result.alerts?.length > 0 && (
                <div className="space-y-2 pt-2 border-t border-slate-800">
                  <h4 className="text-xs font-medium text-amber-400">
                    Active Heuristic Advisories
                  </h4>
                  {result.alerts.map((alert: string, i: number) => (
                    <div
                      key={i}
                      className="text-xs bg-amber-500/10 border border-amber-500/20 text-amber-300 rounded-lg p-2.5 flex items-start gap-2"
                    >
                      <span>&#9888;</span>
                      <span>{alert}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
