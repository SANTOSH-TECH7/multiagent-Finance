from market_agent import MarketDataAgent
from news_agent import NewsAgent
from analysis_agent import AnalysisAgent
from voice_agent import VoiceAgent
from ai_language_agent import AILanguageAgent
from yfinance import Ticker
import re

class FinanceOrchestrator:
    def __init__(self):
        self.market_agent = MarketDataAgent()
        self.news_agent = NewsAgent()
        self.analysis_agent = AnalysisAgent()
        self.voice_agent = VoiceAgent()
        self.ai_agent = None

    def set_ai_agent(self, model):
        self.ai_agent = AILanguageAgent(model)

    def process_query(self, query, symbols=None):
        if not self.ai_agent:
            return "AI Language Agent not initialized. Please provide API key."

        if not symbols:
            symbols = self._extract_symbols_from_query(query)
            if not symbols:
                symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'TSM']

        market_data = self.market_agent.get_stock_data(symbols)
        news_data = self.news_agent.get_earnings_news(symbols)
        analysis_data = self.analysis_agent.analyze_performance(market_data)
        ai_response = self.ai_agent.process_query(query, market_data, news_data, analysis_data)
        voice_info = self.voice_agent.text_to_speech_info(ai_response)

        return {
            'query': query,
            'response': ai_response,
            'market_data': market_data,
            'news_data': news_data,
            'analysis_data': analysis_data,
            'voice_info': voice_info,
            'symbols_analyzed': symbols
        }

    def _extract_symbols_from_query(self, query):
        NAME_TO_TICKER = {
            "APPLE": "AAPL",
            "MICROSOFT": "MSFT",
            "GOOGLE": "GOOGL",
            "TESLA": "TSLA",
            "NVIDIA": "NVDA"
        }

        words = set(re.findall(r'\b[A-Z]{2,6}\b', query.upper()))
        possible_symbols = []

        for word in words:
            if word in NAME_TO_TICKER:
                possible_symbols.append(NAME_TO_TICKER[word])
            else:
                try:
                    ticker = Ticker(word)
                    hist = ticker.history(period="1d")
                    if not hist.empty:
                        possible_symbols.append(word)
                except:
                    continue

        if 'tech' in query.lower():
            possible_symbols.extend(['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'TSM'])
        if 'asia' in query.lower():
            possible_symbols.extend(['TSM', 'BABA', 'SONY'])

        return list(set(possible_symbols))
