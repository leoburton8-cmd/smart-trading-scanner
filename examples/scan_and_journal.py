#!/usr/bin/env python3
"""
Example: Scan market and generate journals for top 3 opportunities
"""

from scanner import TradingScanner

API_KEY = "YOUR_PERPLEXITY_API_KEY_HERE"

# Initialize scanner
scanner = TradingScanner(API_KEY)

# Scan for gainers
print("Scanning top gainers...")
opportunities = scanner.scan_opportunities(scan_type="gainers", limit=10)

# Show top 3
print(f"\nTop {min(3, len(opportunities))} opportunities:\n")
for i, opp in enumerate(opportunities[:3], 1):
    print(f"{i}. {opp['ticker']}")
    print(f"   Score: {opp['opportunity_score']:.1f}/100")
    print(f"   Price: ${opp['quote'].get('price', 'N/A')} ({opp['quote'].get('changesPercentage', 'N/A')}%)")
    print(f"   Analyst: {opp['analyst_ratings'].get('consensus_rating', 'N/A')}")
    print(f"   Entry: {opp['trade_setup']['entry_zone']}")
    print(f"   Stop: {opp['trade_setup']['stop_loss']}")
    print()

# Export to CSV
scanner.export_to_csv("today_scans.csv")

# Generate journals for top 3
for opp in opportunities[:3]:
    scanner.save_journal(opp['ticker'])

print("✓ Done! Check 'journals/' folder for markdown files.")
