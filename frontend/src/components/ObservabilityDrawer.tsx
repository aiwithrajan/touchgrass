import React, { useState, useEffect } from 'react';
import { AgentTrace } from '../types';
import { api } from '../api';
import { Activity, RefreshCw, Clock, CheckCircle2, ShieldAlert, Cpu } from 'lucide-react';

export const ObservabilityDrawer: React.FC = () => {
  const [traces, setTraces] = useState<AgentTrace[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const loadTraces = async () => {
    setLoading(true);
    const data = await api.getObservabilityTraces();
    setTraces(data);
    setLoading(false);
  };

  useEffect(() => {
    loadTraces();
  }, []);

  return (
    <div className="w-full max-w-2xl mx-auto space-y-6 pt-2 pb-12 animate-in fade-in duration-500">
      {/* Header */}
      <div className="rounded-2xl bg-gradient-to-r from-emerald-950 to-[#0e2116] border border-emerald-700/40 p-5 flex items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-purple-500/20 border border-purple-500/40 flex items-center justify-center text-purple-300">
            <Activity className="w-5 h-5 text-purple-400" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h2 className="text-base font-bold text-white">Sentry Agent Traces</h2>
              <span className="text-[10px] bg-purple-500/20 text-purple-300 border border-purple-500/40 px-2 py-0.5 rounded-full font-bold">
                OBSERVABILITY
              </span>
            </div>
            <p className="text-xs text-emerald-300/70">
              Live inspection of Gemma agent reasoning spans, policy filters, and execution latency.
            </p>
          </div>
        </div>

        <button
          onClick={loadTraces}
          disabled={loading}
          className="p-2.5 rounded-xl bg-emerald-900/40 hover:bg-emerald-800/60 text-emerald-300 border border-emerald-700/40 cursor-pointer transition-all"
          title="Refresh Traces"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      {/* Traces Timeline */}
      <div className="space-y-3">
        {traces.length > 0 ? (
          traces.map((trace, idx) => (
            <div
              key={idx}
              className="rounded-2xl bg-[#0f1d16] border border-emerald-800/40 p-4 space-y-2.5 hover:border-emerald-700/60 transition-colors"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Cpu className="w-4 h-4 text-emerald-400" />
                  <span className="font-mono text-xs font-bold text-emerald-100">
                    {trace.step}
                  </span>
                </div>
                <div className="flex items-center space-x-1.5 text-xs font-mono font-semibold text-amber-400 bg-emerald-950 px-2.5 py-1 rounded-md border border-emerald-800/50">
                  <Clock className="w-3 h-3 text-amber-400" />
                  <span>{trace.duration_ms} ms</span>
                </div>
              </div>

              {/* Metadata JSON */}
              <div className="bg-[#08120c] rounded-xl p-3 border border-emerald-950 text-[11px] font-mono text-emerald-300/80 overflow-x-auto">
                <pre>{JSON.stringify(trace.metadata, null, 2)}</pre>
              </div>
            </div>
          ))
        ) : (
          <div className="text-center py-12 text-xs text-emerald-400/60">
            No agent traces recorded yet. Generate a mission to inspect spans.
          </div>
        )}
      </div>
    </div>
  );
};
