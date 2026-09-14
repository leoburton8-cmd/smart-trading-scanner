#!/usr/bin/env python3
"""
Smart Trading Opportunity Scanner
===================================
Automated tool that scans market gainers/losers, pulls analyst research,
and generates structured trading journal entries.

Author: leoburton8-cmd
Repository: https://github.com/leoburton8-cmd/smart-trading-scanner
"""

import requests
import json
from datetime import datetime
from typing import List, Dict, Optional
import csv


class FinanceAPI:
    """Wrapper for Perplexity Finance API calls"""
    
    BASE_URL = "https://api.perplexity.ai"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def get_market_gainers(self, limit: int = 10, country: str = "US") -> List[Dict]:
        """Fetch top market gainers"""
        # Implementation would call Perplexity finance API
        # For now, returns mock structure
        pass
    
    def get_market_losers(self, limit: int = 10, country: str = "US") -> List[Dict]:
        """Fetch top market losers"""
        pass
    
    def get_analyst_research(self, ticker: str) -> Dict:
        """Get analyst price targets and ratings"""
        pass
    
    def get_company_profile(self, ticker: str) -> Dict:
        """Get company fundamentals"""
        pass


class TradingScanner:
    """Main scanner class that orchestrates market analysis"""
    
    def __init__(self, api_key: str):
        self.api = FinanceAPI(api_key)
        self.scan_results = []
    
    def scan_opportunities(self, 
                          scan_type: str = "gainers", 
                          limit: int = 10,
                          min_volume: int = 1000000) -> List[Dict]:
        """
        Scan for trading opportunities
        
        Args:
            scan_type: 'gainers', 'losers', or 'both'
            limit: Number of stocks to analyze
            min_volume: Minimum average volume filter
        
        Returns:
            List of opportunity dictionaries with full analysis
        """
        opportunities = []
        
        if scan_type in ["gainers", "both"]:
            gainers = self.api.get_market_gainers(limit=limit)
            for stock in gainers:
                if stock.get('volume', 0) >= min_volume:
                    opp = self._analyze_stock(stock['ticker'])
                    opp['scan_type'] = 'gainer'
                    opportunities.append(opp)
        
        if scan_type in ["losers", "both"]:
            losers = self.api.get_market_losers(limit=limit)
            for stock in losers:
                if stock.get('volume', 0) >= min_volume:
                    opp = self._analyze_stock(stock['ticker'])
                    opp['scan_type'] = 'loser'
                    opportunities.append(opp)
        
        self.scan_results = opportunities
        return opportunities
    
    def _analyze_stock(self, ticker: str) -> Dict:
        """Perform deep analysis on a single stock"""
        
        # Get real-time quote
        quote = self._fetch_quote(ticker)
        
        # Get analyst research
        analyst_data = self.api.get_analyst_research(ticker)
        
        # Get company profile
        profile = self.api.get_company_profile(ticker)
        
        # Calculate opportunity score
        score = self._calculate_opportunity_score(quote, analyst_data)
        
        return {
            'ticker': ticker,
            'timestamp': datetime.now().isoformat(),
            'quote': quote,
            'analyst_ratings': analyst_data,
            'company_profile': profile,
            'opportunity_score': score,
            'trade_setup': self._generate_trade_setup(quote, analyst_data),
            'risk_assessment': self._assess_risk(quote, profile)
        }
    
    def _fetch_quote(self, ticker: str) -> Dict:
        """Fetch real-time quote data"""
        # Would call finance_quotes API
        return {'ticker': ticker}
    
    def _calculate_opportunity_score(self, quote: Dict, analyst: Dict) -> float:
        """
        Calculate 0-100 opportunity score based on:
        - Price momentum
        - Analyst sentiment
        - Volume surge
        - Risk/reward ratio
        """
        score = 50.0  # Base score
        
        # Momentum factor
        if 'changesPercentage' in quote:
            momentum = quote['changesPercentage']
            score += min(momentum * 2, 20)  # Cap at +20
        
        # Analyst sentiment
        if analyst.get('consensus_rating') == 'Strong Buy':
            score += 15
        elif analyst.get('consensus_rating') == 'Buy':
            score += 10
        
        # Volume surge
        if 'volume' in quote and 'avgVolume' in quote:
            volume_ratio = quote['volume'] / quote['avgVolume']
            if volume_ratio > 2.0:
                score += 10
        
        return min(max(score, 0), 100)
    
    def _generate_trade_setup(self, quote: Dict, analyst: Dict) -> Dict:
        """Generate specific trade setup recommendations"""
        
        current_price = quote.get('price', 0)
        target_price = analyst.get('average_price_target', current_price * 1.1)
        
        return {
            'entry_zone': f"{current_price * 0.98:.2f} - {current_price * 1.02:.2f}",
            'stop_loss': f"{current_price * 0.95:.2f}",
            'take_profit_1': f"{current_price * 1.05:.2f}",
            'take_profit_2': f"{current_price * 1.10:.2f}",
            'risk_reward_ratio': round((target_price - current_price) / (current_price * 0.05), 2),
            'position_size_recommendation': '1-2% of portfolio for high conviction'
        }
    
    def _assess_risk(self, quote: Dict, profile: Dict) -> Dict:
        """Assess risk factors"""
        
        risk_level = "MEDIUM"
        risk_factors = []
        
        # Check volatility
        if 'yearLow' in quote and 'yearHigh' in quote:
            volatility = (quote['yearHigh'] - quote['yearLow']) / quote['yearLow']
            if volatility > 0.5:
                risk_level = "HIGH"
                risk_factors.append("High 52-week volatility")
        
        # Check market cap
        market_cap = quote.get('marketCap', 0)
        if market_cap < 2e9:  # Under 2B
            risk_factors.append("Small cap - higher volatility")
        
        return {
            'overall_risk': risk_level,
            'risk_factors': risk_factors,
            'recommendations': [
                "Use smaller position size",
                "Set tight stop loss",
                "Monitor closely"
            ] if risk_level == "HIGH" else ["Standard risk management"]
        }
    
    def export_to_csv(self, filename: str = "trading_opportunities.csv"):
        """Export scan results to CSV"""
        if not self.scan_results:
            print("No scan results to export")
            return
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Ticker', 'Scan Type', 'Price', 'Change %', 
                'Volume', 'Opportunity Score', 'Analyst Rating',
                'Entry Zone', 'Stop Loss', 'Take Profit'
            ])
            
            for opp in self.scan_results:
                writer.writerow([
                    opp['ticker'],
                    opp['scan_type'],
                    opp['quote'].get('price', 'N/A'),
                    opp['quote'].get('changesPercentage', 'N/A'),
                    opp['quote'].get('volume', 'N/A'),
                    f"{opp['opportunity_score']:.1f}",
                    opp['analyst_ratings'].get('consensus_rating', 'N/A'),
                    opp['trade_setup']['entry_zone'],
                    opp['trade_setup']['stop_loss'],
                    opp['trade_setup']['take_profit_1']
                ])
        
        print(f"✓ Exported {len(self.scan_results)} opportunities to {filename}")
    
    def generate_journal_entry(self, ticker: str) -> str:
        """Generate a structured trading journal entry"""
        
        opp = next((o for o in self.scan_results if o['ticker'] == ticker), None)
        if not opp:
            return f"No data found for {ticker}"
        
        journal = f"""
# Trading Journal Entry - {ticker}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Scan Type:** {opp['scan_type'].upper()}
**Opportunity Score:** {opp['opportunity_score']:.1f}/100

## Market Data
- **Current Price:** ${opp['quote'].get('price', 'N/A')}
- **Daily Change:** {opp['quote'].get('changesPercentage', 'N/A')}%
- **Volume:** {opp['quote'].get('volume', 'N/A'):,}
- **52-Week Range:** ${opp['quote'].get('yearLow', 'N/A')} - ${opp['quote'].get('yearHigh', 'N/A')}

## Analyst Sentiment
- **Consensus:** {opp['analyst_ratings'].get('consensus_rating', 'N/A')}
- **Price Target:** ${opp['analyst_ratings'].get('average_price_target', 'N/A')}
- **Upside Potential:** {((opp['analyst_ratings'].get('average_price_target', 0) / opp['quote'].get('price', 1)) - 1) * 100:.1f}%

## Trade Setup
- **Entry Zone:** {opp['trade_setup']['entry_zone']}
- **Stop Loss:** {opp['trade_setup']['stop_loss']}
- **Take Profit 1:** {opp['trade_setup']['take_profit_1']}
- **Take Profit 2:** {opp['trade_setup']['take_profit_2']}
- **Risk/Reward:** {opp['trade_setup']['risk_reward_ratio']}:1

## Risk Assessment
- **Risk Level:** {opp['risk_assessment']['overall_risk']}
- **Key Risks:** {', '.join(opp['risk_assessment']['risk_factors']) if opp['risk_assessment']['risk_factors'] else 'None identified'}

## Notes
[Add your analysis here before entering trade]

---
"""
        return journal
    
    def save_journal(self, ticker: str, output_dir: str = "journals"):
        """Save journal entry to markdown file"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        journal = self.generate_journal_entry(ticker)
        filename = f"{output_dir}/{ticker}_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        
        with open(filename, 'w') as f:
            f.write(journal)
        
        print(f"✓ Journal saved to {filename}")


def main():
    """Example usage"""
    
    # Initialize with your API key
    API_KEY = "YOUR_PERPLEXITY_API_KEY_HERE"
    
    scanner = TradingScanner(API_KEY)
    
    print("🔍 Smart Trading Scanner")
    print("=" * 50)
    
    # Scan for opportunities
    print("\nScanning market gainers...")
    opportunities = scanner.scan_opportunities(scan_type="gainers", limit=10)
    
    print(f"\n✓ Found {len(opportunities)} opportunities")
    
    # Display top 5
    print("\n📊 Top Opportunities:")
    print("-" * 50)
    for i, opp in enumerate(opportunities[:5], 1):
        print(f"{i}. {opp['ticker']} - Score: {opp['opportunity_score']:.1f}")
        print(f"   Price: ${opp['quote'].get('price', 'N/A')} | Change: {opp['quote'].get('changesPercentage', 'N/A')}%")
        print(f"   Analyst: {opp['analyst_ratings'].get('consensus_rating', 'N/A')}")
        print()
    
    # Export results
    scanner.export_to_csv()
    
    # Generate journal for top pick
    if opportunities:
        top_ticker = opportunities[0]['ticker']
        scanner.save_journal(top_ticker)
        print(f"\n📝 Journal generated for {top_ticker}")


if __name__ == "__main__":
    main()
