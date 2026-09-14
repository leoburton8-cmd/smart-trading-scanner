#!/usr/bin/env python3
"""
Backtesting Module for Smart Trading Scanner
=============================================
Test trading strategies on historical data before risking real capital.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class BacktestEngine:
    """Simple backtesting engine for strategy validation"""
    
    def __init__(self, initial_capital: float = 100000.0):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.positions = {}
        self.trades = []
        self.equity_curve = []
    
    def run_backtest(self, 
                    data: pd.DataFrame, 
                    strategy_func,
                    ticker: str = "BACKTEST") -> Dict:
        """
        Run backtest on historical data
        
        Args:
            data: DataFrame with OHLCV data (columns: date, open, high, low, close, volume)
            strategy_func: Function that returns 'buy', 'sell', or 'hold' signals
            ticker: Stock ticker symbol
        
        Returns:
            Dictionary with backtest results
        """
        
        self.capital = self.initial_capital
        self.positions = {}
        self.trades = []
        self.equity_curve = []
        
        position = 0  # Number of shares held
        
        for idx, row in data.iterrows():
            date = row['date']
            price = row['close']
            
            # Get signal from strategy
            signal = strategy_func(data, idx)
            
            # Execute trades
            if signal == 'buy' and self.capital > 0:
                # Buy as many shares as possible
                shares_to_buy = int(self.capital * 0.95 / price)  # Use 95% of capital
                if shares_to_buy > 0:
                    cost = shares_to_buy * price
                    self.capital -= cost
                    position += shares_to_buy
                    
                    self.trades.append({
                        'date': date,
                        'type': 'BUY',
                        'price': price,
                        'shares': shares_to_buy,
                        'value': cost
                    })
            
            elif signal == 'sell' and position > 0:
                # Sell all shares
                proceeds = position * price
                self.capital += proceeds
                
                self.trades.append({
                    'date': date,
                    'type': 'SELL',
                    'price': price,
                    'shares': position,
                    'value': proceeds
                })
                
                position = 0
            
            # Record equity
            total_equity = self.capital + (position * price)
            self.equity_curve.append({
                'date': date,
                'equity': total_equity
            })
        
        # Calculate metrics
        return self._calculate_metrics(ticker)
    
    def _calculate_metrics(self, ticker: str) -> Dict:
        """Calculate performance metrics"""
        
        if not self.equity_curve:
            return {'error': 'No trades executed'}
        
        equity_df = pd.DataFrame(self.equity_curve)
        
        # Total return
        final_equity = equity_df['equity'].iloc[-1]
        total_return = ((final_equity - self.initial_capital) / self.initial_capital) * 100
        
        # Max drawdown
        equity_df['peak'] = equity_df['equity'].cummax()
        equity_df['drawdown'] = (equity_df['equity'] - equity_df['peak']) / equity_df['peak'] * 100
        max_drawdown = equity_df['drawdown'].min()
        
        # Win rate
        if len(self.trades) >= 2:
            buy_trades = [t for t in self.trades if t['type'] == 'BUY']
            sell_trades = [t for t in self.trades if t['type'] == 'SELL']
            
            wins = 0
            for i in range(min(len(buy_trades), len(sell_trades))):
                if sell_trades[i]['price'] > buy_trades[i]['price']:
                    wins += 1
            
            win_rate = (wins / min(len(buy_trades), len(sell_trades))) * 100 if min(len(buy_trades), len(sell_trades)) > 0 else 0
        else:
            win_rate = 0
        
        # Sharpe ratio (simplified)
        returns = equity_df['equity'].pct_change().dropna()
        sharpe = (returns.mean() / returns.std()) * np.sqrt(252) if len(returns) > 1 and returns.std() > 0 else 0
        
        return {
            'ticker': ticker,
            'initial_capital': self.initial_capital,
            'final_equity': final_equity,
            'total_return_pct': round(total_return, 2),
            'max_drawdown_pct': round(max_drawdown, 2),
            'win_rate_pct': round(win_rate, 2),
            'sharpe_ratio': round(sharpe, 2),
            'total_trades': len([t for t in self.trades if t['type'] == 'SELL']),
            'trades': self.trades,
            'equity_curve': self.equity_curve
        }
    
    def plot_equity_curve(self, results: Dict, save_path: str = "backtest_results.png"):
        """Plot equity curve and drawdowns"""
        
        if 'equity_curve' not in results or not results['equity_curve']:
            print("No equity curve data to plot")
            return
        
        equity_df = pd.DataFrame(results['equity_curve'])
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
        
        # Plot equity curve
        ax1.plot(equity_df['date'], equity_df['equity'], 'b-', linewidth=2, label='Portfolio Value')
        ax1.axhline(y=self.initial_capital, color='gray', linestyle='--', alpha=0.5, label='Initial Capital')
        ax1.set_ylabel('Portfolio Value ($)')
        ax1.set_title(f"Backtest Results - {results.get('ticker', 'STRATEGY')}")
        ax1.legend(loc='upper left')
        ax1.grid(True, alpha=0.3)
        
        # Format y-axis as currency
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        # Plot drawdowns
        equity_df['peak'] = equity_df['equity'].cummax()
        equity_df['drawdown'] = (equity_df['equity'] - equity_df['peak']) / equity_df['peak'] * 100
        
        ax2.fill_between(equity_df['date'], equity_df['drawdown'], 0, color='red', alpha=0.3)
        ax2.plot(equity_df['date'], equity_df['drawdown'], 'r-', linewidth=1)
        ax2.set_ylabel('Drawdown (%)')
        ax2.set_xlabel('Date')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Equity curve saved to {save_path}")


# Example Strategies
def momentum_strategy(data: pd.DataFrame, current_idx: int) -> str:
    """
    Simple momentum strategy:
    - Buy when price > 20-day MA and RSI < 70
    - Sell when price < 20-day MA or RSI > 70
    """
    
    if current_idx < 20:
        return 'hold'
    
    current_data = data.iloc[:current_idx + 1]
    
    # Calculate 20-day moving average
    ma_20 = current_data['close'].rolling(window=20).mean().iloc[-1]
    current_price = current_data['close'].iloc[-1]
    
    # Calculate RSI (14-day)
    delta = current_data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean().iloc[-1]
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean().iloc[-1]
    rs = gain / loss if loss != 0 else 0
    rsi = 100 - (100 / (1 + rs))
    
    # Generate signals
    if current_price > ma_20 and rsi < 70:
        return 'buy'
    elif current_price < ma_20 or rsi > 70:
        return 'sell'
    else:
        return 'hold'


def mean_reversion_strategy(data: pd.DataFrame, current_idx: int) -> str:
    """
    Mean reversion strategy:
    - Buy when price drops 5% below 20-day MA
    - Sell when price returns to MA or rises 3%
    """
    
    if current_idx < 20:
        return 'hold'
    
    current_data = data.iloc[:current_idx + 1]
    ma_20 = current_data['close'].rolling(window=20).mean().iloc[-1]
    current_price = current_data['close'].iloc[-1]
    
    # Buy signal: price 5% below MA
    if current_price < ma_20 * 0.95:
        return 'buy'
    # Sell signal: price at or above MA
    elif current_price >= ma_20:
        return 'sell'
    else:
        return 'hold'


def breakout_strategy(data: pd.DataFrame, current_idx: int) -> str:
    """
    Breakout strategy:
    - Buy when price breaks above 20-day high
    - Sell when price drops below 10-day low
    """
    
    if current_idx < 20:
        return 'hold'
    
    current_data = data.iloc[:current_idx + 1]
    current_price = current_data['close'].iloc[-1]
    
    # 20-day high
    high_20 = current_data['high'].rolling(window=20).max().iloc[-1]
    
    # 10-day low
    low_10 = current_data['low'].rolling(window=10).min().iloc[-1]
    
    # Buy on breakout above 20-day high
    if current_price > high_20:
        return 'buy'
    # Sell on breakdown below 10-day low
    elif current_price < low_10:
        return 'sell'
    else:
        return 'hold'


def main():
    """Example backtest"""
    
    print("🔬 Backtesting Module")
    print("=" * 50)
    print("\nThis module allows you to test trading strategies on historical data.")
    print("\nAvailable strategies:")
    print("  - momentum_strategy: Trend-following with MA and RSI")
    print("  - mean_reversion_strategy: Buy dips below moving average")
    print("  - breakout_strategy: Trade breakouts of 20-day highs")
    print("\nUsage example:")
    print("""
    from backtester import BacktestEngine, momentum_strategy
    import pandas as pd
    
    # Load your historical data
    data = pd.read_csv('AAPL_historical.csv')
    data['date'] = pd.to_datetime(data['date'])
    
    # Run backtest
    engine = BacktestEngine(initial_capital=50000)
    results = engine.run_backtest(data, momentum_strategy, ticker="AAPL")
    
    # Print results
    print(f"Total Return: {results['total_return_pct']}%")
    print(f"Max Drawdown: {results['max_drawdown_pct']}%")
    print(f"Win Rate: {results['win_rate_pct']}%")
    print(f"Sharpe Ratio: {results['sharpe_ratio']}")
    
    # Plot equity curve
    engine.plot_equity_curve(results)
    """)


if __name__ == "__main__":
    main()
