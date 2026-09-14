# 📚 Complete Setup Guide

## Step 1: Get Your Perplexity API Key

1. Go to [Perplexity API](https://www.perplexity.ai/settings/api)
2. Sign in or create an account
3. Generate a new API key
4. Copy and save it securely

## Step 2: Clone the Repository

```bash
git clone https://github.com/leoburton8-cmd/smart-trading-scanner.git
cd smart-trading-scanner
```

## Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Requirements:**
- Python 3.8 or higher
- pip (Python package manager)

## Step 4: Configure API Key

### Option A: Edit scanner.py directly

Open `scanner.py` and find this line (around line 260):

```python
API_KEY = "YOUR_PERPLEXITY_API_KEY_HERE"
```

Replace with your actual key:

```python
API_KEY = "pplx-xxxxxxxxxxxxxxxxxxxxxxxx"
```

### Option B: Use environment variable (recommended)

```bash
# On Mac/Linux
export PERPLEXITY_API_KEY="pplx-xxxxxxxxxxxxxxxxxxxxxxxx"

# On Windows (Command Prompt)
set PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxxxxxxxxxxxxx

# On Windows (PowerShell)
$env:PERPLEXITY_API_KEY="pplx-xxxxxxxxxxxxxxxxxxxxxxxx"
```

Then modify scanner.py to use:

```python
import os
API_KEY = os.getenv("PERPLEXITY_API_KEY", "YOUR_PERPLEXITY_API_KEY_HERE")
```

## Step 5: Test the Installation

Run a simple test:

```bash
python scanner.py
```

**Expected output:**
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

✓ Exported 10 opportunities to trading_opportunities.csv
📝 Journal generated for NVDA
```

## Step 6: Customize Your Scanner

### Adjust Scan Parameters

Edit the `main()` function in `scanner.py`:

```python
# Scan only top 5 gainers with minimum 5M volume
opportunities = scanner.scan_opportunities(
    scan_type="gainers", 
    limit=5,
    min_volume=5000000
)
```

### Change Risk Management Settings

Edit `config.example.json` (rename to `config.json`):

```json
{
  "risk_management": {
    "max_position_size_pct": 1,  // Risk only 1% per trade
    "default_stop_loss_pct": 3,   // Tighter 3% stops
    "default_take_profit_pct": 6  // 6% profit targets
  }
}
```

## Step 7: Set Up Automated Scans (Optional)

### Using Cron (Mac/Linux)

Edit your crontab:

```bash
crontab -e
```

Add this line to scan every weekday at 9:30 AM (market open):

```bash
30 9 * * 1-5 cd /path/to/smart-trading-scanner && python scanner.py
```

### Using Task Scheduler (Windows)

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (daily at market open)
4. Action: Start a program
   - Program: `python.exe`
   - Arguments: `scanner.py`
   - Start in: `C:\path\to\smart-trading-scanner`

## Step 8: Integrate with Your Trading Workflow

### Morning Routine

1. Run scanner before market open
2. Review top 5 opportunities
3. Check generated journal entries
4. Add your analysis and notes
5. Set alerts for entry zones

### During Trading Hours

1. Monitor stocks in your entry zones
2. Execute trades with predefined risk management
3. Update journal with entry price and reasoning

### End of Day

1. Review all trades
2. Update journal with exit prices
3. Export daily results to CSV
4. Analyze win rate and adjust strategy

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'requests'"

**Solution:**
```bash
pip install -r requirements.txt
```

### Error: "Invalid API key"

**Solution:**
- Check your API key is correct
- Ensure no extra spaces or quotes
- Verify API key hasn't expired

### Error: "No opportunities found"

**Solution:**
- Market might be closed (weekends/holidays)
- Volume filter too high - lower `min_volume` parameter
- API rate limit reached - wait a few minutes

### CSV file not created

**Solution:**
- Check you have write permissions in the directory
- Ensure no other program has the file open
- Try specifying full path: `scanner.export_to_csv("/full/path/file.csv")`

## Next Steps

1. **Backtest strategies** - See `backtester.py` for testing on historical data
2. **Customize scoring** - Modify `_calculate_opportunity_score()` in scanner.py
3. **Add new features** - Pull requests welcome!
4. **Join the community** - Share your improvements on GitHub

## Support

- **Issues:** [GitHub Issues](https://github.com/leoburton8-cmd/smart-trading-scanner/issues)
- **Discussions:** [GitHub Discussions](https://github.com/leoburton8-cmd/smart-trading-scanner/discussions)
- **Email:** Check README.md for contact info

---

**Happy Trading! 📈**
