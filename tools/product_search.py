import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()

def search_products(query: str, site: str = "amazon.com") -> str:
    """Search for products on specified shopping site."""
    try:
        search = GoogleSearch({
            "q": f"site:{site} {query}",
            "api_key": os.getenv("SERPAPI_API_KEY"),
            "engine": "google",
            "num": 5  # Number of results to return
        })
        
        results = search.get_dict()
        
        if "organic_results" not in results:
            return f"No products found on {site}"
        
        formatted_results = []
        for result in results["organic_results"][:5]:
            title = result.get("title", "No title")
            link = result.get("link", "No link")
            snippet = result.get("snippet", "No description")
            
            formatted_results.append(
                f"- {title}\n  Price: Check {site}\n  Link: {link}\n  Description: {snippet}"
            )
        
        return "\n\n".join(formatted_results)
    
    except Exception as e:
        return f"Error searching products: {str(e)}"
