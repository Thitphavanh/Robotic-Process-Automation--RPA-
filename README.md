# 🤖 Stock Bot RPA - Complete Documentation

## 📋 Overview

This repository contains multiple versions of automated stock market data collection bots using RPA (Robotic Process Automation).

---

## 📂 File Structure

### Basic Versions
- **stock_bot.py** - Original version (cross-platform attempt)
- **stock_bot_macos.py** ⭐ - Simple macOS version (Google search + screenshot)
- **stock_bot_windows.py** - Simple Windows version (Google search + screenshot)

### Auto-Click Versions (10 websites)
- **stock_bot_auto_click_macos.py** - macOS: Clicks through 10 search results
- **stock_bot_auto_click_windows.py** - Windows: Clicks through 10 search results

### Direct Visit Versions (5 specific URLs)
- **stock_bot_direct_visit_macos.py** - macOS: Visits 5 specific stock websites
- **stock_bot_direct_visit_windows.py** - Windows: Visits 5 specific stock websites

### Interactive Versions (8 actions per site)
- **stock_bot_interactive_macos.py** - macOS: Advanced interaction with website content
- **stock_bot_interactive_windows.py** - Windows: Advanced interaction with website content

### AI-Powered Versions
- **stock_bot_macos_agent.py** ⚠️ - Uses Claude AI (requires valid API key)
- **stock_bot_macos_no_api.py** ⭐ - Uses OCR (free, no API needed)

### Documentation
- **README_API_KEY.md** - Guide for fixing Claude API authentication
- **README.md** - This file

---

## 🚀 Quick Start Guide

### For macOS Users - Simple Version

```bash
# Install dependencies
pip install pyautogui pillow

# Run the simple version
python stock_bot_macos.py
```

### For macOS Users - Advanced OCR Version (Recommended)

```bash
# Install dependencies
pip install pyautogui pillow pytesseract

# Install Tesseract OCR
brew install tesseract tesseract-lang

# Run with OCR analysis
python stock_bot_macos_no_api.py
```

### For Windows Users - Simple Version

```bash
# Install dependencies
pip install pyautogui pillow

# Run the simple version
python stock_bot_windows.py
```

---

## 📊 Feature Comparison

| Feature | Basic | Auto-Click | Direct Visit | Interactive | AI Agent | No API (OCR) |
|---------|-------|------------|--------------|-------------|----------|--------------|
| Google Search | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ |
| Screenshot | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Auto-click websites | ❌ | ✅ (10 sites) | ✅ (5 sites) | ✅ (5 sites) | ✅ (3 sites) | ✅ (3 sites) |
| Website interaction | ❌ | ⚡ Basic | ⚡⚡ Medium | ⚡⚡⚡ Advanced | ⚡⚡ Medium | ⚡⚡ Medium |
| AI Analysis | ❌ | ❌ | ❌ | ❌ | ✅ (Claude) | ⚡ (OCR) |
| Cost | Free | Free | Free | Free | $0.10-0.50/run | Free |
| API Required | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |

---

## 🎯 Which Version Should You Use?

### Use **stock_bot_macos.py** if:
- You just want to search Google and capture a screenshot
- First time testing RPA automation
- Don't need to visit multiple websites

### Use **stock_bot_auto_click_macos.py** if:
- You want to automatically visit 10 websites from search results
- Need to capture sponsored + organic results
- Want comprehensive market overview

### Use **stock_bot_direct_visit_macos.py** if:
- You have specific URLs you want to visit
- Don't want Google search step
- Want to visit: Webull, XTB, Trademan, SET, Investing.com

### Use **stock_bot_interactive_macos.py** if:
- You want advanced website interaction
- Need to scroll, click different areas, capture multiple angles
- Want 8 screenshots per website

### Use **stock_bot_macos_agent.py** if:
- You have a valid Anthropic API key
- Want AI-powered image analysis
- Need intelligent stock data extraction
- Have budget ($0.10-0.50 per run)

