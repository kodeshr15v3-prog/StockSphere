const express = require('express');
const {
  searchStocks,
  getStockQuote,
  getStockCandles,
  getMarketStatus,
  getStockPrediction,
  getStockThesis,
} = require('../controllers/stockController');
const { protect } = require('../middleware/auth');

const router = express.Router();

router.use(protect);

router.get('/search', searchStocks);
router.get('/market-status', getMarketStatus);
router.get('/quote/:symbol', getStockQuote);
router.get('/candles/:symbol', getStockCandles);
router.get('/predict/:symbol', getStockPrediction);
router.get('/thesis/:symbol', getStockThesis);

module.exports = router;
