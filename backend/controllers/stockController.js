const fetch = require('node-fetch');

const FINNHUB_BASE = 'https://finnhub.io/api/v1';
const getKey = () => process.env.FINNHUB_API_KEY;

// ─────────────────────────────────────────────────────────────
// In-Memory Cache  (prevents 429 rate-limit on Finnhub free tier)
//  - quote   → cached for 60 s  (prices don't change every second)
//  - profile → cached for 1 hr  (company info is static)
//  - search  → cached for 5 min
// ─────────────────────────────────────────────────────────────
const cache = new Map();

const cacheGet = (key) => {
  const entry = cache.get(key);
  if (!entry) return null;
  if (Date.now() > entry.expiresAt) { cache.delete(key); return null; }
  return entry.data;
};

const cacheSet = (key, data, ttlMs) => {
  cache.set(key, { data, expiresAt: Date.now() + ttlMs });
};

// ─────────────────────────────────────────────────────────────
// Queue: serialize Finnhub calls so we never burst the limit
// Finnhub free = 30 req/min → max 1 request every 2 seconds
// ─────────────────────────────────────────────────────────────
let finnhubQueue = Promise.resolve();
const FINNHUB_DELAY_MS = 300; // small delay between queued calls

const finnhubFetch = (path) => {
  // Check cache first
  const cached = cacheGet(`finnhub:${path}`);
  if (cached) return Promise.resolve(cached);

  // Queue the actual fetch
  finnhubQueue = finnhubQueue.then(async () => {
    await new Promise((r) => setTimeout(r, FINNHUB_DELAY_MS));
  });

  return finnhubQueue.then(async () => {
    const url = `${FINNHUB_BASE}${path}&token=${getKey()}`;
    const res = await fetch(url);
    if (res.status === 429) throw new Error('Finnhub API error: 429 (rate limit - please wait a moment)');
    if (!res.ok) throw new Error(`Finnhub API error: ${res.status}`);
    const data = await res.json();
    return data;
  });
};

// Convenience: cached finnhub call
const finnhubCached = async (path, ttlMs = 60_000) => {
  const cached = cacheGet(`finnhub:${path}`);
  if (cached) return cached;
  const data = await finnhubFetch(path);
  cacheSet(`finnhub:${path}`, data, ttlMs);
  return data;
};

// ─────────────────────────────────────────────────────────────
// @desc    Search stocks
// @route   GET /api/stocks/search?q=AAPL
// @access  Private
// ─────────────────────────────────────────────────────────────
const searchStocks = async (req, res) => {
  const { q } = req.query;
  if (!q || q.trim().length < 1) {
    return res.status(400).json({ success: false, message: 'Query parameter q is required.' });
  }

  try {
    // Search results cached for 5 min
    const data = await finnhubCached(`/search?q=${encodeURIComponent(q.trim())}`, 5 * 60_000);
    const results = (data.result || [])
      .filter((item) => item.type === 'Common Stock' && item.symbol && !item.symbol.includes('.'))
      .slice(0, 10)
      .map((item) => ({
        symbol: item.symbol,
        description: item.description,
        type: item.type,
      }));

    res.json({ success: true, results });
  } catch (error) {
    console.error('Stock search error:', error.message);
    res.status(500).json({ success: false, message: 'Failed to search stocks.' });
  }
};

