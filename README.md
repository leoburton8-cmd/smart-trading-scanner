# 🚀 Smart Trading Scanner

**Automated trading opportunity scanner** that leverages real-time market data, analyst research, and AI-powered analysis to generate actionable trade setups and trading journal entries.

[![GitHub stars](https://img.shields.io/github/stars/leoburton8-cmd/smart-trading-scanner?style=social)](https://github.com/leoburton8-cmd/smart-trading-scanner/stargazers)
[![License](https://img.shields.io/github/license/leoburton8-cmd/smart-trading-scanner)](https://github.com/leoburton8-cmd/smart-trading-scanner/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## ✨ Features

- **🔍 Real-time Market Scanning**: Automatically scans top gainers and losers
- **📊 Analyst Research Integration**: Pulls consensus ratings and price targets
- **🎯 Opportunity Scoring**: AI-calculated 0-100 score based on momentum, sentiment, and volume
- **📈 Trade Setup Generation**: Automatic entry zones, stop losses, and take profit levels
- **⚠️ Risk Assessment**: Identifies key risk factors and provides recommendations
- **📝 Trading Journal**: Auto-generates structured markdown journal entries
- **📥 CSV Export**: Export scan results for further analysis
- **🖥️ Web Dashboard**: Interactive Streamlit interface for visual monitoring
- **🔬 Backtesting Module**: Test strategies on historical data before risking capital

## 🎯 Why This Is Massively Beneficial

1. **Saves Hours of Research**: Automates the entire pre-market research process
2. **Data-Driven Decisions**: Combines multiple data sources (price, volume, analyst sentiment)
3. **Consistent Analysis**: Every opportunity evaluated with the same rigorous framework
4. **Built-in Risk Management**: Stop losses and position sizing recommendations
5. **Journal Integration**: Automatic documentation for continuous improvement
6. **Backtesting**: Validate strategies before using real money
7. **Fully Customizable**: Modify scoring, filters, and strategies to match your style

## 🚀 Quick Start (5 Minutes)

### Option 1: Command Line Scanner

```bash
# 1. Clone
git clone https://github.com/leoburton8-cmd/smart-trading-scanner.git
cd smart-trading-scanner

# 2. Install
pip install -r requirements.txt

# 3. Configure (edit scanner.py line ~260)
# API_KEY = "YOUR_PERPLEXITY_API_KEY_HERE"

# 4. Run
python scanner.py
```

### Option 2: Web Dashboard (Recommended)

```bash
# 1. Install dashboard dependencies
pip install -r streamlit_requirements.txt

# 2. Launch dashboard
streamlit run dashboard.py
```

This opens a web interface at `http://localhost:8501` with:
- Real-time opportunity cards
- Interactive filters and settings
- One-click journal generation
- Visual charts and metrics

## 📊 Example Output

```
🔍 Smart Trading Scanner
==================================================

Scanning market gainers...

✓ Found 10 opportunities

📊 Top Opportunities:
--------------------------------------------------
1. NVDA - Score: 87.5
   Price: $485.20 | Change: +8.3%
   Analyst: Strong Buy
   Entry: $475.50 - $494.90
   Stop: $461.00 | Target: $509.46

2. TSLA - Score: 82.1
   Price: $242.50 | Change: +6.7%
   Analyst: Buy
   Entry: $237.65 - $247.35
   Stop: $230.38 | Target: $254.63

✓ Exported 10 opportunities to trading_opportunities.csv
📝 Journal generated for NVDA
```

## 📁 Project Structure

```
smart-trading-scanner/
├── scanner.py              # Main scanner engine
├── backtester.py           # Strategy backtesting module
├── dashboard.py            # Streamlit web dashboard
├── requirements.txt        # Core dependencies
├── streamlit_requirements.txt  # Dashboard dependencies
├── README.md              # This file
├── SETUP_GUIDE.md         # Detailed setup instructions
├── API_REFERENCE.md       # API integration docs
├── config.example.json    # Configuration template
├── examples/
│   ├── scan_and_journal.py    # Example usage
│   └── backtest_example.py    # Backtesting demo
└── journals/              # Auto-generated trading journals
```

## 🛠️ Usage Examples

### Scan Only Gainers

```python
from scanner import TradingScanner

scanner = TradingScanner(API_KEY)
opportunities = scanner.scan_opportunities(scan_type="gainers", limit=15)
```

### Scan Both Gainers and Losers

```python
opportunities = scanner.scan_opportunities(scan_type="both", limit=20)
```

### Filter by Minimum Volume

```python
opportunities = scanner.scan_opportunities(
    scan_type="gainers", 
    min_volume=5000000  # Only stocks with 5M+ avg volume
)
```

### Generate Journal for Specific Ticker

```python
scanner.save_journal("AAPL")
# Creates: journals/AAPL_20260914_1430.md
```

### Backtest a Strategy

```python
from backtester import BacktestEngine, momentum_strategy
import pandas as pd

# Load historical data
data = pd.read_csv('AAPL_historical.csv')
data['date'] = pd.to_datetime(data['date'])

# Run backtest
engine = BacktestEngine(initial_capital=50000)
results = engine.run_backtest(data, momentum_strategy, ticker="AAPL")

print(f"Total Return: {results['total_return_pct']}%")
print(f"Max Drawdown: {results['max_drawdown_pct']}%")
print(f"Sharpe Ratio: {results['sharpe_ratio']}")

# Plot equity curve
engine.plot_equity_curve(results)
```

## 📥 Output Files

- `trading_opportunities.csv` - All scanned opportunities with key metrics
- `journals/TICKER_YYYYMMDD_HHMM.md` - Detailed trading journal entries
- `backtest_*.png` - Equity curve visualizations from backtesting

## 🎯 Opportunity Score Calculation

The scanner calculates a 0-100 opportunity score based on:

| Factor | Weight | Description |
|--------|--------|-------------|
| Price Momentum | Up to +20 | Daily percentage change |
| Analyst Sentiment | Up to +15 | Strong Buy/Buy ratings |
| Volume Surge | +10 | Volume > 2x average |
| Risk/Reward | Up to +5 | Favorable setups |

**Score Interpretation:**
- 🟢 **80-100**: High conviction opportunities
- 🟡 **60-79**: Moderate opportunities
- 🔴 **<60**: Lower quality setups

## 🖥️ Web Dashboard Features

The Streamlit dashboard provides:

- **Interactive scanning** with adjustable parameters
- **Visual opportunity cards** with color-coded scores
- **Expandable sections** for trade setups and risk assessment
- **One-click actions** (journal generation, CSV export)
- **Real-time metrics** (avg score, gainers vs losers)
- **Responsive design** for desktop and mobile

**Launch:**
```bash
streamlit run dashboard.py
```

## 🔬 Backtesting Module

Test strategies before risking real capital:

**Built-in Strategies:**
- `momentum_strategy` - Trend-following with MA and RSI
- `mean_reversion_strategy` - Buy dips below moving average
- `breakout_strategy` - Trade breakouts of 20-day highs

**Custom Strategies:**
```python
def my_strategy(data, current_idx):
    # Your logic here
    if condition:
        return 'buy'
    elif other_condition:
        return 'sell'
    else:
        return 'hold'

results = engine.run_backtest(data, my_strategy, ticker="TEST")
```

## ⚠️ Disclaimer

**This tool is for educational and research purposes only. It does not constitute financial advice.**

Always:
- Do your own research (DYOR)
- Use proper risk management
- Never risk more than you can afford to lose
- Consult with a licensed financial advisor
- Understand that past performance ≠ future results

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit (`git commit -m 'Add amazing feature'`)
5. Push (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📝 License

MIT License - feel free to use and modify for personal or commercial projects.

## 🔗 Connect

- **GitHub:** [@leoburton8-cmd](https://github.com/leoburton8-cmd)
- **Issues:** [Report bugs or request features](https://github.com/leoburton8-cmd/smart-trading-scanner/issues)
- **Discussions:** [Share ideas and ask questions](https://github.com/leoburton8-cmd/smart-trading-scanner/discussions)

## 📚 Additional Resources

- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Detailed installation and configuration
- [API_REFERENCE.md](API_REFERENCE.md) - Complete API documentation
- [Examples](examples/) - Working code samples

---

**Built with ❤️ for traders** | Last updated: September 2026

**Star ⭐ this repo if you find it useful!**
