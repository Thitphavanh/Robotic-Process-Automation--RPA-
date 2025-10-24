# 🤖 AI Agent - Dynamic Market Discovery

## Overview

Advanced AI-powered feature that uses **Claude AI (Anthropic)** to dynamically discover and track top stocks and cryptocurrencies in real-time, eliminating the need for hardcoded lists.

## ✨ Key Features

### 1. **Dynamic Stock Discovery**
- 🇹🇭 **Thai Stock Exchange (SET)**: Auto-discovers top 10 Thai stocks
- 🇺🇸 **US Markets (NYSE/NASDAQ)**: Auto-discovers top 10 US stocks
- 🇪🇺 **European Markets**: Auto-discovers top 10 European stocks
- 🇨🇳 **Chinese Markets**: Auto-discovers top 10 Chinese stocks

### 2. **Dynamic Cryptocurrency Discovery**
- 💰 Auto-discovers top 10 cryptocurrencies by market cap
- 📊 Uses CoinGecko API for real-time pricing
- 🔄 Updates automatically based on current market conditions

### 3. **Market Sentiment Analysis**
- 📈 Analyzes overall market sentiment (bullish/bearish/neutral)
- 🎯 Provides confidence levels and key factors
- 📝 Thai language summaries for easy understanding

## 🏗️ Architecture

```
┌─────────────────┐
│  News Scraper   │
│    Service      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│   AI Agent      │◄────►│   Claude AI      │
│   (ai_agent.py) │      │   (Anthropic)    │
└────────┬────────┘      └──────────────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│   yfinance      │      │   CoinGecko API  │
│   (Stock Data)  │      │   (Crypto Data)  │
└─────────────────┘      └──────────────────┘
```

## 📋 How It Works

### Stock Discovery Flow:
1. **AI Agent Request**: Scraper requests top stocks for a specific market
2. **Claude AI Analysis**: Claude AI analyzes current market and returns top stocks
3. **Data Fetching**: yfinance fetches real-time prices for discovered stocks
4. **Database Storage**: Articles saved with current prices and metadata

### Crypto Discovery Flow:
1. **AI Agent Request**: Scraper requests top cryptocurrencies
2. **Claude AI Analysis**: Claude AI returns top crypto by market cap
3. **CoinGecko API**: Fetches real-time prices for discovered cryptos
4. **Database Storage**: Articles saved with 24h changes and market cap

## 🚀 Usage

### Basic Usage

```python
from rpa_bot.ai_agent import get_ai_agent

# Initialize AI Agent
agent = get_ai_agent()

# Discover top Thai stocks
thai_stocks = agent.discover_top_stocks(market='thai', limit=10)
# Returns: [('PTT.BK', 'ปตท.'), ('CPALL.BK', 'ซีพีออลล์'), ...]

# Discover top cryptocurrencies
cryptos = agent.discover_top_crypto(limit=10)
# Returns: [{'id': 'bitcoin', 'name': 'Bitcoin', 'symbol': 'BTC'}, ...]

# Analyze market sentiment
sentiment = agent.analyze_market_sentiment(market='us')
# Returns: {'sentiment': 'bullish', 'confidence': 0.75, 'summary': '...'}
```

### Integration with News Scraper

The AI Agent is automatically integrated into the News Scraper Service:

```python
from rpa_bot.news_scraper import NewsScraperService

scraper = NewsScraperService()

# AI Agent is initialized automatically
# scraper.ai_agent is available

# Scraping automatically uses AI Agent for discovery
results = scraper.scrape_all_categories()
```

## 🔧 Configuration

### Environment Variables

Add to `docker-compose.yml` and `.env`:

```yaml
environment:
  - ANTHROPIC_API_KEY=sk-ant-api03-xxx...
  - GEMINI_API_KEY=AIzaSyA3-xxx...
```

### Requirements

Add to `requirements.txt`:

```
anthropic>=0.18.0
```

## 📊 Comparison: Before vs After

### Before (Hardcoded Lists)
```python
# ❌ Static list - requires manual updates
thai_stocks = [
    ('PTT.BK', 'ปตท.'),
    ('CPALL.BK', 'ซีพีออลล์'),
    # ... hardcoded 10 stocks
]
```

