class AILanguageAgent:
    def __init__(self, model):
        self.model = model
        self.name = "AI Language Agent"

    def process_query(self, query, market_data, news_data, analysis_data):
        context = self._build_context(market_data, news_data, analysis_data)
        prompt = f"""
        You are an expert financial advisor and market analyst. Answer the user's question based on the real-time market data provided.
        USER QUESTION: {query}
        CURRENT MARKET DATA:
        {context}
        INSTRUCTIONS:
        1. Answer the specific question asked by the user
        2. Use the real market data provided to give accurate, current information
        3. If asked about portfolio exposure, calculate percentages based on market caps
        4. If asked about earnings, mention specific companies and their performance
        5. If asked about risk, analyze volatility and market conditions
        6. If asked about recommendations, provide specific actionable advice
        7. Keep response professional but conversational (suitable for voice delivery)
        8. Include specific numbers, percentages, and company names
        9. If the question is outside financial scope, politely redirect to financial topics
        10. Maximum 200 words for voice-friendly delivery
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"I apologize, but I encountered an error processing your query: {str(e)}. Please try rephrasing your question."

    def _build_context(self, market_data, news_data, analysis_data):
        context_parts = []
        if market_data:
            context_parts.append("STOCK PERFORMANCE:")
            for symbol, data in market_data.items():
                if 'error' not in data:
                    context_parts.append(f"- {symbol} ({data.get('company_name', symbol)}): ${data.get('current_price', 0)}, Change: {data.get('change_percent', 0)}%, Sector: {data.get('sector', 'N/A')}, Market Cap: {data.get('market_cap', 'N/A')}")
        if analysis_data:
            context_parts.append("\nTECHNICAL ANALYSIS:")
            for symbol, analysis in analysis_data.items():
                context_parts.append(f"- {symbol}: Trend: {analysis.get('trend', 'N/A')}, Volatility: {analysis.get('volatility', 0)}%, Risk: {analysis.get('risk_level', 'N/A')}")
        if news_data:
            context_parts.append("\nLATEST NEWS:")
            for symbol, news_list in news_data.items():
                if news_list and len(news_list) > 0:
                    latest_news = news_list[0]
                    context_parts.append(f"- {symbol}: {latest_news.get('title', 'No recent news')}")
        return "\n".join(context_parts)