import requests
from typing import List,Dict,Any,Optional,Set
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re



def getPage(url : str) -> Optional[BeautifulSoup]:
    try:
        response = requests.get(url,timeout=15,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        response.raise_for_status()

        return BeautifulSoup(response.content,'html.parser')
    except Exception as e:
        print(f"Error while parsing the url to bs4 : {e}")
        return None

def getPageText(url : str)-> Optional[str]:
    soup = getPage(url)

    if not soup:
        return None

    mainContent = soup.find('main') or soup.find(role='main')

    if mainContent:
        text = mainContent.get_text(separator='\n',strip=True)
    else:
        text = soup.body.get_text(separator='\n',strip=True)
    
    return re.sub(r'\n\s*\n' , '\n\n' , text)


def getProducts(url : str) -> List[Dict[str,Any]]:

    try:
        productUrl = f"{url.rstrip('/')}/products.json"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(productUrl,timeout=15,headers=headers)
        response.raise_for_status()

        data = response.json()

        if "products" in data and isinstance(data['products'],List):
            if not data['products']:
                print(f"Request successful but product is empty")
            return data['products']
        else:
            raise ValueError("Products not found")
    except Exception as e:
        print(f"Error while fetching data from the url : {e}" )
        raise


def socialLinks(soup : BeautifulSoup,url : str) -> Dict[str,str]:
    social_handles = {}
    social_patterns = {
        'instagram': r'instagram\.com/([a-zA-Z0-9_\.]+)',
        'facebook': r'facebook\.com/([a-zA-Z0-9_\.]+)',
        'tiktok': r'tiktok\.com/@([a-zA-Z0-9_\.]+)',
        'twitter': r'twitter\.com/([a-zA-Z0-9_]+)',
        'youtube': r'youtube\.com/(user/|channel/|@)?([a-zA-Z0-9_\-]+)'
    }
    
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        for platform, pattern in social_patterns.items():
            if platform not in social_handles: # Find first one for each platform
                match = re.search(pattern, href)
                if match:
                    social_handles[platform] = urljoin(url, href)

    return social_handles

def findContactDetails(soup: BeautifulSoup) -> Dict[str, List[str]]:
    text = soup.get_text()
    emails = list(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)))
    
    # Simple regex for phone numbers, can be improved for international formats
    phone_numbers = list(set(re.findall(r'\(?\+?[0-9\s\-\(\)]{8,}[0-9]', text)))
    
    return {"emails": emails, "phone_numbers": phone_numbers}

def find_policy_and_important_links(soup: BeautifulSoup, base_url: str) -> Dict[str, Optional[str]]:
    links = {}
    link_keywords = {
        'privacy_policy': ['privacy', 'policy'],
        'refund_policy': ['refund', 'return'],
        'about_us': ['about'],
        'contact_us': ['contact'],
        'faqs': ['faq', 'frequently asked questions'],
        'blogs': ['blog'],
        'track_order': ['track', 'order']
    }
    
    for key, keywords in link_keywords.items():
        if key not in links:
            for a_tag in soup.find_all('a', href=True):
                link_text = a_tag.get_text(strip=True).lower()
                if any(keyword in link_text for keyword in keywords):
                    links[key] = urljoin(base_url, a_tag['href'])
                    break 
    
    return links

def scrape_all_insights(store_url: str) -> Dict[str, Any]:
    insights = {
        'product_catalog': [],
        'social_handles': {},
        'contact_details': {},
        'important_links': {}
    }
    
    try:
        insights['product_catalog'] = getProducts(store_url)
    except Exception as e:
        print(f"Could not fetch product catalog: {e}")

    soup = getPage(store_url)
    if not soup:
        return insights 

    insights['social_handles'] = socialLinks(soup, store_url)
    insights['contact_details'] = findContactDetails(soup)
    
    important_links = find_policy_and_important_links(soup, store_url)
    insights['important_links'] = important_links # Store the found links
    
    for key, link_url in important_links.items():
        if link_url:
            print(f"Fetching content for: {key} ({link_url})")
            insights[f'{key}_content'] = getPageText(link_url)

    return insights

def isShopify(url : str) -> bool:
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url,timeout=15,headers=headers)
        response.raise_for_status()

        content = response.text

        #add checks to see if this store is in shopify..
        if "Shopify.theme" in content or "cdn.shopify.com" in content:
            print(f"This is a shopify store")
            return True
        else:
            print(f"This is not a shopify store")
            return False
    except requests.exceptions.RequestException:
        print(f"Could not open the url.")
        return False

# test = "https://hairoriginals.com"

# products = getProducts(test)

# for p in products:
#     print(p['title'])