### After (AI Agent)
```python
# ✅ Dynamic discovery - auto-updates based on market
thai_stocks = agent.discover_top_stocks(market='thai', limit=10)
# AI Agent fetches current top 10 stocks dynamically
```

## 🎯 Benefits

1. **Always Up-to-Date**: No more outdated stock lists
2. **Market-Aware**: Adapts to market changes automatically
3. **Scalable**: Easy to add new markets or change criteria
4. **Intelligent**: Uses AI to understand market context
5. **Fallback Safe**: Falls back to cached data if AI is unavailable

## 🛡️ Fallback Mechanism

If Claude AI is unavailable:
1. System falls back to cached/default stock lists
2. Warning logged: "⚠ AI Agent discovery failed, using fallback"
3. Service continues without interruption

## 📈 Performance

- **AI Discovery Time**: ~2-5 seconds per market
- **Cache Duration**: Recommended 1 hour for production
- **API Rate Limits**: Respects Anthropic rate limits
- **Fallback Time**: <0.1 seconds

## 🔐 Security

- API keys stored in environment variables
- Never hardcoded in source code
- Supports Docker secrets for production
- Secure communication with Claude AI API

## 🧪 Testing

### Test AI Agent Discovery
```bash
python manage.py shell

from rpa_bot.ai_agent import get_ai_agent
agent = get_ai_agent()

# Test stock discovery
stocks = agent.discover_top_stocks('thai', 5)
print(stocks)

# Test crypto discovery
cryptos = agent.discover_top_crypto(5)
print(cryptos)
```

### Test News Scraper Integration
```bash
python manage.py shell

from rpa_bot.news_scraper import scrape_all_news_sources
results = scrape_all_news_sources()
print(results)
```

## 📝 Logs

Monitor AI Agent activity in logs:

```
🤖 AI Agent initialized for dynamic market discovery
🤖 AI Agent discovering top Thai stocks...
✓ AI Agent discovered 10 Thai stocks
🤖 AI Agent discovering top US stocks...
✓ AI Agent discovered 10 US stocks
🤖 AI Agent discovering top cryptocurrencies...
✓ AI Agent discovered 10 cryptocurrencies
```

## 🔮 Future Enhancements

- [ ] Multi-language support for analysis
- [ ] Custom market criteria (by sector, industry, etc.)
- [ ] Historical trend analysis
- [ ] Predictive market insights
- [ ] Integration with more data sources
- [ ] Real-time WebSocket updates

## 🤝 Contributing

To extend AI Agent capabilities:

1. Add new discovery methods in `ai_agent.py`
2. Create prompts for Claude AI in `_create_*_prompt()` methods
3. Add parsing logic in `_parse_*_response()` methods
4. Update News Scraper to use new methods

## 📚 API Reference

### ClaudeAIAgent Class

#### `discover_top_stocks(market: str, limit: int = 10)`
Discovers top stocks for a specific market.

**Parameters:**
- `market`: 'thai', 'us', 'europe', 'china'
- `limit`: Number of stocks to discover (default: 10)

**Returns:** `List[Tuple[str, str]]` - List of (symbol, name) tuples

#### `discover_top_crypto(limit: int = 10)`
Discovers top cryptocurrencies by market cap.

**Parameters:**
- `limit`: Number of cryptos to discover (default: 10)

**Returns:** `List[Dict[str, str]]` - List of crypto dictionaries

#### `analyze_market_sentiment(market: str)`
Analyzes market sentiment using Claude AI.

**Parameters:**
- `market`: 'thai', 'us', 'europe', 'china', 'crypto'

**Returns:** `Dict` - Sentiment analysis results

## 💡 Tips

1. **API Key Management**: Use environment variables, never commit keys
2. **Rate Limiting**: Implement caching to reduce API calls
3. **Error Handling**: Always have fallback data ready
4. **Monitoring**: Log all AI Agent activities for debugging
5. **Testing**: Test with small limits first before scaling

## 📞 Support

For issues or questions:
- Check logs for AI Agent errors
- Verify API key is valid and active
- Ensure network connectivity to Anthropic API
- Review fallback mechanisms if AI is unavailable

---

**Version**: 1.0.0
**Last Updated**: 2025-01-25
**Powered by**: Claude AI (Anthropic) + Gemini AI (Google)
