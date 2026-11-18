import React, { useState } from "react";
import { runSocketExchange } from "../../services/smarttripApi";

export const SocketCommSection: React.FC = () => {
  const [result, setResult] = useState<any>(null);
  const [running, setRunning] = useState(false);
  const [origin, setOrigin] = useState("DEL");
  const [destination, setDestination] = useState("GOI");
  const [budget, setBudget] = useState(45000);

  const executeSocketDemo = async () => {
    setRunning(true);
    try {
      const data = await runSocketExchange({ origin, destination, budget });
      setResult(data);
    } catch (err) {
      console.error("Socket exchange error", err);
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="text-xs font-semibold uppercase tracking-wider text-indigo-400 mb-1">
            Assignment 4 &middot; Network Protocol & Sockets
          </div>
          <h2 className="text-2xl font-bold text-white">
            TCP Client-Server Socket Communication
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            Low-level TCP stream socket connection between Agent A (Trip Coordinator) and Agent B (Resource Broker) with serialized JSON message framing.
          </p>
        </div>

        <button
          onClick={executeSocketDemo}
          disabled={running}
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-indigo-500 to-cyan-500 hover:from-indigo-600 hover:to-cyan-600 text-white text-xs font-semibold rounded-xl shadow-lg shadow-indigo-500/20 transition-all cursor-pointer disabled:opacity-50 shrink-0"
        >
          <span className={running ? "animate-spin" : ""}>&#8644;</span>
          {running ? "Exchanging TCP Frames..." : "Run TCP Socket Exchange"}
        </button>
      </div>

      {/* Input Parameters & Status Bar */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4">
          <label className="text-[11px] font-semibold text-slate-400 uppercase">Origin & Destination</label>
          <div className="flex items-center gap-2 mt-1">
            <input
              type="text"
              value={origin}
              onChange={(e) => setOrigin(e.target.value.toUpperCase())}
              className="w-16 bg-slate-800 border border-slate-700 text-sm font-mono text-center text-white rounded px-2 py-1"
            />
            <span className="text-slate-500">&rarr;</span>
            <input
              type="text"
              value={destination}
              onChange={(e) => setDestination(e.target.value.toUpperCase())}
              className="w-16 bg-slate-800 border border-slate-700 text-sm font-mono text-center text-white rounded px-2 py-1"
            />
          </div>
        </div>

        <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4">
          <label className="text-[11px] font-semibold text-slate-400 uppercase">Trip Budget</label>
          <div className="mt-1">
            <input
              type="number"
              value={budget}
              onChange={(e) => setBudget(Number(e.target.value))}
              className="w-full bg-slate-800 border border-slate-700 text-sm font-mono text-white rounded px-2 py-1"
            />
          </div>
        </div>

        <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4">
          <label className="text-[11px] font-semibold text-slate-400 uppercase">Socket Endpoint</label>
          <div className="text-sm font-mono text-cyan-400 mt-1">
            {result?.server_endpoint || "127.0.0.1:8999 (Loopback)"}
          </div>
        </div>

        <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4">
          <label className="text-[11px] font-semibold text-slate-400 uppercase">Network Roundtrip Latency</label>
          <div className="text-base font-mono font-bold text-emerald-400 mt-1">
            {result ? `${result.roundtrip_latency_ms} ms` : "—"}
          </div>
        </div>
      </div>

      {/* Frame Transcript */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-base font-semibold text-white">Chronological TCP Frame Stream</h3>
            <p className="text-xs text-slate-400">
              Bi-directional message transmission with byte sizing and delivery verification
            </p>
          </div>
          {result && (
            <div className="flex items-center gap-3 text-xs font-mono text-slate-400">
              <span>Frames: <strong className="text-white">{result.messages_count}</strong></span>
              <span>&middot;</span>
              <span>Total Bytes: <strong className="text-cyan-400">{result.total_bytes_exchanged} B</strong></span>
            </div>
          )}
        </div>

        {result?.transcript?.length > 0 ? (
          <div className="space-y-3 font-mono">
            {result.transcript.map((msg: any, i: number) => {
              const isAgentA = msg.role.includes("Agent A");
              return (
                <div
                  key={i}
                  className={`p-4 rounded-xl border transition-all ${
                    isAgentA
                      ? "bg-indigo-950/30 border-indigo-500/30 ml-0 mr-8"
                      : "bg-slate-800/50 border-slate-700/60 ml-8 mr-0"
                  }`}
                >
                  <div className="flex items-center justify-between text-xs mb-2">
                    <div className="flex items-center gap-2">
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          isAgentA
                            ? "bg-indigo-500/20 text-indigo-300 border border-indigo-500/30"
                            : "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30"
                        }`}
                      >
                        {msg.role}
                      </span>
                      <span className="text-white font-semibold text-[11px]">
                        {msg.event}
                      </span>
                    </div>
                    <div className="flex items-center gap-2 text-slate-400 text-[11px]">
                      <span>{msg.raw_bytes} bytes</span>
                      <span>&middot;</span>
                      <span>{msg.timestamp?.split("T")[1]?.slice(0, 12)}</span>
                    </div>
                  </div>

                  <pre className="text-[11px] bg-slate-950/80 p-3 rounded-lg text-slate-300 overflow-x-auto border border-slate-900">
                    {JSON.stringify(msg.payload, null, 2)}
                  </pre>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="py-12 text-center text-slate-500 text-sm">
            Socket demonstration has not been executed yet. Click &ldquo;Run TCP Socket Exchange&rdquo; to initiate the handshake.
          </div>
        )}
      </div>
    </div>
  );
};