### Use **stock_bot_macos_no_api.py** ⭐ if:
- You want AI-like features without API costs
- Want text extraction with OCR
- Need keyword/number detection
- Prefer completely free solution
- **THIS IS THE RECOMMENDED VERSION**

---

## ⚙️ Installation

### macOS

```bash
# Basic dependencies (required for all versions)
pip install pyautogui pillow

# For OCR version (stock_bot_macos_no_api.py)
pip install pytesseract
brew install tesseract tesseract-lang

# For AI Agent version (stock_bot_macos_agent.py)
pip install anthropic
```

### Windows

```bash
# Basic dependencies (required for all versions)
pip install pyautogui pillow

# For AI Agent version
pip install anthropic
```

---

## 🔒 macOS Permissions

Before running any bot, you must grant permissions:

### 1. Accessibility Permission
1. Open **System Settings**
2. Go to **Privacy & Security** > **Accessibility**
3. Add Terminal (or your Python IDE)
4. Toggle it ON

### 2. Screen Recording Permission
1. Open **System Settings**
2. Go to **Privacy & Security** > **Screen Recording**
3. Add Terminal (or your Python IDE)
4. Toggle it ON

**⚠️ Restart Terminal after granting permissions!**

---

## 🎮 How to Run

### Basic Usage

```bash
python stock_bot_macos.py
```

### Advanced Usage with Modes

```bash
python stock_bot_macos_no_api.py

# Then select mode:
# 1. Dynamic Search (any query)
# 2. Stock Focus (Thai stock market)
# 3. Custom Query
```

---

## 📸 Output Files

### All versions create screenshots:
- **stock_price_result_macos.png** (basic version)
- **001_Website_Name_01_main.png** (numbered versions)
- **local_search_results.png** (no-API version)
- **local_website_01_main.png** (no-API version)

### AI/OCR versions also create:
- **analysis_report.txt** (AI Agent version)
- **local_analysis_report.txt** (No-API version)

---

## 🔧 Troubleshooting

### Issue: "No module named 'pyautogui'"
```bash
pip install pyautogui pillow
```

### Issue: "No module named 'anthropic'"
```bash
pip install anthropic
```

### Issue: "401 authentication error" (AI Agent version)
- Your API key is invalid or expired
- See **README_API_KEY.md** for detailed fix
- Or use **stock_bot_macos_no_api.py** instead (no API needed)

### Issue: Can't capture screenshots on macOS
- Grant Screen Recording permission (see Permissions section above)
- Restart Terminal
- Run again

### Issue: OCR not extracting text
```bash
# Install Tesseract
brew install tesseract tesseract-lang

# Verify installation
tesseract --version
```

### Issue: Bot clicks wrong positions
- Adjust screen position multipliers in code
- Different screen resolutions may need tuning
- Check your browser zoom level (should be 100%)

---

## 💰 Cost Analysis

| Version | Cost per Run | Monthly Cost (1x/day) | Notes |
|---------|--------------|----------------------|-------|
| Basic | $0 | $0 | Free forever |
| Auto-Click | $0 | $0 | Free forever |
| Direct Visit | $0 | $0 | Free forever |
| Interactive | $0 | $0 | Free forever |
| AI Agent | $0.10-0.50 | $3-15 | Requires Anthropic API |
| No API (OCR) | $0 | $0 | Free forever ⭐ |

---

## 🎨 Customization

### Change Search Query (Basic/Auto-Click versions)
```python
# Edit line ~12-32
search_term = "ราคาหุ้นไทยวันนี้"  # Change this
```

### Add More Websites (Direct Visit versions)
```python
# Edit the websites list
websites = [
    {"name": "Your Website", "url": "https://example.com"},
    # Add more...
]
```

### Change Number of Websites (Auto-Click versions)
```python
# Edit line ~136
for i in range(10):  # Change 10 to desired number
```

### Adjust Click Positions (All versions)
```python
# Edit position multipliers (0.0 to 1.0)
pyautogui.click(screen_width // 2, int(screen_height * 0.40))
#                                                      ^^^^ Change this
```

---

## 📊 Performance Tips

