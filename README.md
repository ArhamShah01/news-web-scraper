# Times of India Headlines Scraper 📰

A **Python web scraper** that extracts the latest news headlines from [Times of India](https://timesofindia.indiatimes.com) across **10 different news categories** with a user-friendly interactive menu.

---

## 📋 Features

✅ **10 News Categories** - Home, Sports, Business, Technology, Entertainment, India, World, Health, Life & Style, and Education

✅ **Robots.txt Compliance** - Automatically verifies scraping permissions before proceeding

✅ **Smart Filtering** - Removes category headers and promotional content, extracting only actual news headlines

✅ **Clean Text Processing** - Removes dates, prefixes, and artifacts for readable headlines

✅ **Error Handling** - Gracefully handles timeouts, connection errors, and HTTP failures

✅ **Interactive Menu** - Simple input system supporting both genre names and numeric selection

✅ **Visual Feedback** - Emoji-enhanced console output for better user experience

---

## 🎯 Supported Categories

| # | Category | Code | URL |
|---|----------|------|-----|
| 1 | Home (All News) | `home` | `/home/headlines` |
| 2 | Sports | `sports` | `/sports/` |
| 3 | Business | `business` | `/business/` |
| 4 | Technology | `tech` | `/technology` |
| 5 | Entertainment | `entertainment` | `/etimes` |
| 6 | India | `india` | `/india/` |
| 7 | World | `world` | `/world/` |
| 8 | Health | `health` | `/life-style/health-fitness` |
| 9 | Life & Style | `life` | `/life-style` |
| 10 | Education | `education` | `/education/` |

---

## 📦 Requirements

**Python 3.10+** with the following libraries:

```bash
requests>=2.31.0
beautifulsoup4>=4.12.0
```

### Installation

```bash
# Clone or download the project
cd your-scraper-directory

# Install dependencies
pip install -r requirements.txt
```

Or install manually:

```bash
pip install requests beautifulsoup4
```

---

## 🚀 Usage

### Basic Execution

```bash
python main.py
```

### Interactive Menu Example

```
🔍 Times of India Headlines Scraper with Genre Selection

================================================================================
📚 Available Genres:
================================================================================

 1. Home (All News)           ('home')
 2. Sports                    ('sports')
 3. Business                  ('business')
 4. Technology                ('tech')
 5. Entertainment             ('entertainment')
 6. India                     ('india')
 7. World                     ('world')
 8. Health                    ('health')
 9. Life & Style              ('life')
10. Education                 ('education')

================================================================================

Enter genre name or number (e.g., 'sports' or '1'): sports
```

### Input Options

You can input either:

- **Numeric** (1-10): `1`, `5`, `10`
- **Genre Name**: `sports`, `tech`, `india`

---

## 📊 Output Example

```
🔍 Times of India Headlines Scraper with Genre Selection

✨ Selected Genre: Sports
📍 Target: https://timesofindia.indiatimes.com/sports/

📋 Checking robots.txt compliance...
 └─ Path is allowed by robots.txt

📥 Fetching webpage...
 └─ ✅ Webpage fetched successfully

🔎 Parsing headlines...
 └─ ✅ Found 10 headlines

================================================================================
📰 Times of India - Sports (Top 10 Headlines)
================================================================================

 1. IPL 2026 Auction: Updated players list for all 10 teams; who got whom
 2. Venkatesh Iyer takes 70% pay cut; joins RCB from KKR
 3. Auqib Nabi Dar: Meet J&K pacer sold to DC for Rs 8.4 crore
 4. Prashant Veer: 20-year-old left-armer snapped up by CSK for Rs 14.20 crore
 5. KKR Full Team Player List IPL 2026
 6. MI Full Team Player List IPL 2026
 7. RCB Full Team Player List IPL 2026
 8. CSK Full Team Player List IPL 2026
 9. DC Full Team Player List IPL 2026
10. GT Full Team Player List IPL 2026

================================================================================
```

---

## 🔧 Core Functions

### `get_genre_input() -> str`
Displays available genres and prompts user for selection. Returns the selected genre key.

### `fetch_page(url: str) -> str | None`
Fetches webpage content with error handling for timeouts, connection errors, and HTTP failures.

### `parse_headlines(html_content: str, limit: int) -> list[str]`
Extracts actual news headlines from HTML, filtering out category headers and promotional content. Tries multiple CSS selectors to adapt to different page structures.

### `clean_headline(text: str) -> str`
Removes dates, category prefixes, and artifacts from raw headline text using regex patterns.

### `is_category_header(text: str) -> bool`
Identifies and filters out category headers, navigation links, and promotional content.

### `check_robots_txt(url: str) -> dict`
Verifies scraping permissions by checking the website's `robots.txt` file.

### `print_headlines(headlines: list[str], genre: str) -> None`
Displays headlines in a formatted, user-friendly layout.

---

## ⚙️ Configuration

All configurable settings are at the top of the script:

```python
TOI_BASE_URL = "https://timesofindia.indiatimes.com"
REQUEST_TIMEOUT = 10                    # Seconds before timeout
HEADLINE_LIMIT = 10                     # Max headlines to display
MIN_HEADLINE_LENGTH = 15                # Minimum headline characters
MAX_HEADLINE_LENGTH = 300               # Maximum headline characters
```

### Custom User Agent

The script uses a Chrome browser header to avoid blocks:

```python
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36..."
}
```

---

## 🛡️ Ethical Scraping Practices

This scraper follows responsible web scraping guidelines:

- ✅ **Robots.txt Compliance** - Checks and respects `/robots.txt` directives
- ✅ **Rate Limiting** - Uses reasonable request timeouts (10 seconds)
- ✅ **User Agent** - Identifies as a real browser
- ✅ **Non-Commercial** - Intended for personal/educational use
- ✅ **Light Load** - Fetches only 10 headlines per request

**Note**: Always verify that scraping is permitted by the website's terms of service and robots.txt before using this tool.

---

## 🐛 Troubleshooting

### ❌ "No headlines found" Error

**Solution**: The website structure may have changed. Try:
1. Verify your internet connection
2. Check if the website is accessible in your browser
3. Update CSS selectors in `HEADLINE_SELECTORS` if TOI changes their HTML structure

### ❌ HTTP 403 Error (Forbidden)

**Solution**: The website may be blocking automated requests. Try:
1. Add a delay between requests (modify the code)
2. Use a VPN if geographically restricted
3. Check if robots.txt disallows that path

### ❌ Request Timeout

**Solution**: The server is slow to respond. Try:
1. Increase `REQUEST_TIMEOUT` value in the configuration
2. Check your internet connection
3. Try again in a few moments

### ❌ ModuleNotFoundError

**Solution**: Install missing dependencies:

```bash
pip install -r requirements.txt
```

---

## 📝 Code Structure

```
version5.py
├── Configuration & Constants
│   ├── URLs & Headers
│   └── Genre Definitions
├── Utility Functions
│   ├── Input/Output Functions
│   ├── Web Fetching
│   ├── HTML Parsing
│   ├── Text Cleaning
│   └── Validation Functions
└── Main Execution
    └── User Interaction Flow
```

---

## 🔄 How It Works

```
1. Display Menu
   ↓
2. Get User Input (Genre)
   ↓
3. Check robots.txt
   ↓
4. Fetch Webpage
   ↓
5. Parse HTML with BeautifulSoup
   ↓
6. Extract & Clean Headlines
   ↓
7. Filter Category Headers
   ↓
8. Display Top 10 Headlines
```

---

## 📚 Libraries Used

| Library | Purpose |
|---------|---------|
| **requests** | HTTP requests and page fetching |
| **BeautifulSoup4** | HTML parsing and CSS selectors |
| **re** | Regular expressions for text cleaning |
| **sys** | System-level operations |
| **urllib.parse** | URL parsing utilities |

---

## 🚨 Legal & Ethical Considerations

- **Terms of Service**: Always respect the website's ToS
- **Robots.txt**: This tool checks and respects robots.txt rules
- **Rate Limiting**: Use responsibly; don't flood the server
- **Attribution**: If publishing data, credit Times of India
- **Educational Use**: Intended for learning web scraping concepts

---

## 🤝 Contributing

Found a bug or have suggestions? Consider:

1. Checking if the issue is a website structure change
2. Updating CSS selectors in `HEADLINE_SELECTORS`
3. Modifying `CATEGORY_HEADERS` if new headers appear

---

## 📄 License

This project is provided as-is for educational purposes. Use responsibly and respect website terms of service.

---

## ✨ Future Enhancements

Potential improvements for future versions:

- 📁 **Export to CSV/JSON** - Save headlines to files
- 🔄 **Scheduled Scraping** - Automated periodic updates
- 🎨 **GUI Interface** - Tkinter-based graphical interface
- 💾 **Database Integration** - Store headlines in SQLite/PostgreSQL
- 🔐 **Proxy Support** - Handle IP blocking with proxies
- 🌍 **Multi-Language** - Support for different TOI language editions
- 📧 **Email Notifications** - Digest of headlines via email

---

## 👨‍💻 Author

**Arham Shah | Engineering Student | Web Scraping Enthusiast**

Built for learning web scraping, HTML parsing, and API interaction in Python.

---

## 📧 Support

If you encounter issues:

1. Check the **Troubleshooting** section above
2. Verify your Python version (3.10+)
3. Ensure all dependencies are installed
4. Check your internet connection
5. Verify the website is accessible

---

**Happy Scraping! 🎉**
