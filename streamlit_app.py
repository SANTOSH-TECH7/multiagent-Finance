# File: streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from config import Config
from orchestrator import FinanceOrchestrator

# Configure page
st.set_page_config(
    page_title="🎙️ Dynamic Finance Assistant",
    page_icon="🎙️",
    layout="wide"
)

# Initialize config
config = Config()

# Sidebar configuration
with st.sidebar:
    st.header("🔧 Configuration")
    api_key = st.text_input("Google Gemini API Key", type="password")
    if api_key:
        success = config.setup_gemini(api_key)
        if success:
            st.success("✅ Gemini API configured successfully!")
        else:
            st.error("❌ Failed to configure Gemini API")
    custom_symbols = st.text_input("Custom Stock Symbols (optional)", placeholder="AAPL, GOOGL, TSLA")

# Main interface
st.title("🎙️ Dynamic Multi-Agent Finance Assistant")
st.subheader("Ask any financial question - Get real-time, intelligent answers")

sample_questions = [
    "What's our risk exposure in Asia tech stocks today?",
    "How is Apple performing compared to Microsoft this quarter?",
    "Should I buy Tesla stock right now based on recent news?",
    "What's the current market sentiment for technology stocks?"
]
selected_question = st.selectbox("Choose a sample question:", [""] + sample_questions)
user_query = st.text_area("Your Financial Question:", value=selected_question, height=100)

if st.button("🚀 Get AI-Powered Analysis", type="primary"):
    if not api_key:
        st.error("🔑 Please provide your Gemini API key in the sidebar")
    elif not user_query.strip():
        st.warning("💭 Please enter a financial question")
    else:
        orchestrator = FinanceOrchestrator()
        orchestrator.set_ai_agent(config.model)
        symbols = [s.strip().upper() for s in custom_symbols.split(",") if s.strip()] if custom_symbols else None
        with st.spinner("🔄 Processing your query with AI agents..."):
            result = orchestrator.process_query(user_query, symbols)
            st.success("✅ Analysis Complete!")
            st.markdown("### 🤖 AI Financial Advisor Response")
            st.info(result['response'])
            st.markdown(f"🎤 **Voice Ready:** {result['voice_info']['word_count']} words, ~{result['voice_info']['estimated_duration_seconds']}s duration")

            if result['market_data']:
                st.markdown("### 📊 Real-Time Market Data")
                fig = go.Figure()
                for symbol, data in result['market_data'].items():
                    if 'error' not in data and 'price_history' in data:
                        fig.add_trace(go.Scatter(
                            x=data['dates'],
                            y=data['price_history'],
                            mode='lines',
                            name=f"{symbol} (${data['current_price']})"
                        ))
                fig.update_layout(
                    title="Stock Price Performance (Last 30 Days)",
                    xaxis_title="Date",
                    yaxis_title="Price ($)",
                    template="plotly_white",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)

                table_data = [
                    {
                        'Symbol': sym,
                        'Company': dat.get('company_name', sym),
                        'Price': f"${dat.get('current_price', 0)}",
                        'Change %': f"{dat.get('change_percent', 0)}%",
                        'Sector': dat.get('sector', 'N/A')
                    } for sym, dat in result['market_data'].items() if 'error' not in dat
                ]
                st.dataframe(pd.DataFrame(table_data), use_container_width=True)

            if result['analysis_data']:
                st.markdown("### 📈 Technical Analysis")
                analysis_table = [
                    {
                        'Symbol': sym,
                        'Trend': dat.get('trend'),
                        'Volatility': f"{dat.get('volatility')}%",
                        'Risk Level': dat.get('risk_level'),
                        'Support': f"${dat.get('support_level')}",
                        'Resistance': f"${dat.get('resistance_level')}"
                    } for sym, dat in result['analysis_data'].items()
                ]
                st.dataframe(pd.DataFrame(analysis_table), use_container_width=True)

            if result['news_data']:
                st.markdown("### 📰 Latest Financial News")
                for sym, news_list in result['news_data'].items():
                    if news_list and news_list[0].get('title'):
                        with st.expander(f"📈 {sym} News"):
                            for news in news_list[:2]:
                                st.markdown(f"**{news['title']}**")
                                st.markdown(news['summary'])
                                st.markdown("---")

if __name__ == "__main__":
    pass