1. **Close unnecessary browser tabs** before running
2. **Use 100% browser zoom** for consistent clicking
3. **Disable browser popups** and notifications
4. **Use wired internet** for faster page loads
5. **Run during off-peak hours** for better website response
6. **Increase wait times** if websites are slow to load

---

## 🔐 Security & Privacy

1. **API Keys**: Never commit API keys to Git
2. **Screenshots**: May contain sensitive financial data
3. **Automation**: Some websites may block automated access
4. **Rate Limiting**: Don't run too frequently (respect website ToS)
5. **Data Storage**: Clear old screenshots regularly

---

## 📈 Use Cases

### 1. Daily Market Monitoring
```bash
# Run every morning
python stock_bot_macos_no_api.py
# Select mode 2: Stock Focus
```

### 2. Competitor Analysis
```bash
# Visit specific brokerage websites
python stock_bot_direct_visit_macos.py
```

### 3. Research & Documentation
```bash
# Interactive exploration with 8 screenshots per site
python stock_bot_interactive_macos.py
```

### 4. AI-Powered Insights (with API)
```bash
# Get intelligent analysis
python stock_bot_macos_agent.py
```

---

## 🛠️ Development

### Project Structure
```
Robotic-Process Automation-(RPA)/
├── stock_bot_macos.py              # Simple version
├── stock_bot_macos_agent.py        # AI version (needs API)
├── stock_bot_macos_no_api.py       # OCR version (recommended)
├── stock_bot_auto_click_macos.py   # 10 websites
├── stock_bot_direct_visit_macos.py # 5 specific URLs
├── stock_bot_interactive_macos.py  # Advanced interaction
├── README.md                       # This file
└── README_API_KEY.md              # API setup guide
```

### Adding New Features
1. Fork from the appropriate base version
2. Test with small delays first
3. Add error handling for each action
4. Document new features in this README

---

## 🆘 Getting Help

### If you encounter issues:

1. **Check this README** first
2. **Read README_API_KEY.md** for API issues
3. **Verify permissions** on macOS
4. **Check Python version** (3.8+ required)
5. **Update dependencies**: `pip install --upgrade pyautogui pillow`

### Common Questions:

**Q: Which Python version do I need?**
A: Python 3.8 or higher

**Q: Can I run on Linux?**
A: Yes, but you'll need to adapt keyboard shortcuts (use 'ctrl' instead of 'command')

**Q: Can I schedule this to run automatically?**
A: Yes, use cron (macOS/Linux) or Task Scheduler (Windows)

**Q: Is this legal?**
A: For personal research, yes. For commercial use, check website Terms of Service.

**Q: Can I modify the code?**
A: Yes, it's open for modification. Just maintain attribution.

---

## 📝 Version History

- **v1.0**: Basic Google search + screenshot
- **v2.0**: Added auto-click (10 websites)
- **v3.0**: Added direct visit (5 specific URLs)
- **v4.0**: Added interactive mode (8 actions per site)
- **v5.0**: Added AI Agent (Claude integration)
- **v6.0**: Added OCR version (no API needed) ⭐

---

## 🎉 Recommended Workflow

### For Beginners:
1. Start with **stock_bot_macos.py**
2. Once comfortable, try **stock_bot_macos_no_api.py**
3. Experiment with **stock_bot_interactive_macos.py**

### For Advanced Users:
1. Use **stock_bot_macos_no_api.py** for daily monitoring
2. Customize website lists in direct visit versions
3. If you have budget, try **stock_bot_macos_agent.py** with valid API

---

## 🌟 Best Practices

1. **Always test with small delays** (increase time.sleep() values)
2. **Don't spam websites** (respect rate limits)
3. **Keep screenshots organized** (create date folders)
4. **Monitor for changes** (websites may redesign)
5. **Backup your configurations** (if you customize positions)

---

## 📞 Support

For Anthropic API issues: https://support.anthropic.com/
For Python/PyAutoGUI issues: Check official documentation

---

**Made with ❤️ for automated stock market research**

**⭐ Star this project if you find it useful!**
