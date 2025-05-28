import yfinance as yf
from datetime import datetime

class MarketDataAgent:
    def __init__(self):
        self.name = "Market Data Agent"

    def get_stock_data(self, symbols, period="6mo"):
        data = {}
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period=period)
                info = ticker.info

                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
                    change_pct = ((current_price - prev_price) / prev_price) * 100

                    data[symbol] = {
                        'current_price': round(current_price, 2),
                        'change_percent': round(change_pct, 2),
                        'volume': hist['Volume'].iloc[-1],
                        'market_cap': info.get('marketCap', 'N/A'),
                        'sector': info.get('sector', 'N/A'),
                        'company_name': info.get('longName', symbol),
                        'pe_ratio': info.get('trailingPE', 'N/A'),
                        'price_history': hist['Close'].tolist()[-30:],
                        'dates': [d.strftime('%Y-%m-%d') for d in hist.index[-30:]]
                    }
            except Exception as e:
                data[symbol] = {'error': str(e)}

        return data

    def get_portfolio_metrics(self, symbols):
        data = self.get_stock_data(symbols)
        total_market_cap = 0
        asia_tech_cap = 0

        asia_tech_symbols = ['TSM', 'TSMC', '005930.KS', 'ASML', 'SONY', 'BABA']

        for symbol, info in data.items():
            if isinstance(info.get('market_cap'), (int, float)):
                total_market_cap += info['market_cap']
                if symbol in asia_tech_symbols or 'Technology' in str(info.get('sector', '')):
                    asia_tech_cap += info['market_cap']

        exposure = (asia_tech_cap / total_market_cap * 100) if total_market_cap > 0 else 0

        return {
            'asia_tech_exposure': round(exposure, 1),
            'total_portfolio_value': total_market_cap,
            'asia_tech_value': asia_tech_cap,
            'stock_data': data
        }