# 🔌 API Reference

## Finance API Integration

This scanner uses Perplexity's Finance Data API for real-time market data. Here's how to make direct API calls:

### Base Configuration

```python
import requests

API_KEY = "YOUR_PERPLEXITY_API_KEY"
BASE_URL = "https://api.perplexity.ai"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
```

## Available Endpoints

### 1. Market Gainers

Fetch top gaining stocks today:

```python
def get_market_gainers(limit=10, country="US"):
    url = f"{BASE_URL}/finance/market/gainers"
    params = {"limit": limit, "country": country}
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Usage
gainers = get_market_gainers(limit=15)
print(f"Top gainer: {gainers[0]['ticker']} +{gainers[0]['changesPercentage']}%")
```

**Response fields:**
- `ticker`: Stock symbol
- `price`: Current price
- `changesPercentage`: Daily change %
- `volume`: Trading volume
- `marketCap`: Market capitalization

### 2. Market Losers

Fetch top losing stocks today:

```python
def get_market_losers(limit=10, country="US"):
    url = f"{BASE_URL}/finance/market/losers"
    params = {"limit": limit, "country": country}
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()
```

### 3. Real-Time Quotes

Get current quote for specific tickers:

```python
def get_quotes(tickers: list):
    url = f"{BASE_URL}/finance/quotes"
    payload = {
        "ticker_symbols": tickers,
        "fields": ["price", "changesPercentage", "volume", "marketCap"]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Usage
quotes = get_quotes(["AAPL", "NVDA", "TSLA"])
for quote in quotes:
    print(f"{quote['ticker']}: ${quote['price']} ({quote['changesPercentage']}%)")
```

### 4. Analyst Research

Get analyst ratings and price targets:

```python
def get_analyst_research(ticker: str):
    url = f"{BASE_URL}/finance/analyst-research"
    payload = {"ticker_symbols": [ticker]}
    
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    
    return {
        'consensus_rating': data[0]['consensus_rating'],
        'average_price_target': data[0]['price_target_average'],
        'high_price_target': data[0]['price_target_high'],
        'low_price_target': data[0]['price_target_low'],
        'num_analysts': data[0]['ratings_count']
    }

# Usage
research = get_analyst_research("AAPL")
print(f"Consensus: {research['consensus_rating']}")
print(f"Price Target: ${research['average_price_target']}")
```

### 5. Company Profile

Get company fundamentals:

```python
def get_company_profile(ticker: str):
    url = f"{BASE_URL}/finance/company-profile"
    payload = {
        "ticker_symbols": [ticker],
        "query": f"Company profile for {ticker}"
    }
    
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    
    return {
        'sector': data[0]['sector'],
        'industry': data[0]['industry'],
        'description': data[0]['description'],
        'ceo': data[0]['ceo'],
        'employees': data[0]['employees'],
        'website': data[0]['website']
    }
```

### 6. Historical OHLCV Data

Get price history for backtesting:

```python
def get_historical_data(ticker: str, start_date: str, end_date: str, interval="1day"):
    url = f"{BASE_URL}/finance/ohlcv-histories"
    payload = {
        "ticker_symbols": [ticker],
        "start_date_yyyy_mm_dd": start_date,
        "end_date_yyyy_mm_dd": end_date,
        "time_interval": interval,
        "fields": ["open", "high", "low", "close", "volume"]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Usage
# Get 1 year of daily data
history = get_historical_data("AAPL", "2025-01-01", "2026-01-01")
```

### 7. Earnings Schedule

Get upcoming earnings dates:

```python
def get_earnings_schedule(ticker: str = None, start_date: str = None, end_date: str = None):
    url = f"{BASE_URL}/finance/earnings-schedule"
    payload = {}
    
    if ticker:
        payload["ticker_symbols"] = [ticker]
    if start_date:
        payload["start_date"] = start_date
    if end_date:
        payload["end_date"] = end_date
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Usage
# Get all earnings this week
earnings = get_earnings_schedule(start_date="2026-09-14", end_date="2026-09-20")
```

### 8. Stock Screener

Run custom SQL queries on stock data:

```python
def run_stock_screener(query: str, sql: str, max_rows=100):
    url = f"{BASE_URL}/finance/stock-screener"
    payload = {
        "query": query,
        "sql": sql,
        "max_rows": max_rows
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Example: Find stocks with P/E < 15 and volume > 1M
query = "Undervalued stocks with good liquidity"
sql = """
SELECT ticker, price, pe, volume 
FROM stocks 
WHERE pe < 15 
  AND volume > 1000000 
  AND market_cap > 1000000000
ORDER BY pe ASC
"""

results = run_stock_screener(query, sql)
```

## Rate Limits

- **Free tier:** 100 requests/hour
- **Pro tier:** 1000 requests/hour
- **Enterprise:** Custom limits

**Best practices:**
- Cache results when possible
- Batch multiple tickers in single requests
- Use webhooks for real-time updates (if available)

## Error Handling

```python
def safe_api_call(func, *args, **kwargs):
    try:
        result = func(*args, **kwargs)
        return result
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            print("Rate limit exceeded - waiting 60 seconds...")
            time.sleep(60)
            return safe_api_call(func, *args, **kwargs)
        elif e.response.status_code == 401:
            print("Invalid API key - check your credentials")
            return None
        else:
            print(f"API error: {e}")
            return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

# Usage
quotes = safe_api_call(get_quotes, ["AAPL", "NVDA"])
```

## Example: Complete Data Fetch

```python
def fetch_complete_analysis(ticker: str):
    """Fetch all available data for a ticker"""
    
    # Real-time quote
    quote = get_quotes([ticker])[0]
    
    # Analyst research
    analyst = get_analyst_research(ticker)
    
    # Company profile
    profile = get_company_profile(ticker)
    
    # Historical data (1 year)
    from datetime import datetime, timedelta
    end = datetime.now()
    start = end - timedelta(days=365)
    history = get_historical_data(
        ticker, 
        start.strftime("%Y-%m-%d"), 
        end.strftime("%Y-%m-%d")
    )
    
    return {
        'quote': quote,
        'analyst': analyst,
        'profile': profile,
        'history': history
    }

# Usage
aapl_data = fetch_complete_analysis("AAPL")
print(json.dumps(aapl_data, indent=2))
```

## Webhooks & Real-Time Updates

For real-time trading, consider:

1. **Polling:** Run scanner every 5-15 minutes
2. **Alert services:** Set up price alerts via your broker
3. **WebSocket:** Check if your data provider offers WebSocket streams

## Testing

Test API calls before deploying:

```python
# Test script
test_tickers = ["AAPL", "NVDA", "TSLA"]

print("Testing API connection...")
quotes = get_quotes(test_tickers)
print(f"✓ Successfully fetched {len(quotes)} quotes")

print("Testing analyst data...")
research = get_analyst_research("AAPL")
print(f"✓ Consensus: {research['consensus_rating']}")

print("All tests passed!")
```

---

**For full API documentation, visit:** [Perplexity Finance API Docs](https://docs.perplexity.ai/finance)
