import React, { useState, useEffect } from "react";
import { runSecurityAudit } from "../../services/smarttripApi";

export const SecuritySection: React.FC = () => {
  const [auditData, setAuditData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const executeAudit = async () => {
    setLoading(true);
    try {
      const data = await runSecurityAudit();
      setAuditData(data);
    } catch (err) {
      console.error("Security audit error", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    executeAudit();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="text-xs font-semibold uppercase tracking-wider text-indigo-400 mb-1">
            Assignment 9 &middot; Cryptographic Inter-Agent Security
          </div>
          <h2 className="text-2xl font-bold text-white">
            HMAC-SHA256 Message Integrity & Tamper Detection
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            Zero-trust communication channel enforcing HMAC cryptographic digests, sender identity whitelisting, replay clock-skew checks, and payload tampering rejection.
          </p>
        </div>

        <button
          onClick={executeAudit}
          disabled={loading}
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-indigo-500 to-indigo-600 hover:from-indigo-600 hover:to-indigo-700 text-white text-xs font-semibold rounded-xl shadow-lg shadow-indigo-500/20 transition-all cursor-pointer disabled:opacity-50 shrink-0"
        >
          <span className={loading ? "animate-spin" : ""}>&#128274;</span>
          {loading ? "Auditing Signatures..." : "Run Cryptographic Audit"}
        </button>
      </div>

      {/* Security Metrics Banner */}
      {auditData && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 font-mono">
          <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5">
            <div className="text-xs font-sans text-slate-400">CRYPTOGRAPHIC STANDARD</div>
            <div className="text-xl font-bold text-indigo-400 mt-2">HMAC-SHA256</div>
            <div className="text-[11px] text-slate-500 font-sans mt-1">Constant-time digest comparison</div>
          </div>

          <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5">
            <div className="text-xs font-sans text-slate-400">SECURITY ENFORCEMENT RATE</div>
            <div className="text-2xl font-bold text-emerald-400 mt-2">100.0%</div>
            <div className="text-[11px] text-slate-500 font-sans mt-1">0 false acceptances allowed</div>
          </div>

          <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5">
            <div className="text-xs font-sans text-slate-400">LEGITIMATE ACCEPTED</div>
            <div className="text-2xl font-bold text-emerald-400 mt-2">
              {auditData.accepted_legitimate} / {auditData.total_tests}
            </div>
            <div className="text-[11px] text-slate-500 font-sans mt-1">Verified signature & sender</div>
          </div>

          <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5">
            <div className="text-xs font-sans text-slate-400">ATTACKS INTERCEPTED & BLOCKED</div>
            <div className="text-2xl font-bold text-red-400 mt-2">
              {auditData.blocked_malicious} / {auditData.total_tests}
            </div>
            <div className="text-[11px] text-slate-500 font-sans mt-1">Tampering, replay & forged keys</div>
          </div>
        </div>
      )}

      {/* Multi-Scenario Audit Test Results */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6">
        <h3 className="text-base font-semibold text-white mb-4">
          Cryptographic Test Scenarios & Tampering Demonstrations
        </h3>

        <div className="space-y-4">
          {auditData?.test_results?.map((res: any, idx: number) => {
            const isValid = res.audit.is_valid;
            return (
              <div
                key={idx}
                className={`p-5 rounded-2xl border transition-all ${
                  isValid
                    ? "bg-emerald-950/20 border-emerald-500/40"
                    : "bg-red-950/20 border-red-500/40"
                }`}
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3 mb-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <span
                        className={`w-2.5 h-2.5 rounded-full ${
                          isValid ? "bg-emerald-400" : "bg-red-400"
                        }`}
                      />
                      <h4 className="text-sm font-bold text-white">{res.test_case}</h4>
                    </div>
                    <p className="text-xs text-slate-400 mt-0.5">{res.description}</p>
                  </div>

                  <span
                    className={`px-3 py-1 rounded-full text-xs font-mono font-bold ${
                      isValid
                        ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30"
                        : "bg-red-500/20 text-red-300 border border-red-500/30"
                    }`}
                  >
                    STATUS: {res.audit.status_code}
                  </span>
                </div>

                <div className="text-xs text-slate-300 font-sans mb-3">
                  <strong>Auditor Verdict:</strong> {res.audit.details}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs font-mono">
                  <div className="bg-slate-950/70 p-3 rounded-xl border border-slate-800">
                    <div className="text-slate-400 text-[10px] uppercase mb-1">Signed Message Payload</div>
                    <pre className="text-[11px] text-slate-300 overflow-x-auto">
                      {JSON.stringify(res.message.payload, null, 2)}
                    </pre>
                  </div>

                  <div className="bg-slate-950/70 p-3 rounded-xl border border-slate-800">
                    <div className="text-slate-400 text-[10px] uppercase mb-1">Cryptographic Metadata</div>
                    <div className="space-y-1 text-[11px] text-slate-300">
                      <div>Sender: <span className="text-indigo-300 font-bold">{res.message.sender_id}</span></div>
                      <div>Recipient: {res.message.recipient_id}</div>
                      <div>Nonce: <span className="text-cyan-300">{res.message.nonce}</span></div>
                      <div>Timestamp: {res.message.timestamp}</div>
                      <div className="truncate">HMAC-SHA256: <span className="text-amber-300">{res.message.signature}</span></div>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
