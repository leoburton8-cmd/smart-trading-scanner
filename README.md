# 🚀 Smart Trading Scanner

Automated trading opportunity scanner that leverages real-time market data, analyst research, and AI-powered analysis to generate actionable trade setups and trading journal entries.

## ✨ Features

- **Real-time Market Scanning**: Automatically scans top gainers and losers
- **Analyst Research Integration**: Pulls consensus ratings and price targets
- **Opportunity Scoring**: AI-calculated 0-100 score based on momentum, sentiment, and volume
- **Trade Setup Generation**: Automatic entry zones, stop losses, and take profit levels
- **Risk Assessment**: Identifies key risk factors and provides recommendations
- **Trading Journal**: Auto-generates structured markdown journal entries
- **CSV Export**: Export scan results for further analysis

## 📋 Requirements

- Python 3.8+
- Perplexity API key (for finance data connector)
- Required packages in `requirements.txt`

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/leoburton8-cmd/smart-trading-scanner.git
cd smart-trading-scanner
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

Edit `scanner.py` and replace:
```python
API_KEY = "YOUR_PERPLEXITY_API_KEY_HERE"
```

### 4. Run the Scanner

```bash
python scanner.py
```

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

2. TSLA - Score: 82.1
   Price: $242.50 | Change: +6.7%
   Analyst: Buy

3. AMD - Score: 78.9
   Price: $165.30 | Change: +5.2%
   Analyst: Buy

✓ Exported 10 opportunities to trading_opportunities.csv
📝 Journal generated for NVDA
```

## 🛠️ Usage Examples

### Scan Only Gainers
```python
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
```

## 📁 Output Files

- `trading_opportunities.csv` - All scanned opportunities with key metrics
- `journals/TICKER_YYYYMMDD_HHMM.md` - Detailed trading journal entries

## 🎯 Opportunity Score Calculation

The scanner calculates a 0-100 opportunity score based on:

| Factor | Weight | Description |
|--------|--------|-------------|
| Price Momentum | Up to +20 | Daily percentage change |
| Analyst Sentiment | Up to +15 | Strong Buy/Buy ratings |
| Volume Surge | +10 | Volume > 2x average |
| Risk/Reward | Up to +5 | Favorable setups |

## ⚠️ Disclaimer

This tool is for educational and research purposes only. It does not constitute financial advice. Always:

- Do your own research (DYOR)
- Use proper risk management
- Never risk more than you can afford to lose
- Consult with a licensed financial advisor

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - feel free to use and modify

## 🔗 Connect

- GitHub: [@leoburton8-cmd](https://github.com/leoburton8-cmd)
- Report issues on the [Issues page](https://github.com/leoburton8-cmd/smart-trading-scanner/issues)

---

**Built with ❤️ for traders** | Last updated: September 2026
