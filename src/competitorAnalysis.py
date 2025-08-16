import re
from urllib.parse import urlparse
from googlesearch import search

# logic:
# get the competitor list from google,
#gather insights of the brand 
#use LLMs to compare the results and output a final result

def get_brand_name_from_url(url: str) -> str:
    try:
        hostname = urlparse(url).hostname
        if hostname:
            parts = hostname.replace('www.', '').split('.')
            if len(parts) > 1:
                return parts[0] # Return the name
    except Exception:
        pass
    return "No brand found"

def is_valid_competitor_url(url: str, original_domain: str) -> bool:
    if not url or not url.startswith('http'):
        return False

    try:
        domain = urlparse(url).hostname
        if not domain:
            return False

        if original_domain in domain:
            return False


        return True
    except Exception:
        return False
    
def find_competitors(brand_url: str, num_results: int = 3) -> list[str]:

    brand_name = get_brand_name_from_url(brand_url)
    original_domain = urlparse(brand_url).hostname

    query = f"online stores like {brand_name}"
    print(f"Searching for competitors with query: '{query}'")

    competitor_urls = []
    

    #code breaking :
    #add a checker to see if the competitor store is in shopiffy or not,
    #cant scrape non shopify stores
    
    try:
        for url in search(query):
            if is_valid_competitor_url(url, original_domain):
                # Add to list if it's a valid and unique domain
                domain = urlparse(url).hostname
                if domain not in [urlparse(c).hostname for c in competitor_urls]:
                    competitor_urls.append(url)
            
            # Stop once we have enough results
            if len(competitor_urls) >= num_results:
                break
                
    except Exception as e:
        print(f"An error occurred during web search: {e}")

    print(f"Found competitors: {competitor_urls}")
    return competitor_urls