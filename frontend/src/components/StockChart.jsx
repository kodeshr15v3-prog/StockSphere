import { useState, useEffect, useRef } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import stockService from '../services/stockService';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

const TIMEFRAMES = [
  { label: '1D', resolution: '60', days: 1 },
  { label: '1W', resolution: 'D', days: 7 },
  { label: '1M', resolution: 'D', days: 30 },
  { label: '1Y', resolution: 'W', days: 365 },
];

const StockChart = ({ symbol, predictionsData, predictionsActive, predictionsLoading, onTogglePredictions }) => {
  const [candles, setCandles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTimeframe, setActiveTimeframe] = useState(TIMEFRAMES[2]); // 1M default

  useEffect(() => {
    const fetchCandles = async () => {
      setLoading(true);
      setError(null);
      try {
        const now = Math.floor(Date.now() / 1000);
        const from = now - activeTimeframe.days * 24 * 60 * 60;
        const data = await stockService.getCandles(symbol, activeTimeframe.resolution, from, now);
        setCandles(data.candles || []);
      } catch (err) {
        setError('Failed to load chart data');
      } finally {
        setLoading(false);
      }
    };

    if (symbol) fetchCandles();
  }, [symbol, activeTimeframe]);

  const isPositive = candles.length >= 2
    ? candles[candles.length - 1].close >= candles[0].close
    : true;

  const color = isPositive ? '#00d4aa' : '#ff4d6d';
  const colorDim = isPositive ? 'rgba(0,212,170,0.1)' : 'rgba(255,77,109,0.1)';

  const formatLabel = (timestamp) => {
    const d = new Date(timestamp * 1000);
    if (activeTimeframe.label === '1D') {
      return d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false });
    }
    if (activeTimeframe.label === '1Y') {
      return d.toLocaleDateString('en-US', { month: 'short', year: '2-digit' });
    }
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  const hasPredictions = predictionsData && predictionsData.predictions && predictionsData.predictions.length > 0;

  const historicalLabels = candles.map((c) => formatLabel(c.time));
  const predictedLabels = hasPredictions 
    ? predictionsData.predictions.map((p) => {
        const d = new Date(p.time * 1000);
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
      }) 
    : [];

  const labels = [...historicalLabels, ...predictedLabels];

  const datasets = [
    {
      label: 'Historical Price',
      data: candles.map((c) => c.close),
      borderColor: color,
      borderWidth: 2,
      backgroundColor: (ctx) => {
        const gradient = ctx.chart.ctx.createLinearGradient(0, 0, 0, 300);
        gradient.addColorStop(0, colorDim);
        gradient.addColorStop(1, 'rgba(0,0,0,0)');
        return gradient;
      },
      fill: !hasPredictions, // Disable fill when predictions are shown for a cleaner look
      tension: 0.3,
      pointRadius: 0,
      pointHoverRadius: 4,
      pointHoverBackgroundColor: color,
      pointHoverBorderColor: '#fff',
      pointHoverBorderWidth: 2,
    }
  ];

  if (hasPredictions) {
    const isTrendBullish = predictionsData.metrics.trend === 'Bullish';
    const isTrendBearish = predictionsData.metrics.trend === 'Bearish';
    const predColor = isTrendBullish ? '#00d4aa' : isTrendBearish ? '#ff4d6d' : '#60a5fa';

    // Pad future datasets with nulls for historical points (except the last one to connect lines)
    const predictedData = Array(candles.length - 1).fill(null);
    const confidenceHighData = Array(candles.length - 1).fill(null);
    const confidenceLowData = Array(candles.length - 1).fill(null);

    if (candles.length > 0) {
      const lastClose = candles[candles.length - 1].close;
      predictedData.push(lastClose);
      confidenceHighData.push(lastClose);
      confidenceLowData.push(lastClose);
    }

    predictionsData.predictions.forEach((p) => {
      predictedData.push(p.close);
      confidenceHighData.push(p.confidenceHigh);
      confidenceLowData.push(p.confidenceLow);
    });

    datasets.push({
      label: 'AI Forecast',
      data: predictedData,
      borderColor: predColor,
      borderWidth: 2,
      borderDash: [6, 4],
      fill: false,
      tension: 0.3,
      pointRadius: 0,
      pointHoverRadius: 5,
      pointHoverBackgroundColor: predColor,
      pointHoverBorderColor: '#fff',
      pointHoverBorderWidth: 2,
    });

    datasets.push({
      label: 'Confidence High (95%)',
      data: confidenceHighData,
      borderColor: 'rgba(148, 163, 184, 0.25)',
      borderWidth: 1,
      borderDash: [3, 3],
      fill: false,
      tension: 0.3,
      pointRadius: 0,
      pointHoverRadius: 0,
    });

    datasets.push({
      label: 'Confidence Low (95%)',
      data: confidenceLowData,
      borderColor: 'rgba(148, 163, 184, 0.25)',
      borderWidth: 1,
      borderDash: [3, 3],
      fill: false,
      tension: 0.3,
      pointRadius: 0,
      pointHoverRadius: 0,
    });
  }

  const chartData = {
    labels,
    datasets,
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    animation: { duration: 600, easing: 'easeInOutQuart' },
    interaction: { intersect: false, mode: 'index' },
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: '#1a2235',
        borderColor: '#2a3548',
        borderWidth: 1,
        titleColor: '#94a3b8',
        bodyColor: '#fff',
        titleFont: { family: 'JetBrains Mono', size: 11 },
        bodyFont: { family: 'JetBrains Mono', size: 13, weight: 'bold' },
        padding: 12,
        displayColors: true, // Display color box to differentiate datasets
        callbacks: {
          label: (ctx) => {
            const label = ctx.dataset.label || '';
            const val = ctx.parsed.y;
            return ` ${label}: $${val.toFixed(2)}`;
          },
        },
      },
    },
    scales: {
      x: {
        grid: { display: false },
        border: { display: false },
        ticks: {
          color: '#4b5563',
          font: { family: 'JetBrains Mono', size: 10 },
          maxTicksLimit: 8,
          maxRotation: 0,
        },
      },
      y: {
        position: 'right',
        grid: { color: '#1a2235', drawBorder: false },
        border: { display: false, dash: [4, 4] },
        ticks: {
          color: '#4b5563',
          font: { family: 'JetBrains Mono', size: 10 },
          callback: (val) => `$${val.toFixed(2)}`,
          maxTicksLimit: 6,
        },
      },
    },
  };

  return (
    <div className="card p-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <h3 className="font-display font-semibold text-white">Price Chart</h3>
          {candles.length >= 2 && (
            <p className={`text-xs font-mono mt-1 ${isPositive ? 'text-accent-green' : 'text-accent-red'}`}>
              {isPositive ? '▲' : '▼'} {Math.abs(((candles[candles.length-1].close - candles[0].close) / candles[0].close) * 100).toFixed(2)}% this period
            </p>
          )}
        </div>

        <div className="flex flex-wrap items-center gap-3">
          {/* AI Predictor Toggle */}
          <button
            onClick={onTogglePredictions}
            disabled={predictionsLoading}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-mono font-bold border transition-all duration-200 ${
              predictionsActive
                ? 'bg-accent-green/10 border-accent-green text-accent-green hover:bg-accent-green/20'
                : 'border-surface-border bg-dark-800 text-gray-400 hover:border-gray-600 hover:text-white'
            }`}
          >
            {predictionsLoading ? (
              <>
                <div className="w-3 h-3 border border-current border-t-transparent rounded-full animate-spin" />
                <span>CALCULATING...</span>
              </>
            ) : (
              <>
                <span>✨</span>
                <span>{predictionsActive ? 'AI PREDICTOR ON' : 'AI PREDICTOR'}</span>
              </>
            )}
          </button>

          {/* Timeframe buttons */}
          <div className="flex gap-1 bg-dark-800 rounded-xl p-1">
            {TIMEFRAMES.map((tf) => (
              <button
                key={tf.label}
                onClick={() => setActiveTimeframe(tf)}
                className={`px-3 py-1.5 rounded-lg text-xs font-mono font-medium transition-all duration-200 ${
                  activeTimeframe.label === tf.label
                    ? 'bg-accent-green text-dark-900'
                    : 'text-gray-500 hover:text-gray-300'
                }`}
              >
                {tf.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Chart area */}
      <div className="h-64 relative">
        {loading ? (
          <div className="absolute inset-0 flex flex-col items-center justify-center gap-3">
            <div className="w-6 h-6 border-2 border-surface-border border-t-accent-green rounded-full animate-spin" />
            <p className="text-gray-600 text-xs font-mono">Loading chart data...</p>
          </div>
        ) : error ? (
          <div className="absolute inset-0 flex items-center justify-center">
            <p className="text-gray-500 text-sm">{error}</p>
          </div>
        ) : candles.length === 0 ? (
          <div className="absolute inset-0 flex items-center justify-center">
            <p className="text-gray-500 text-sm">No data available for this timeframe</p>
          </div>
        ) : (
          <Line data={chartData} options={options} />
        )}
      </div>
    </div>
  );
};

export default StockChart;
