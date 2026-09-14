#!/usr/bin/env python3
"""
Example: Backtest a momentum strategy on historical data
"""

import pandas as pd
from backtester import BacktestEngine, momentum_strategy, mean_reversion_strategy, breakout_strategy

# Load historical data (example - replace with actual data fetch)
# You would typically fetch this using scanner.api.get_ohlcv_histories()
data = pd.read_csv('historical_data.csv')
data['date'] = pd.to_datetime(data['date'])
data = data.sort_values('date')

print("🔬 Running Backtests...")
print("=" * 60)

# Test different strategies
strategies = {
    'Momentum': momentum_strategy,
    'Mean Reversion': mean_reversion_strategy,
    'Breakout': breakout_strategy
}

results = {}

for name, strategy in strategies.items():
    print(f"\nTesting {name} Strategy...")
    
    engine = BacktestEngine(initial_capital=50000)
    result = engine.run_backtest(data, strategy, ticker="TEST")
    results[name] = result
    
    print(f"  Total Return: {result['total_return_pct']:.2f}%")
    print(f"  Max Drawdown: {result['max_drawdown_pct']:.2f}%")
    print(f"  Win Rate: {result['win_rate_pct']:.2f}%")
    print(f"  Sharpe Ratio: {result['sharpe_ratio']:.2f}")
    print(f"  Total Trades: {result['total_trades']}")
    
    # Save equity curve plot
    engine.plot_equity_curve(result, save_path=f"backtest_{name.lower().replace(' ', '_')}.png")

# Compare strategies
print("\n" + "=" * 60)
print("📊 Strategy Comparison:")
print("-" * 60)

print(f"\n{'Strategy':<20} {'Return':>10} {'Drawdown':>12} {'Win Rate':>10} {'Sharpe':>8}")
print("-" * 60)

for name, result in results.items():
    print(f"{name:<20} {result['total_return_pct']:>9.2f}% {result['max_drawdown_pct']:>11.2f}% {result['win_rate_pct']:>9.2f}% {result['sharpe_ratio']:>8.2f}")

print("\n✓ Backtests complete! Check PNG files for equity curves.")
