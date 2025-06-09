import requests
import json
from typing import List, Dict, Optional, Any
from urllib.parse import urlparse, quote_plus
import os

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not installed, skip
    pass


# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not installed, skip
    pass


class WebSearchAPI:
    """Web search API wrapper using SerpApi with robust fallbacks."""
    
    def __init__(self):
        """Initialize web search client."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        # API key should be set as environment variable: SERPAPI_KEY
        self.api_key = os.getenv('SERPAPI_KEY')
        
        # Try to import SerpApi library
        self.serpapi_available = self._check_serpapi_library()
    
    def _check_serpapi_library(self) -> bool:
        """Check if SerpApi library is available."""
        try:
            import serpapi
            self.serpapi = serpapi
            return True
        except ImportError:
            try:
                from serpapi import GoogleSearch
                self.GoogleSearch = GoogleSearch
                return True
            except ImportError:
                return False
    
    def search_serpapi_library(self, query: str, max_results: int = 10, engine: str = "google") -> List[Dict[str, str]]:
        """
        Search using SerpApi official library.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            engine: Search engine (google, bing, duckduckgo, etc.)
            
        Returns:
            List of search results with title, link, and snippet
        """
        if not self.api_key:
            return [{'error': "SerpApi API key not found. Set SERPAPI_KEY environment variable or get a free key from https://serpapi.com/"}]
        
        if not self.serpapi_available:
            return [{'error': "SerpApi library not installed. Install with: pip install serpapi"}]
        
        try:
            # Try new serpapi library first
            if hasattr(self, 'serpapi'):
                client = self.serpapi.Client(api_key=self.api_key)
                data = client.search({
                    'engine': engine,
                    'q': query,
                    'num': min(max_results, 20)
                })
            else:
                # Use legacy google-search-results library
                search = self.GoogleSearch({
                    "engine": engine,
                    "q": query,
                    "api_key": self.api_key,
                    "num": min(max_results, 20)
                })
                data = search.get_dict()
            
            # Check for API errors
            if 'error' in data:
                return [{'error': f"SerpApi error: {data['error']}"}]
            
            results = []
            
            # Extract organic results
            organic_results = data.get('organic_results', [])
            for result in organic_results[:max_results]:
                results.append({
                    'title': result.get('title', 'No title'),
                    'link': result.get('link', ''),
                    'snippet': result.get('snippet', ''),
                    'source': f'SerpApi ({engine.title()})',
                    'position': result.get('position', 0)
                })
            
            # If no organic results, check for answer box or knowledge graph
            if not results:
                # Check answer box
                answer_box = data.get('answer_box')
                if answer_box:
                    results.append({
                        'title': answer_box.get('title', query),
                        'link': answer_box.get('link', ''),
                        'snippet': answer_box.get('answer', answer_box.get('snippet', '')),
                        'source': f'SerpApi ({engine.title()}) - Answer Box',
                        'position': 0
                    })
                
                # Check knowledge graph
                knowledge_graph = data.get('knowledge_graph')
                if knowledge_graph:
                    results.append({
                        'title': knowledge_graph.get('title', query),
                        'link': knowledge_graph.get('website', ''),
                        'snippet': knowledge_graph.get('description', ''),
                        'source': f'SerpApi ({engine.title()}) - Knowledge Graph',
                        'position': 0
                    })
            
            if not results:
                return [{'error': f"No search results found for query: {query}"}]
            
            return results
            
        except Exception as e:
            return [{'error': f"SerpApi library error: {str(e)}"}]
    
    def search_serpapi_requests(self, query: str, max_results: int = 10, engine: str = "google") -> List[Dict[str, str]]:
        """
        Search using SerpApi via direct HTTP requests (fallback).
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            engine: Search engine (google, bing, duckduckgo, etc.)
            
        Returns:
            List of search results with title, link, and snippet
        """
        if not self.api_key:
            return [{'error': "SerpApi API key not found. Set SERPAPI_KEY environment variable or get a free key from https://serpapi.com/"}]
        
        try:
            params = {
                'engine': engine,
                'q': query,
                'api_key': self.api_key,
                'num': min(max_results, 20),
                'output': 'json'
            }
            
            response = self.session.get("https://serpapi.com/search", params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Check for API errors
            if 'error' in data:
                return [{'error': f"SerpApi error: {data['error']}"}]
            
            results = []
            
            # Extract organic results
            organic_results = data.get('organic_results', [])
            for result in organic_results[:max_results]:
                results.append({
                    'title': result.get('title', 'No title'),
                    'link': result.get('link', ''),
                    'snippet': result.get('snippet', ''),
                    'source': f'SerpApi ({engine.title()})',
                    'position': result.get('position', 0)
                })
            
            if not results:
                return [{'error': f"No search results found for query: {query}"}]
            
            return results
            
        except requests.exceptions.RequestException as e:
            return [{'error': f"SerpApi request failed: {str(e)}"}]
        except json.JSONDecodeError:
            return [{'error': "Invalid JSON response from SerpApi"}]
        except Exception as e:
            return [{'error': f"SerpApi search error: {str(e)}"}]
    
    def search_fallback_bing(self, query: str, max_results: int = 10) -> List[Dict[str, str]]:
        """
        Fallback search using Bing search (no API key required).
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            List of search results
        """
        try:
            from bs4 import BeautifulSoup
            
            # Bing search URL
            search_url = f"https://www.bing.com/search?q={quote_plus(query)}&count={min(max_results, 50)}"
            
            response = self.session.get(search_url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            results = []
            
            # Bing search results structure
            result_items = soup.find_all('li', class_='b_algo')
            
            for i, item in enumerate(result_items[:max_results], 1):
                title_elem = item.find('h2')
                if title_elem:
                    link_elem = title_elem.find('a')
                    if link_elem:
                        title = link_elem.get_text(strip=True)
                        link = link_elem.get('href', '')
                        
                        # Find snippet
                        snippet = ""
                        snippet_elem = item.find('p') or item.find('div', class_='b_caption')
                        if snippet_elem:
                            snippet = snippet_elem.get_text(strip=True)
                        
                        if title and link:
                            results.append({
                                'title': title,
                                'link': link,
                                'snippet': snippet,
                                'source': 'Bing Fallback',
                                'position': i
                            })
            
            return results if results else [{'error': f"No Bing results found for query: {query}"}]
            
        except ImportError:
            return [{'error': "BeautifulSoup4 library required for fallback search. Install with: pip install beautifulsoup4"}]
        except Exception as e:
            return [{'error': f"Bing fallback failed: {str(e)}"}]
    
    def search_comprehensive_fallback(self, query: str, max_results: int = 10) -> List[Dict[str, str]]:
        """
        Comprehensive fallback search trying multiple sources.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            List of search results
        """
        # Try Bing fallback
        results = self.search_fallback_bing(query, max_results)
        if results and 'error' not in results[0]:
            return results
        
        # If all else fails, create synthetic results with helpful guidance
        return [{
            'title': f"Search guidance for: {query}",
            'link': f"https://www.google.com/search?q={quote_plus(query)}",
            'snippet': f"Try searching for '{query}' on Google, Bing, or DuckDuckGo. You can also try more specific keywords or check if the terms are spelled correctly.",
            'source': 'Search Guidance',
            'position': 1
        }, {
            'title': f"Alternative search: {query} tutorial",
            'link': f"https://www.youtube.com/results?search_query={quote_plus(query + ' tutorial')}",
            'snippet': f"Consider searching for '{query} tutorial' or '{query} guide' on YouTube or educational platforms for comprehensive learning materials.",
            'source': 'Search Suggestions',
            'position': 2
        }]


# Global web search instance
web_search_api = WebSearchAPI()


def search_web(query: str, max_results: int = 10, engine: str = "google") -> str:
    """
    Search the web for information about a query using SerpApi with robust fallbacks.

    Args:
        query (str): The search query
        max_results (int): Maximum number of results to return (default: 10)
        engine (str): Search engine to use (google, bing, duckduckgo, etc.)

    Returns:
        str: Formatted search results or error message
    """
    if not query.strip():
        return "Error: Search query cannot be empty"
    
    if max_results < 1 or max_results > 50:
        max_results = 10
    
    try:
        # Try SerpApi library first
        if web_search_api.api_key:
            results = web_search_api.search_serpapi_library(query, max_results, engine)
            
            # If library method fails, try direct requests
            if results and 'error' in results[0] and 'library not installed' in results[0]['error']:
                results = web_search_api.search_serpapi_requests(query, max_results, engine)
        else:
            results = [{'error': "SerpApi API key not found"}]
        
        # If SerpApi fails, try fallback
        if results and 'error' in results[0]:
            if 'API key not found' in results[0]['error']:
                results = web_search_api.search_comprehensive_fallback(query, max_results)
            else:
                # For other SerpApi errors, still try fallback
                fallback_results = web_search_api.search_comprehensive_fallback(query, max_results)
                if fallback_results and 'error' not in fallback_results[0]:
                    results = fallback_results
        
        if not results:
            return f"No search results found for: {query}"
        
        if results and 'error' in results[0]:
            return f"Search error: {results[0]['error']}"
        
        # Format results
        formatted_results = f"Search results for: '{query}'\n"
        formatted_results += "=" * 50 + "\n\n"
        
        for i, result in enumerate(results, 1):
            formatted_results += f"{i}. {result['title']}\n"
            formatted_results += f"   🔗 {result['link']}\n"
            if result['snippet']:
                formatted_results += f"   📝 {result['snippet']}\n"
            formatted_results += f"   📊 Source: {result['source']}\n"
            if result.get('position'):
                formatted_results += f"   📍 Position: {result['position']}\n"
            formatted_results += "\n"
        
        return formatted_results
        
    except Exception as e:
        return f"Error performing web search: {str(e)}"


def search_website(query: str, site_url: Optional[str] = None, max_results: int = 10) -> str:
    """
    Search within a specific website or perform general web search.
    
    Args:
        query: Search query
        site_url: Specific website to search within (optional)
        max_results: Maximum number of results
        
    Returns:
        Formatted search results
    """
    if site_url:
        # Search within specific site using site: operator
        site_query = f"site:{site_url} {query}"
        return search_web(site_query, max_results)
    else:
        # General web search
        return search_web(query, max_results)


def fetch_webpage(url: str, extract_text: bool = True) -> Dict[str, Any]:
    """
    Fetch and parse a webpage.
    
    Args:
        url: URL to fetch
        extract_text: Whether to extract text content
        
    Returns:
        Dictionary with webpage data
    """
    try:
        # Validate URL
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            return {"error": "Invalid URL format"}
        
        response = requests.get(url, timeout=15, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()
        
        # Extract basic information
        result = {
            "url": url,
            "status_code": response.status_code,
            "title": "",
            "description": "",
            "text_content": "",
            "content_length": len(response.content)
        }
        
        # Try to parse HTML if BeautifulSoup is available
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title_tag = soup.find('title')
            if title_tag:
                result["title"] = title_tag.get_text(strip=True)
            
            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                result["description"] = meta_desc.get('content', '')
            
            if extract_text:
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                
                # Get text content
                text = soup.get_text()
                # Clean up text
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                result["text_content"] = ' '.join(chunk for chunk in chunks if chunk)[:5000]  # Limit length
        
        except ImportError:
            # If BeautifulSoup not available, return raw content info
            result["text_content"] = "BeautifulSoup4 not available - raw content extraction not supported"
        
        return result
        
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch webpage: {str(e)}"}
    except Exception as e:
        return {"error": f"Error parsing webpage: {str(e)}"}


def get_webpage_text(url: str) -> str:
    """
    Get readable text content from a webpage.
    
    Args:
        url: URL to fetch
        
    Returns:
        Formatted webpage content
    """
    result = fetch_webpage(url, extract_text=True)
    
    if "error" in result:
        return f"Error fetching webpage: {result['error']}"
    
    output = f"Webpage: {result['title']}\n"
    output += f"URL: {result['url']}\n"
    output += f"Status: {result['status_code']}\n"
    output += "=" * 50 + "\n\n"
    
    if result['description']:
        output += f"Description: {result['description']}\n\n"
    
    output += "Content:\n"
    output += result['text_content']
    
    return output


# Example usage and test cases
if __name__ == '__main__':
    test_queries = [
        "Python programming tutorial",
        "machine learning basics", 
        "OpenAI GPT models"
    ]
    
    print("Web Search API Test Results:")
    print("SerpApi Key Status:", "✅ Found" if web_search_api.api_key else "❌ Not Found (will use fallback)")
    print("SerpApi Library:", "✅ Available" if web_search_api.serpapi_available else "❌ Not Installed")
    print()
    
    for query in test_queries:
        print(f"\n{'-' * 60}")
        print(f"Testing query: '{query}'")
        print("-" * 60)
        result = search_web(query, max_results=3)
        print(result)
    
    print(f"\n{'-' * 60}")
    print("Website-specific search test:")
    print("-" * 60)
    result = search_website("list comprehension", "docs.python.org", 3)
    print(result)
    
    print(f"\n{'-' * 60}")
    print("Webpage fetch test:")
    print("-" * 60)
    webpage_result = fetch_webpage("https://httpbin.org/html")
    if "error" not in webpage_result:
        print(f"Title: {webpage_result['title']}")
        print(f"Status: {webpage_result['status_code']}")
        print(f"Content length: {webpage_result['content_length']} bytes")
        print(f"Text preview: {webpage_result['text_content'][:200]}...")
    else:
        print(webpage_result['error'])