// ─────────────────────────────────────────────────────────────
// @desc    Get stock quote + profile
// @route   GET /api/stocks/quote/:symbol
// @access  Private
// ─────────────────────────────────────────────────────────────
const getStockQuote = async (req, res) => {
  const { symbol } = req.params;
  const sym = symbol.toUpperCase();

  try {
    // Run sequentially (not parallel) to avoid bursting rate limit
    const quote = await finnhubCached(`/quote?symbol=${sym}`, 60_000);           // 60s cache
    const profile = await finnhubCached(`/stock/profile2?symbol=${sym}`, 3_600_000); // 1hr cache

    if (!quote || !quote.c || quote.c === 0) {
      return res.status(404).json({ success: false, message: 'Stock not found or no data available.' });
    }

    res.json({
      success: true,
      data: {
        symbol: sym,
        companyName: profile?.name || sym,
        logo: profile?.logo || '',
        exchange: profile?.exchange || '',
        industry: profile?.finnhubIndustry || '',
        marketCap: profile?.marketCapitalization || 0,
        currentPrice: quote.c,
        openPrice: quote.o,
        highPrice: quote.h,
        lowPrice: quote.l,
        previousClose: quote.pc,
        change: quote.d,
        changePercent: quote.dp,
        timestamp: quote.t,
        currency: profile?.currency || 'USD',
      },
    });
  } catch (error) {
    console.error('Get stock quote error:', error.message);
    if (error.message.includes('429')) {
      return res.status(429).json({ success: false, message: 'Rate limit reached. Please wait a moment and try again.' });
    }
    res.status(500).json({ success: false, message: 'Failed to fetch stock data.' });
  }
};

// ─────────────────────────────────────────────────────────────
// @desc    Get stock candles (historical data via Yahoo Finance)
// @route   GET /api/stocks/candles/:symbol
// @access  Private
// ─────────────────────────────────────────────────────────────
const getStockCandles = async (req, res) => {
  const { symbol } = req.params;
  const { resolution = 'D', from, to } = req.query;
  const sym = symbol.toUpperCase();

  const now = Math.floor(Date.now() / 1000);
  const toTime = to ? parseInt(to) : now;
  const fromTime = from ? parseInt(from) : now - 30 * 24 * 60 * 60;

  // Map resolution to Yahoo Finance interval
  let interval = '1d';
  if (['1', '5', '15', '30', '60'].includes(resolution)) {
    interval = `${resolution}m`;
  } else if (resolution === 'W') {
    interval = '1wk';
  } else if (resolution === 'M') {
    interval = '1mo';
  }

  const cacheKey = `yahoo:${sym}:${interval}:${fromTime}`;
  const cached = cacheGet(cacheKey);
  if (cached) return res.json(cached);

  try {
    const url = `https://query1.finance.yahoo.com/v8/finance/chart/${sym}?period1=${fromTime}&period2=${toTime}&interval=${interval}`;
    const response = await fetch(url, {
      headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' },
    });
    if (!response.ok) throw new Error(`Yahoo API error: ${response.status}`);
    const data = await response.json();

    const result = data.chart?.result?.[0];
    if (!result || !result.timestamp) {
      return res.status(404).json({ success: false, message: 'No historical data available.' });
    }

    const quote = result.indicators.quote[0];
    const candles = [];
    for (let i = 0; i < result.timestamp.length; i++) {
      if (quote.open[i] !== null && quote.close[i] !== null) {
        candles.push({
          time: result.timestamp[i],
          open: parseFloat(quote.open[i]?.toFixed(4)) || 0,
          high: parseFloat(quote.high[i]?.toFixed(4)) || 0,
          low: parseFloat(quote.low[i]?.toFixed(4)) || 0,
          close: parseFloat(quote.close[i]?.toFixed(4)) || 0,
          volume: quote.volume[i] || 0,
        });
      }
    }

    const payload = { success: true, symbol: sym, resolution, candles };
    // Cache candles for 10 min (daily data doesn't change frequently)
    cacheSet(cacheKey, payload, 10 * 60_000);
    res.json(payload);
  } catch (error) {
    console.error('Get candles error:', error.message);
    res.status(500).json({ success: false, message: 'Failed to fetch historical data.' });
  }
};

// ─────────────────────────────────────────────────────────────
// @desc    Get market status
// @route   GET /api/stocks/market-status
// @access  Private
// ─────────────────────────────────────────────────────────────
const getMarketStatus = async (req, res) => {
  try {
    // Market status cached for 5 min
    const data = await finnhubCached('/stock/market-status?exchange=US', 5 * 60_000);
    res.json({ success: true, data });
  } catch (error) {
    console.error('Market status error:', error.message);
    res.status(500).json({ success: false, message: 'Failed to fetch market status.' });
  }
};

