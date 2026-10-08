import { useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import stockService from '../services/stockService';

const AIInvestmentThesis = ({ symbol, predictionData }) => {
  const [thesis, setThesis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  // Auto-fetch or reset when symbol changes
  useEffect(() => {
    setThesis(null);
    setLoading(false);
  }, [symbol]);

  const handleFetchThesis = async () => {
    if (!symbol) return;
    setLoading(true);
    try {
      const res = await stockService.getThesis(symbol);
      if (res.success && res.thesis) {
        setThesis(res);
        toast.success(`AI Bull/Bear Thesis generated for ${symbol.toUpperCase()}!`);
      } else {
        toast.error('Unable to generate AI thesis at this time.');
      }
    } catch (err) {
      console.error('Error fetching thesis:', err);
      toast.error('Failed to connect to AI thesis service.');
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    if (!thesis?.thesis) return;
    const t = thesis.thesis;
    const textToCopy = `StockSphere AI Investment Thesis (${symbol.toUpperCase()}):
Trend: ${thesis.metrics?.trend || 'N/A'}
5-Day Target: $${thesis.metrics?.targetPrice || 'N/A'} (${thesis.metrics?.pctChange >= 0 ? '+' : ''}${thesis.metrics?.pctChange}%)

Executive Summary:
${t.summary}

Bull Case:
${t.bullCase?.map((b) => `• ${b}`).join('\n')}

Bear Case:
${t.bearCase?.map((b) => `• ${b}`).join('\n')}

Actionable Plan:
${t.actionableVerdict || 'N/A'}
`;
    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    toast.success('AI Thesis copied to clipboard!');
    setTimeout(() => setCopied(false), 2000);
  };

  const trend = thesis?.metrics?.trend || predictionData?.metrics?.trend || 'Bullish';
  const isBull = trend === 'Bullish';
  const isBear = trend === 'Bearish';

  return (
    <div className="card p-6 bg-gradient-to-br from-dark-800 via-dark-850 to-dark-900 border border-purple-500/20 shadow-xl rounded-2xl animate-fade-in relative overflow-hidden">
      {/* Decorative gradient blur */}
      <div className="absolute top-0 right-0 -mr-16 -mt-16 w-56 h-56 bg-accent-purple/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 left-0 -ml-16 -mb-16 w-56 h-56 bg-accent-green/10 rounded-full blur-3xl pointer-events-none" />

      {/* Header section */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6 relative z-10 border-b border-surface-border pb-5">
        <div className="flex items-center gap-3">
          <div className="w-11 h-11 bg-gradient-to-br from-accent-purple/20 to-accent-blue/20 border border-accent-purple/40 rounded-xl flex items-center justify-center text-2xl shadow-inner">
            🧠
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="font-display font-bold text-white text-lg tracking-tight">
                AI Bull / Bear Investment Thesis
              </h3>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-semibold bg-accent-purple/20 text-accent-purple border border-accent-purple/30">
                Explainable AI (XAI)
              </span>
            </div>
            <p className="text-gray-400 text-xs mt-0.5">
              Generative AI translation of mathematical Machine Learning projections into human-understandable market strategy.
            </p>
          </div>
        </div>

        {/* Action Button */}
        <div className="flex items-center gap-2">
          {thesis && (
            <button
              onClick={handleCopy}
              className="px-3 py-1.5 rounded-xl text-xs font-mono font-medium border border-surface-border bg-dark-900/60 text-gray-300 hover:text-white hover:border-gray-500 transition-all flex items-center gap-1.5"
              title="Copy thesis to clipboard"
            >
              <span>{copied ? '✓' : '📋'}</span>
              <span>{copied ? 'COPIED' : 'COPY'}</span>
            </button>
          )}

          <button
            onClick={handleFetchThesis}
            disabled={loading}
            className={`px-4 py-2 rounded-xl text-xs font-mono font-bold border transition-all duration-200 flex items-center gap-2 shadow-lg ${
              loading
                ? 'bg-dark-900 border-surface-border text-gray-500 cursor-not-allowed'
                : 'bg-gradient-to-r from-accent-purple/20 to-accent-blue/20 border-accent-purple/40 text-purple-200 hover:from-accent-purple/30 hover:to-accent-blue/30 hover:border-accent-purple'
            }`}
          >
            {loading ? (
              <>
                <div className="w-3.5 h-3.5 border-2 border-accent-purple border-t-transparent rounded-full animate-spin" />
                <span>SYNTHESIZING WITH GENAI...</span>
              </>
            ) : (
              <>
                <span>✨</span>
                <span>{thesis ? 'REFRESH AI THESIS' : 'GENERATE AI THESIS'}</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Body Section */}
      {!thesis && !loading && (
        <div className="py-10 text-center relative z-10">
          <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-dark-900/70 border border-surface-border flex items-center justify-center text-3xl">
            🔮
          </div>
          <h4 className="font-display font-semibold text-white text-base mb-1">
            Generate Explainable AI Investment Thesis
          </h4>
          <p className="text-gray-400 text-xs max-w-md mx-auto mb-5 leading-relaxed">
            Bridge your raw 5-day ML polynomial forecast with institutional-grade reasoning. Generative AI will analyze the quadratic slope, confidence intervals, and key resistance levels to synthesize the bull and bear scenarios.
          </p>
          <button
            onClick={handleFetchThesis}
            className="px-5 py-2.5 rounded-xl text-xs font-mono font-bold bg-accent-purple text-white hover:bg-accent-purple/90 transition-all shadow-glow inline-flex items-center gap-2"
          >
            <span>✨</span>
            <span>GENERATE BULL / BEAR THESIS NOW</span>
          </button>
        </div>
      )}

      {loading && (
        <div className="py-12 text-center relative z-10 space-y-4">
          <div className="relative w-16 h-16 mx-auto">
            <div className="absolute inset-0 rounded-full border-2 border-accent-purple/30 animate-ping" />
            <div className="w-16 h-16 rounded-full border-2 border-accent-purple border-t-transparent animate-spin flex items-center justify-center text-2xl">
              🧠
            </div>
          </div>
          <div>
            <h4 className="font-display font-semibold text-white text-sm">
              Analyzing ML Curvature & Grounding Insights...
            </h4>
            <p className="text-gray-500 text-xs font-mono mt-1">
              Extracting OLS polynomial coefficients • Assessing 95% confidence bounds • Generating synthesis
            </p>
          </div>
        </div>
      )}

      {thesis && !loading && (
        <div className="space-y-6 relative z-10 animate-fade-in">
          {/* Key Metrics Banner */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="bg-dark-900/60 border border-surface-border rounded-xl p-3">
              <span className="text-gray-500 text-[10px] font-mono uppercase tracking-wider block mb-1">
                ML Signal
              </span>
              <span
                className={`inline-flex items-center gap-1 font-mono font-bold text-xs px-2 py-0.5 rounded-md ${
                  isBull
                    ? 'bg-accent-green/15 text-accent-green border border-accent-green/30'
                    : isBear
                    ? 'bg-accent-red/15 text-accent-red border border-accent-red/30'
                    : 'bg-blue-500/15 text-blue-400 border border-blue-500/30'
                }`}
              >
                {trend.toUpperCase()} {isBull ? '📈' : isBear ? '📉' : '➡️'}
              </span>
            </div>

            <div className="bg-dark-900/60 border border-surface-border rounded-xl p-3">
              <span className="text-gray-500 text-[10px] font-mono uppercase tracking-wider block mb-1">
                5-Day ML Target
              </span>
              <span className="font-mono font-bold text-sm text-white">
                ${thesis.metrics?.targetPrice}
                <span
                  className={`text-xs ml-1 ${
                    Number(thesis.metrics?.pctChange) >= 0 ? 'text-accent-green' : 'text-accent-red'
                  }`}
                >
                  ({Number(thesis.metrics?.pctChange) >= 0 ? '+' : ''}
                  {thesis.metrics?.pctChange}%)
                </span>
              </span>
            </div>

            <div className="bg-dark-900/60 border border-surface-border rounded-xl p-3">
              <span className="text-gray-500 text-[10px] font-mono uppercase tracking-wider block mb-1">
                Risk Profile
              </span>
              <span
                className={`font-mono font-bold text-xs px-2 py-0.5 rounded-md inline-block ${
                  thesis.thesis?.riskLevel === 'Low'
                    ? 'bg-accent-green/15 text-accent-green'
                    : thesis.thesis?.riskLevel === 'High'
                    ? 'bg-accent-red/15 text-accent-red'
                    : 'bg-yellow-500/15 text-yellow-400'
                }`}
              >
                {thesis.thesis?.riskLevel || 'Moderate'} Risk
              </span>
            </div>

            <div className="bg-dark-900/60 border border-surface-border rounded-xl p-3">
              <span className="text-gray-500 text-[10px] font-mono uppercase tracking-wider block mb-1">
                Intelligence Source
              </span>
              <span className="text-[11px] font-mono text-purple-300 font-semibold truncate block" title={thesis.thesis?.source}>
                {thesis.thesis?.source || 'Gemini 1.5 Flash (XAI)'}
              </span>
            </div>
          </div>

          {/* Executive Summary */}
          <div className="bg-dark-900/70 border border-accent-purple/30 rounded-xl p-4 relative overflow-hidden">
            <div className="flex items-center gap-2 mb-2 text-accent-purple text-xs font-mono font-bold uppercase tracking-wider">
              <span>⚡</span>
              <span>Executive Analyst Thesis</span>
            </div>
            <p className="text-gray-200 text-sm leading-relaxed font-body">
              {thesis.thesis?.summary}
            </p>
          </div>

          {/* Two-Column Bull vs Bear Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Bull Case */}
            <div className="bg-dark-900/50 border border-accent-green/20 rounded-xl p-4 relative flex flex-col justify-between">
              <div>
                <div className="flex items-center gap-2 mb-3 pb-2 border-b border-surface-border">
                  <span className="text-base">🟢</span>
                  <h4 className="font-display font-bold text-accent-green text-sm">
                    The Bull Case (Upside Catalysts)
                  </h4>
                </div>
                <ul className="space-y-2.5">
                  {thesis.thesis?.bullCase?.map((item, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-xs text-gray-300 leading-relaxed">
                      <span className="text-accent-green font-bold mt-0.5">▸</span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
              <div className="mt-4 pt-3 border-t border-surface-border/50 text-[10px] font-mono text-accent-green/80">
                PROJECTION BIAS: Positive Curvature Expansion
              </div>
            </div>

            {/* Bear Case */}
            <div className="bg-dark-900/50 border border-accent-red/20 rounded-xl p-4 relative flex flex-col justify-between">
              <div>
                <div className="flex items-center gap-2 mb-3 pb-2 border-b border-surface-border">
                  <span className="text-base">🔴</span>
                  <h4 className="font-display font-bold text-accent-red text-sm">
                    The Bear Case (Downside Risks)
                  </h4>
                </div>
                <ul className="space-y-2.5">
                  {thesis.thesis?.bearCase?.map((item, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-xs text-gray-300 leading-relaxed">
                      <span className="text-accent-red font-bold mt-0.5">▸</span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
              <div className="mt-4 pt-3 border-t border-surface-border/50 text-[10px] font-mono text-accent-red/80">
                RISK THRESHOLD: Confidence Margin Breakdown
              </div>
            </div>
          </div>

          {/* Actionable Strategy & Trading Verdict */}
          {thesis.thesis?.actionableVerdict && (
            <div className="bg-gradient-to-r from-dark-900/80 to-dark-850 border border-surface-border rounded-xl p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-accent-blue/15 border border-accent-blue/30 flex items-center justify-center text-base">
                  🎯
                </div>
                <div>
                  <h5 className="font-mono text-xs font-bold text-accent-blue uppercase tracking-wider">
                    Virtual Trading Tactical Plan
                  </h5>
                  <p className="text-xs text-gray-300 mt-0.5 font-body leading-relaxed">
                    {thesis.thesis.actionableVerdict}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* College Project / Viva Footnote */}
          <div className="border-t border-surface-border/60 pt-3 flex items-center justify-between text-[11px] text-gray-500 font-mono">
            <span>🎓 Explainable AI (XAI) Synthesis: ML Math → Natural Language Intelligence</span>
            <span>Generated: {new Date(thesis.generatedAt || Date.now()).toLocaleTimeString()}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default AIInvestmentThesis;
