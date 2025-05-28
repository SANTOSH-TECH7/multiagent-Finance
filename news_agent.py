import yfinance as yf

class NewsAgent:
    def __init__(self):
        self.name = "News Scraping Agent"

    def get_earnings_news(self, symbols):
        news_data = {}

        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                news = ticker.news[:3]
                news_items = []
                for item in news:
                    news_items.append({
                        'title': item.get('title', ''),
                        'summary': item.get('summary', '')[:200] + '...',
                        'url': item.get('link', ''),
                        'published': item.get('providerPublishTime', '')
                    })
                news_data[symbol] = news_items
            except Exception as e:
                news_data[symbol] = [{'title': f'Error fetching news: {str(e)}', 'summary': '', 'url': '', 'published': ''}]

        return news_data