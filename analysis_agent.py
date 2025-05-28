import numpy as np

class AnalysisAgent:
    def __init__(self):
        self.name = "Quantitative Analysis Agent"

    def analyze_performance(self, market_data):
        analysis = {}
        for symbol, data in market_data.items():
            if 'error' not in data and 'price_history' in data:
                prices = np.array(data['price_history'])
                if len(prices) > 1:
                    returns = np.diff(prices) / prices[:-1]
                    volatility = np.std(returns) * np.sqrt(252) * 100
                    recent_trend = np.polyfit(range(len(prices[-10:])), prices[-10:], 1)[0]
                    trend = 'Bullish' if recent_trend > 0 else 'Bearish'
                    support = np.min(prices[-20:]) if len(prices) >= 20 else np.min(prices)
                    resistance = np.max(prices[-20:]) if len(prices) >= 20 else np.max(prices)

                    analysis[symbol] = {
                        'volatility': round(volatility, 2),
                        'trend': trend,
                        'trend_strength': abs(recent_trend),
                        'support_level': round(support, 2),
                        'resistance_level': round(resistance, 2),
                        'risk_level': 'High' if volatility > 30 else 'Medium' if volatility > 15 else 'Low'
                    }
        return analysis