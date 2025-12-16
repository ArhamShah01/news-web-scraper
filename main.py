"""
Times of India Headlines Scraper with Genre Selection

Scrapes top 10 ACTUAL news headlines from Times of India for selected genres.
FIXED VERSION - Corrected URLs and selectors for all genres.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import sys
import re

# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

TOI_BASE_URL = "https://timesofindia.indiatimes.com"
ROBOTS_TXT_URL = f"{TOI_BASE_URL}/robots.txt"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": TOI_BASE_URL,
}

REQUEST_TIMEOUT = 10
HEADLINE_LIMIT = 10

# GENRE CONFIGURATION - FIXED URLs
GENRES = {
    'home': {
        'name': 'Home (All News)',
        'url': f"{TOI_BASE_URL}/home/headlines"
    },
    'sports': {
        'name': 'Sports',
        'url': f"{TOI_BASE_URL}/sports/"
    },
    'business': {
        'name': 'Business',
        'url': f"{TOI_BASE_URL}/business/"
    },
    'tech': {
        'name': 'Technology',
        'url': f"{TOI_BASE_URL}/technology"
    },
    'entertainment': {
        'name': 'Entertainment',
        'url': f"{TOI_BASE_URL}/etimes"
    },
    'india': {
        'name': 'India',
        'url': f"{TOI_BASE_URL}/india/"
    },
    'world': {
        'name': 'World',
        'url': f"{TOI_BASE_URL}/world/"
    },
    'health': {
        'name': 'Health',
        'url': f"{TOI_BASE_URL}/life-style/health-fitness"
    },
    'life': {
        'name': 'Life & Style',
        'url': f"{TOI_BASE_URL}/life-style"
    },
    'education': {
        'name': 'Education',
        'url': f"{TOI_BASE_URL}/education/"
    }
}

# CRITICAL: Target ACTUAL news headline links, not category headers
# These selectors target anchor tags that link to articles
HEADLINE_SELECTORS = [
    "a[data-test='headline_link']",          # TOI's data attribute for articles
    "h2.eachStory a",                        # TOI story headlines
    "h2 a[href*='articleshow']",             # Article links in h2
    "a.news_link",                           # Common article link class
    "a[href*='/articleshow/']",              # Direct article URLs
    ".topstories a",                         # Top stories section
    "a[itemprop='url']",                     # Schema.org markup
    ".list-item h2 a",                       # List item articles
]

MIN_HEADLINE_LENGTH = 15  # Minimum headline length
MAX_HEADLINE_LENGTH = 300  # Maximum headline length

# Common category headers to EXCLUDE
CATEGORY_HEADERS = {
    'METRO CITIES', 'ENTERTAINMENT', 'LIFE & STYLE', 'MOST POPULAR',
    'TOP PHOTOSTORIES', 'PHOTO GALLERY', 'FROM OUR NETWORK',
    'TOI TIMESPOINTS', 'VISIT TOI DAILY & EARN TIMES POINTS',
    'CITIES', 'INDIA', 'WORLD', 'BUSINESS', 'SPORTS', 'HEALTH',
    'TV', 'WEB STORIES', 'VIRAL', 'TRENDING', 'INTERNATIONAL BUSINESS',
    'LATEST BUSINESS VIDEOS', 'PERSONAL FINANCE', 'BANKING SERVICES',
    'POPULAR BANKS IFSC CODES', 'STOCK MARKET TODAY', 'TOP STOCKS TODAY',
    'POPULAR SPORTS STORIES', 'POPULAR INDIA STORIES', 'POPULAR WORLD STORIES'
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def display_genres() -> None:
    """Display available genres for user selection."""
    print(f"\n{'='*80}")
    print("📚 Available Genres:")
    print(f"{'='*80}\n")
    for i, (key, details) in enumerate(GENRES.items(), 1):
        print(f"{i:2d}. {details['name']:25s} ('{key}')")
    print(f"\n{'='*80}\n")

def get_genre_input() -> str:
    """Get genre input from user."""
    display_genres()
    while True:
        user_input = input("Enter genre name or number (e.g., 'sports' or '1'): ").strip().lower()
        
        # Check if input is a number
        try:
            num = int(user_input)
            genre_keys = list(GENRES.keys())
            if 1 <= num <= len(genre_keys):
                return genre_keys[num - 1]
            else:
                print(f"❌ Invalid number. Please enter a number between 1 and {len(GENRES)}")
                continue
        except ValueError:
            pass
        
        # Check if input is a valid genre name
        if user_input in GENRES:
            return user_input
        else:
            print(f"❌ Invalid genre '{user_input}'. Please try again.")
            print(f" Valid genres: {', '.join(GENRES.keys())}")

def is_category_header(text: str) -> bool:
    """
    Check if text is a category header rather than a news headline.
    
    Args:
        text (str): Text to check
    
    Returns:
        bool: True if text is likely a category header
    """
    text_upper = text.upper().strip()
    
    # Check if it matches known category headers
    if text_upper in CATEGORY_HEADERS:
        return True
    
    # Check if it's all caps and short (typical of category headers)
    if text_upper == text and len(text) < 50 and len(text.split()) <= 4:
        return True
    
    # Check for promotional content
    if any(promo in text.lower() for promo in ['earn times points', 'daily &', 'follow us', 'see more']):
        return True
    
    # Check for navigation links
    if any(nav in text.lower() for nav in ['subscribe', 'sign in', 'log in', 'download app']):
        return True
    
    return False

def clean_headline(text: str) -> str:
    """
    Clean up headline text by removing artifacts.
    
    Args:
        text (str): Raw headline text
    
    Returns:
        str: Cleaned headline text
    """
    text = text.strip()
    if not text:
        return text
    
    # Remove date patterns like "/ Dec 16, 2025"
    text = re.sub(r'/\s*[A-Za-z]+\s+\d{1,2},\s*\d{4}', '', text).strip()
    
    # Remove category prefixes like "Sports / " or "India / "
    text = re.sub(r'^[A-Za-z\s]+/\s*', '', text).strip()
    
    # Remove "MORE" artifacts
    if "MORE" in text.upper():
        text_normalized = re.sub(r'MORE', '|', text, flags=re.IGNORECASE)
        parts = [p.strip() for p in text_normalized.split('|') if p.strip()]
        valid_parts = [p for p in parts if len(p) > 10 and len(p) < 250]
        if valid_parts:
            text = max(valid_parts, key=len)
    
    # Remove trailing "NEWS"
    text = re.sub(r'\s+NEWS\s*$', '', text, flags=re.IGNORECASE).strip()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def check_robots_txt(url: str) -> dict:
    """Check robots.txt compliance."""
    try:
        robots_response = requests.get(ROBOTS_TXT_URL, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        robots_response.raise_for_status()
        robots_text = robots_response.text
        
        parsed_url = urlparse(url)
        path = parsed_url.path
        
        if "User-agent: *" in robots_text:
            lines = robots_text.split('\n')
            in_wildcard_section = False
            
            for line in lines:
                line = line.strip()
                
                if line.startswith("User-agent: *"):
                    in_wildcard_section = True
                elif line.startswith("User-agent:") and not line.startswith("User-agent: *"):
                    in_wildcard_section = False
                
                if in_wildcard_section and line.startswith("Disallow:"):
                    disallowed_path = line.replace("Disallow:", "").strip()
                    if disallowed_path and path.startswith(disallowed_path):
                        return {
                            'allowed': False,
                            'message': f"Path '{path}' is disallowed by robots.txt"
                        }
        
        return {
            'allowed': True,
            'message': "Path is allowed by robots.txt"
        }
    
    except requests.RequestException as e:
        return {
            'allowed': True,
            'message': f"Could not verify robots.txt: {str(e)} (proceeding cautiously)"
        }

def fetch_page(url: str) -> str | None:
    """Fetch webpage with error handling."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.text
    except requests.Timeout:
        print(f"❌ Error: Request timed out after {REQUEST_TIMEOUT} seconds")
        return None
    except requests.ConnectionError:
        print("❌ Error: Network connection failed.")
        return None
    except requests.HTTPError as e:
        print(f"❌ Error: HTTP {e.response.status_code}")
        return None
    except requests.RequestException as e:
        print(f"❌ Error: {str(e)}")
        return None

