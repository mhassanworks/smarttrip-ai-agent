import React, { useEffect, useState } from "react";
import { fetchConcurrencyStatus, triggerConcurrencyBatch } from "../../services/smarttripApi";

export const ConcurrencySection: React.FC = () => {
  const [status, setStatus] = useState<any>(null);
  const [triggering, setTriggering] = useState(false);
  const [batchCount, setBatchCount] = useState(5);

  const loadStatus = async () => {
    try {
      const data = await fetchConcurrencyStatus();
      setStatus(data);
    } catch (err) {
      console.error("Concurrency fetch error", err);
    }
  };

  useEffect(() => {
    loadStatus();
    const interval = setInterval(loadStatus, 4000);
    return () => clearInterval(interval);
  }, []);

  const handleTrigger = async () => {
    setTriggering(true);
    try {
      await triggerConcurrencyBatch(batchCount);
      await loadStatus();
    } catch (err) {
      console.error("Trigger batch error", err);
    } finally {
      setTriggering(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="text-xs font-semibold uppercase tracking-wider text-indigo-400 mb-1">
            Assignment 3 &middot; Threading & Concurrency
          </div>
          <h2 className="text-2xl font-bold text-white">
            Background Monitoring & Latency Telemetry
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            Multi-threaded Python worker pool using thread-safe queues and mutex locks. Accurately measures sub-millisecond task execution latency.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <select
            value={batchCount}
            onChange={(e) => setBatchCount(Number(e.target.value))}
            className="bg-slate-800 border border-slate-700 text-xs text-white rounded-lg px-2.5 py-2"
          >
            <option value={3}>3 Tasks</option>
            <option value={5}>5 Tasks</option>
            <option value={10}>10 Tasks</option>
          </select>
          <button
            onClick={handleTrigger}
            disabled={triggering}
            className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold rounded-lg shadow-md transition-all cursor-pointer disabled:opacity-50"
          >
            <span className={triggering ? "animate-spin" : ""}>&#9881;</span>
            {triggering ? "Dispatching..." : "Trigger Load Batch"}
          </button>
        </div>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5">
          <div className="text-xs font-medium text-slate-400">ACTIVE WORKER THREADS</div>
          <div className="text-2xl font-bold text-indigo-400 mt-2">
            {status?.active_workers ?? 3}
          </div>
          <div className="text-xs text-slate-500 mt-1 font-mono">
            {status?.worker_threads?.join(", ") || "SmartTripWorker-1, 2, 3"}
          </div>
        </div>

        <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5">
          <div className="text-xs font-medium text-slate-400">THREAD-SAFE QUEUE DEPTH</div>
          <div className="text-2xl font-bold text-cyan-400 mt-2">
            {status?.queue_depth ?? 0}
          </div>
          <div className="text-xs text-slate-500 mt-1">
            Tasks currently waiting in FIFO Queue
          </div>
        </div>

        <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5">
          <div className="text-xs font-medium text-slate-400">AVERAGE PROCESSING LATENCY</div>
          <div className="text-2xl font-bold text-emerald-400 mt-2 font-mono">
            {status?.latency_metrics?.avg_processing_ms ?? 0.0} ms
          </div>
          <div className="text-xs text-slate-500 mt-1">
            Range: {status?.latency_metrics?.min_processing_ms ?? 0}ms &ndash; {status?.latency_metrics?.max_processing_ms ?? 0}ms
          </div>
        </div>

        <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5">
          <div className="text-xs font-medium text-slate-400">TOTAL TASKS PROCESSED</div>
          <div className="text-2xl font-bold text-amber-400 mt-2">
            {status?.total_tasks_processed ?? 0}
          </div>
          <div className="text-xs text-slate-500 mt-1">
            Thread-safe counter protected by mutex lock
          </div>
        </div>
      </div>

      {/* Latency Log Table */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-base font-semibold text-white">
            Recent Worker Execution Records (Microsecond Precision)
          </h3>
          <span className="text-xs font-mono text-slate-400">
            Real-time telemetry buffer
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 font-semibold uppercase tracking-wider">
                <th className="py-2.5 px-3">Task ID</th>
                <th className="py-2.5 px-3">Type</th>
                <th className="py-2.5 px-3">Target</th>
                <th className="py-2.5 px-3">Worker Thread</th>
                <th className="py-2.5 px-3 text-right">Queued (ms)</th>
                <th className="py-2.5 px-3 text-right">Execution (ms)</th>
                <th className="py-2.5 px-3 text-right">Total (ms)</th>
                <th className="py-2.5 px-3 text-center">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-mono">
              {status?.recent_executions?.length > 0 ? (
                status.recent_executions.slice().reverse().map((rec: any, idx: number) => (
                  <tr key={idx} className="hover:bg-slate-800/40">
                    <td className="py-3 px-3 text-indigo-300 font-bold">{rec.task_id}</td>
                    <td className="py-3 px-3 text-slate-200">{rec.task_type}</td>
                    <td className="py-3 px-3 text-slate-400">{rec.target}</td>
                    <td className="py-3 px-3 text-slate-300">{rec.worker_name}</td>
                    <td className="py-3 px-3 text-right text-slate-400">{rec.queued_duration_ms}</td>
                    <td className="py-3 px-3 text-right text-emerald-400 font-bold">{rec.processing_latency_ms}</td>
                    <td className="py-3 px-3 text-right text-cyan-300">{rec.total_latency_ms}</td>
                    <td className="py-3 px-3 text-center">
                      <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-500/20 text-emerald-300">
                        {rec.status}
                      </span>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={8} className="py-8 text-center text-slate-500">
                    No task executions recorded yet. Click "Trigger Load Batch" above to execute background tasks.
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
