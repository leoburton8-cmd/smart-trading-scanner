#!/usr/bin/env python3
"""
Streamlit Web Dashboard for Smart Trading Scanner
==================================================
Interactive web interface for monitoring trading opportunities in real-time.

Run with: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import json

# Import scanner (make sure scanner.py is in same directory)
from scanner import TradingScanner

# Page config
st.set_page_config(
    page_title="Smart Trading Scanner",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #1e1e1e;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .stButton>button {
        background-color: #28a745;
        color: white;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session():
    """Initialize session state"""
    if 'scanner' not in st.session_state:
        st.session_state.scanner = None
    if 'scan_results' not in st.session_state:
        st.session_state.scan_results = []
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""


def sidebar_config():
    """Sidebar for configuration"""
    with st.sidebar:
        st.title("⚙️ Settings")
        
        # API Key input
        api_key = st.text_input(
            "Perplexity API Key",
            type="password",
            help="Get your key from https://www.perplexity.ai/settings/api",
            value=st.session_state.api_key
        )
        
        if api_key:
            st.session_state.api_key = api_key
            st.session_state.scanner = TradingScanner(api_key)
            st.success("✓ API key configured")
        
        st.divider()
        
        # Scan parameters
        st.subheader("Scan Settings")
        
        scan_type = st.selectbox(
            "Scan Type",
            ["gainers", "losers", "both"],
            index=0
        )
        
        limit = st.slider("Number of Stocks", 5, 50, 15)
        
        min_volume = st.number_input(
            "Min Volume",
            min_value=0,
            value=1000000,
            step=500000,
            format="%d"
        )
        
        st.divider()
        
        # Quick actions
        st.subheader("Quick Actions")
        
        if st.button("🔍 Run Scan", use_container_width=True):
            if st.session_state.scanner:
                with st.spinner("Scanning market..."):
                    results = st.session_state.scanner.scan_opportunities(
                        scan_type=scan_type,
                        limit=limit,
                        min_volume=min_volume
                    )
                    st.session_state.scan_results = results
                    st.success(f"✓ Found {len(results)} opportunities")
                    st.rerun()
            else:
                st.error("Please enter API key first")
        
        if st.button("📥 Export CSV", use_container_width=True):
            if st.session_state.scan_results:
                st.session_state.scanner.export_to_csv()
                st.success("✓ Exported to trading_opportunities.csv")
        
        st.divider()
        
        # Info
        st.markdown("""
        ### 📚 Resources
        - [GitHub Repo](https://github.com/leoburton8-cmd/smart-trading-scanner)
        - [Documentation](https://github.com/leoburton8-cmd/smart-trading-scanner/blob/main/README.md)
        - [API Reference](https://github.com/leoburton8-cmd/smart-trading-scanner/blob/main/API_REFERENCE.md)
        """)


def display_opportunity_card(opp, index):
    """Display a single opportunity card"""
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Header
        ticker = opp['ticker']
        scan_type = opp['scan_type'].upper()
        score = opp['opportunity_score']
        
        # Color coding
        if score >= 80:
            score_color = "🟢"
        elif score >= 60:
            score_color = "🟡"
        else:
            score_color = "🔴"
        
        st.markdown(f"### {score_color} {ticker} | {scan_type}")
        
        # Key metrics
        quote = opp.get('quote', {})
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric(
                "Price",
                f"${quote.get('price', 'N/A')}",
                f"{quote.get('changesPercentage', 'N/A')}%"
            )
        
        with col_b:
            st.metric(
                "Volume",
                f"{quote.get('volume', 0):,}",
                "vs avg"
            )
        
        with col_c:
            st.metric(
                "Opportunity Score",
                f"{score:.1f}/100"
            )
        
        # Analyst sentiment
        analyst = opp.get('analyst_ratings', {})
        st.markdown(f"**Analyst Consensus:** {analyst.get('consensus_rating', 'N/A')}")
        
        # Trade setup
        setup = opp.get('trade_setup', {})
        with st.expander("📊 Trade Setup"):
            st.markdown(f"""
            - **Entry Zone:** {setup.get('entry_zone', 'N/A')}
            - **Stop Loss:** {setup.get('stop_loss', 'N/A')}
            - **Take Profit 1:** {setup.get('take_profit_1', 'N/A')}
            - **Take Profit 2:** {setup.get('take_profit_2', 'N/A')}
            - **Risk/Reward:** {setup.get('risk_reward_ratio', 'N/A')}:1
            """)
        
        # Risk assessment
        risk = opp.get('risk_assessment', {})
        with st.expander("⚠️ Risk Assessment"):
            st.markdown(f"""
            **Risk Level:** {risk.get('overall_risk', 'N/A')}
            
            **Risk Factors:**
            {chr(10).join(['• ' + rf for rf in risk.get('risk_factors', [])]) if risk.get('risk_factors') else 'None identified'}
            """)
    
    with col2:
        # Quick actions
        st.markdown("### Actions")
        
        if st.button(f"📝 Journal", key=f"journal_{index}"):
            st.session_state.scanner.save_journal(ticker)
            st.success(f"Journal saved for {ticker}")
        
        if st.button(f"📈 Chart", key=f"chart_{index}"):
            st.session_state.selected_ticker = ticker
        
        st.divider()
        
        # Quick stats
        st.markdown("""**Quick Stats**""")
        st.write(f"Market Cap: ${quote.get('marketCap', 0):,.0f}")
        st.write(f"52W High: ${quote.get('yearHigh', 'N/A')}")
        st.write(f"52W Low: ${quote.get('yearLow', 'N/A')}")


def main_dashboard():
    """Main dashboard content"""
    
    st.title("📊 Smart Trading Scanner Dashboard")
    st.markdown("Real-time market analysis and trading opportunity detection")
    
    # Display results if available
    if st.session_state.scan_results:
        results = st.session_state.scan_results
        
        # Summary metrics
        st.divider()
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Opportunities Found", len(results))
        
        with col2:
            avg_score = sum(r['opportunity_score'] for r in results) / len(results)
            st.metric("Avg Opportunity Score", f"{avg_score:.1f}")
        
        with col3:
            gainers = len([r for r in results if r['scan_type'] == 'gainer'])
            st.metric("Gainers", gainers)
        
        with col4:
            losers = len([r for r in results if r['scan_type'] == 'loser'])
            st.metric("Losers", losers)
        
        st.divider()
        
        # Display each opportunity
        st.subheader("🎯 Trading Opportunities")
        
        for i, opp in enumerate(results):
            display_opportunity_card(opp, i)
            st.divider()
        
        # Export section
        st.subheader("📥 Export & Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Download Full CSV", use_container_width=True):
                st.session_state.scanner.export_to_csv()
                st.success("✓ Downloaded trading_opportunities.csv")
        
        with col2:
            if st.button("Generate All Journals", use_container_width=True):
                for opp in results[:5]:  # Top 5
                    st.session_state.scanner.save_journal(opp['ticker'])
                st.success("✓ Generated journals for top 5 opportunities")
    
    else:
        # Empty state
        st.info("👈 Run a scan from the sidebar to see opportunities")
        
        # Example data
        st.markdown("### What You'll See")
        st.markdown("""
        - **Real-time market data** from top gainers and losers
        - **AI-powered opportunity scores** (0-100)
        - **Analyst consensus ratings** and price targets
        - **Automated trade setups** with entry zones, stops, and targets
        - **Risk assessments** with key risk factors
        - **One-click journal generation** for trade tracking
        """)


if __name__ == "__main__":
    initialize_session()
    sidebar_config()
    main_dashboard()