def parse_headlines(html_content: str, limit: int = HEADLINE_LIMIT) -> list[str]:
    """
    Parse ACTUAL news headlines from HTML (not category headers).
    
    Args:
        html_content (str): Raw HTML content
        limit (int): Maximum number of headlines to extract
    
    Returns:
        list[str]: List of cleaned headlines
    """
    headlines = []
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
    except Exception as e:
        print(f"❌ Error: Failed to parse HTML - {str(e)}")
        return headlines
    
    # Try each selector to find article links
    for selector in HEADLINE_SELECTORS:
        try:
            elements = soup.select(selector)
            if elements:
                for element in elements:
                    if len(headlines) >= limit:
                        break
                    
                    # Get text content
                    text = element.get_text(separator=" ", strip=True)
                    text = clean_headline(text)
                    
                    # FILTER OUT: Category headers and invalid text
                    if is_category_header(text):
                        continue
                    
                    if MIN_HEADLINE_LENGTH <= len(text) <= MAX_HEADLINE_LENGTH:
                        if text not in headlines:
                            headlines.append(text)
                
                if len(headlines) >= limit:
                    break
        
        except Exception:
            continue
    
    return headlines[:limit]

def print_headlines(headlines: list[str], genre: str) -> None:
    """Print headlines in clean format."""
    if not headlines:
        print("\n⚠️ No headlines found. The website structure may have changed.")
        return
    
    genre_name = GENRES[genre]['name']
    print(f"\n{'='*80}")
    print(f"📰 Times of India - {genre_name} (Top {len(headlines)} Headlines)")
    print(f"{'='*80}\n")
    
    for i, headline in enumerate(headlines, 1):
        print(f"{i:2d}. {headline}")
    
    print(f"\n{'='*80}\n")

def main() -> int:
    """Main execution function."""
    print("🔍 Times of India Headlines Scraper with Genre Selection")
    
    # Get genre input from user
    genre = get_genre_input()
    genre_name = GENRES[genre]['name']
    genre_url = GENRES[genre]['url']
    
    print(f"\n✨ Selected Genre: {genre_name}")
    print(f"📍 Target: {genre_url}\n")
    
    print("📋 Checking robots.txt compliance...")
    robots_check = check_robots_txt(genre_url)
    print(f" └─ {robots_check['message']}")
    
    if not robots_check['allowed']:
        print("\n⚠️ Scraping disallowed by robots.txt. Aborting.\n")
        return 1
    
    print("\n📥 Fetching webpage...")
    html_content = fetch_page(genre_url)
    
    if html_content is None:
        print("\n❌ Failed to fetch webpage.\n")
        return 1
    
    print(" └─ ✅ Webpage fetched successfully")
    
    print("\n🔎 Parsing headlines...")
    headlines = parse_headlines(html_content, HEADLINE_LIMIT)
    
    if headlines:
        print(f" └─ ✅ Found {len(headlines)} headlines")
    else:
        print(" └─ ⚠️ No headlines found")
    
    print_headlines(headlines, genre)
    
    return 0 if headlines else 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⛔ Scraping interrupted by user.\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}\n")
        sys.exit(1)