// ─────────────────────────────────────────────────────────────
// @desc    Get AI Stock Price Prediction (Polynomial Regression Degree 2)
// @route   GET /api/stocks/predict/:symbol
// @access  Private
// ─────────────────────────────────────────────────────────────
const getStockPrediction = async (req, res) => {
  const { symbol } = req.params;
  const sym = symbol.toUpperCase();

  const now = Math.floor(Date.now() / 1000);
  const fromTime = now - 45 * 24 * 60 * 60; // 45 days ago to ensure we get at least 30 trading days

  const cacheKey = `predict:${sym}`;
  const cached = cacheGet(cacheKey);
  if (cached) return res.json(cached);

  try {
    // Fetch historical daily price candles from Yahoo Finance
    const url = `https://query1.finance.yahoo.com/v8/finance/chart/${sym}?period1=${fromTime}&period2=${now}&interval=1d`;
    const response = await fetch(url, {
      headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' },
    });
    if (!response.ok) throw new Error(`Yahoo API error: ${response.status}`);
    const data = await response.json();

    const result = data.chart?.result?.[0];
    if (!result || !result.timestamp) {
      return res.status(404).json({ success: false, message: 'No historical data available for prediction.' });
    }

    const quote = result.indicators.quote[0];
    const candles = [];
    for (let i = 0; i < result.timestamp.length; i++) {
      if (quote.open[i] !== null && quote.close[i] !== null && quote.close[i] !== undefined) {
        candles.push({
          time: result.timestamp[i],
          close: quote.close[i],
        });
      }
    }

    // Take the last 30 daily data points for training
    const points = candles.slice(-30);
    const N = points.length;

    if (N < 10) {
      return res.status(400).json({
        success: false,
        message: 'Insufficient historical data to train the prediction model. Need at least 10 trading days.',
      });
    }

    // ─────────────────────────────────────────────────────────────
    // Ordinary Least Squares (OLS) Polynomial Regression (Degree 2)
    // Model: y = beta2 * x^2 + beta1 * x + beta0
    // Where x is the time step index [0, 1, ..., N-1]
    // ─────────────────────────────────────────────────────────────
    let Sx = 0;
    let Sx2 = 0;
    let Sx3 = 0;
    let Sx4 = 0;
    let Sy = 0;
    let Sxy = 0;
    let Sx2y = 0;

    for (let i = 0; i < N; i++) {
      const x = i;
      const y = points[i].close;
      const x2 = x * x;
      const x3 = x2 * x;
      const x4 = x2 * x2;

      Sx += x;
      Sx2 += x2;
      Sx3 += x3;
      Sx4 += x4;
      Sy += y;
      Sxy += x * y;
      Sx2y += x2 * y;
    }

    // Vandermonde normal matrix components (A = X^T * X)
    // A = [ [N,   Sx,  Sx2],
    //       [Sx,  Sx2, Sx3],
    //       [Sx2, Sx3, Sx4] ]
    const A00 = N,   A01 = Sx,  A02 = Sx2;
    const A10 = Sx,  A11 = Sx2, A12 = Sx3;
    const A20 = Sx2, A21 = Sx3, A22 = Sx4;

    // Vector B = X^T * y
    // B = [Sy, Sxy, Sx2y]
    const B0 = Sy;
    const B1 = Sxy;
    const B2 = Sx2y;

    // Compute determinant of A using Cramer's rule
    const det = A00 * (A11 * A22 - A12 * A21) -
                A01 * (A10 * A22 - A12 * A20) +
                A02 * (A10 * A21 - A11 * A20);

    let beta0 = 0;
    let beta1 = 0;
    let beta2 = 0;

    if (Math.abs(det) < 1e-6) {
      // Fallback: Linear Regression (Degree 1) if matrix is singular
      const Sxx = Sx2 - (Sx * Sx) / N;
      const SxyCov = Sxy - (Sx * Sy) / N;
      beta1 = Sxx !== 0 ? SxyCov / Sxx : 0;
      beta0 = (Sy - beta1 * Sx) / N;
      beta2 = 0;
    } else {
      // Compute inverse of A (adjugate / det)
      const invDet = 1.0 / det;
      const inv00 = (A11 * A22 - A12 * A21) * invDet;
      const inv01 = (A02 * A21 - A01 * A22) * invDet;
      const inv02 = (A01 * A12 - A02 * A11) * invDet;

      const inv10 = (A12 * A20 - A10 * A22) * invDet;
      const inv11 = (A00 * A22 - A02 * A20) * invDet;
      const inv12 = (A02 * A10 - A00 * A12) * invDet;

      const inv20 = (A10 * A21 - A11 * A20) * invDet;
      const inv21 = (A01 * A20 - A00 * A21) * invDet;
      const inv22 = (A00 * A11 - A01 * A10) * invDet;

      // Solve for beta coefficients (beta = A^-1 * B)
      beta0 = inv00 * B0 + inv01 * B1 + inv02 * B2;
      beta1 = inv10 * B0 + inv11 * B1 + inv12 * B2;
      beta2 = inv20 * B0 + inv21 * B1 + inv22 * B2;
    }

    // ─────────────────────────────────────────────────────────────
    // Model Evaluation: Compute R^2, MAE, and Standard Error
    // ─────────────────────────────────────────────────────────────
    let rss = 0;
    let tss = 0;
    let absoluteErrorsSum = 0;
    const yMean = Sy / N;

    for (let i = 0; i < N; i++) {
      const x = i;
      const y = points[i].close;
      const yHat = beta0 + beta1 * x + beta2 * x * x;
      const e = y - yHat;

      rss += e * e;
      tss += (y - yMean) * (y - yMean);
      absoluteErrorsSum += Math.abs(e);
    }

    const r2 = tss > 0 ? Math.max(0, Math.min(1, 1 - (rss / tss))) : 0;
    const mae = absoluteErrorsSum / N;
    const standardError = N > 3 ? Math.sqrt(rss / (N - 3)) : 1.0;

    // Format the equation string
    const formula = `y = ${beta2.toFixed(4)}x² ${beta1 >= 0 ? '+' : '-'} ${Math.abs(beta1).toFixed(4)}x ${beta0 >= 0 ? '+' : '-'} ${Math.abs(beta0).toFixed(2)}`;

    // ─────────────────────────────────────────────────────────────
    // Forecast Projections: Next 5 Days
    // ─────────────────────────────────────────────────────────────
    const predictions = [];
    const lastTime = points[N - 1].time;
    const lastPrice = points[N - 1].close;

    for (let j = 1; j <= 5; j++) {
      const x = N - 1 + j;
      const predClose = Math.max(0.01, beta0 + beta1 * x + beta2 * x * x);

      // Uncertainty grows as a cone: margin expands by 15% each day
      const margin = 1.96 * standardError * (1 + 0.15 * j);
      const confidenceHigh = predClose + margin;
      const confidenceLow = Math.max(0.01, predClose - margin);

      predictions.push({
        time: lastTime + j * 86400, // add 1 day in seconds
        close: parseFloat(predClose.toFixed(4)),
        confidenceHigh: parseFloat(confidenceHigh.toFixed(4)),
        confidenceLow: parseFloat(confidenceLow.toFixed(4)),
      });
    }

    // Determine trend based on percentage change from last historical price to the 5th day projection
    const finalPred = predictions[4].close;
    const pctChange = ((finalPred - lastPrice) / lastPrice) * 100;
    let trend = 'Neutral';
    if (pctChange > 0.5) {
      trend = 'Bullish';
    } else if (pctChange < -0.5) {
      trend = 'Bearish';
    }

    const payload = {
      success: true,
      symbol: sym,
      formula,
      metrics: {
        r2: parseFloat(r2.toFixed(4)),
        mae: parseFloat(mae.toFixed(4)),
        trend,
      },
      predictions,
    };

    // Cache predictions for 15 minutes
    cacheSet(cacheKey, payload, 15 * 60_000);
    res.json(payload);
  } catch (error) {
    console.error('Prediction error:', error.message);
    res.status(500).json({ success: false, message: 'Failed to generate stock prediction.' });
  }
};

module.exports = { searchStocks, getStockQuote, getStockCandles, getMarketStatus, getStockPrediction };
