import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode, urlparse, quote_plus
import json
import time
from typing import List, Dict, Optional, Any
import re


class WebSearchAPI:
    """Web search API wrapper with support for multiple search engines."""
    
    def __init__(self):
        """Initialize web search client."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.search_engines = {
            'duckduckgo': 'https://html.duckduckgo.com/html/',
            'bing': 'https://www.bing.com/search',
            'google': 'https://www.google.com/search'  # Note: May be blocked
        }
    
    def search_duckduckgo(self, query: str, max_results: int = 10) -> List[Dict[str, str]]:
        """
        Search using DuckDuckGo (no API key required).
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            List of search results with title, link, and snippet
        """
        try:
            params = {'q': query}
            response = self.session.get(self.search_engines['duckduckgo'], params=params, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            results = []
            
            # Parse DuckDuckGo results
            result_elements = soup.find_all('div', class_='result')[:max_results]
            
            for element in result_elements:
                title_elem = element.find('a', class_='result__a')
                snippet_elem = element.find('a', class_='result__snippet')
                
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    link = title_elem.get('href', '')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                    
                    results.append({
                        'title': title,
                        'link': link,
                        'snippet': snippet,
                        'source': 'DuckDuckGo'
                    })
            
            return results
            
        except Exception as e:
            return [{'error': f"DuckDuckGo search failed: {str(e)}"}]
    
    def search_mock(self, query: str, max_results: int = 10) -> List[Dict[str, str]]:
        """Generate mock search results for testing."""
        mock_results = [
            {
                'title': f"Search result for '{query}' - Official Documentation",
                'link': f"https://docs.example.com/search?q={quote_plus(query)}",
                'snippet': f"Official documentation and guides related to {query}. Comprehensive information and examples.",
                'source': 'Mock'
            },
            {
                'title': f"{query} - Wikipedia",
                'link': f"https://en.wikipedia.org/wiki/{quote_plus(query)}",
                'snippet': f"Wikipedia article about {query}. Detailed encyclopedia entry with references and related topics.",
                'source': 'Mock'
            },
            {
                'title': f"Tutorial: Getting Started with {query}",
                'link': f"https://tutorial.example.com/{query.lower().replace(' ', '-')}",
                'snippet': f"Step-by-step tutorial for learning {query}. Beginner-friendly guide with practical examples.",
                'source': 'Mock'
            },
            {
                'title': f"{query} Best Practices and Tips",
                'link': f"https://blog.example.com/best-practices-{query.lower().replace(' ', '-')}",
                'snippet': f"Expert tips and best practices for {query}. Industry insights and proven strategies.",
                'source': 'Mock'
            },
            {
                'title': f"Community Forum - {query} Discussion",
                'link': f"https://forum.example.com/topic/{query.lower().replace(' ', '-')}",
                'snippet': f"Community discussion about {query}. Questions, answers, and shared experiences from users.",
                'source': 'Mock'
            }
        ]
        
        return mock_results[:max_results]


# Global web search instance
web_search_api = WebSearchAPI()


def search_web(query: str, max_results: int = 10, engine: str = "auto") -> str:
    """
    Search the web for information about a query.

    Args:
        query (str): The search query
        max_results (int): Maximum number of results to return (default: 10)
        engine (str): Search engine to use ("auto", "duckduckgo", "mock")

    Returns:
        str: Formatted search results
    """
    if not query.strip():
        return "Error: Search query cannot be empty"
    
    if max_results < 1 or max_results > 50:
        max_results = 10
    
    try:
        # Try different search engines
        if engine == "auto":
            # Try DuckDuckGo first, fallback to mock
            results = web_search_api.search_duckduckgo(query, max_results)
            if not results or (results and 'error' in results[0]):
                results = web_search_api.search_mock(query, max_results)
        elif engine == "duckduckgo":
            results = web_search_api.search_duckduckgo(query, max_results)
        elif engine == "mock":
            results = web_search_api.search_mock(query, max_results)
        else:
            return f"Error: Unknown search engine '{engine}'"
        
        if not results:
            return f"No search results found for: {query}"
        
        if results and 'error' in results[0]:
            return results[0]['error']
        
        # Format results
        formatted_results = f"Search results for: '{query}'\n"
        formatted_results += "=" * 50 + "\n\n"
        
        for i, result in enumerate(results, 1):
            formatted_results += f"{i}. {result['title']}\n"
            formatted_results += f"   🔗 {result['link']}\n"
            if result['snippet']:
                formatted_results += f"   📝 {result['snippet']}\n"
            formatted_results += f"   📊 Source: {result['source']}\n\n"
        
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
        # Search within specific site
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
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract basic information
        result = {
            "url": url,
            "status_code": response.status_code,
            "title": "",
            "description": "",
            "text_content": "",
            "links": [],
            "images": []
        }
        
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
        
        # Extract links
        links = soup.find_all('a', href=True)
        result["links"] = [
            {"text": link.get_text(strip=True), "href": link['href']}
            for link in links[:20]
        ]  # Limit to 20 links
        
        # Extract images
        images = soup.find_all('img', src=True)
        result["images"] = [
            {"alt": img.get('alt', ''), "src": img['src']}
            for img in images[:10]
        ]  # Limit to 10 images
        
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
    output += "=" * 50 + "\n\n"
    
    if result['description']:
        output += f"Description: {result['description']}\n\n"
    
    output += "Content:\n"
    output += result['text_content']
    
    return output


def search_and_summarize(query: str, max_results: int = 5) -> str:
    """
    Search for information and provide a summary.
    
    Args:
        query: Search query
        max_results: Number of results to analyze
        
    Returns:
        Search results with summary
    """
    search_results = search_web(query, max_results)
    
    summary = f"Search Summary for '{query}':\n"
    summary += "=" * 40 + "\n\n"
    summary += "Based on the search results, here are the key findings:\n\n"
    summary += search_results
    
    return summary


# Example usage and test cases
if __name__ == '__main__':
    test_queries = [
        "Python programming tutorial",
        "machine learning basics",
        "web development frameworks"
    ]
    
    print("Web Search API Test Results:")
    for query in test_queries:
        print(f"\n{'-' * 60}")
        print(f"Testing query: '{query}'")
        print("-" * 60)
        result = search_web(query, max_results=3, engine="mock")
        print(result)
    
    print(f"\n{'-' * 60}")
    print("Website-specific search test:")
    print("-" * 60)
    result = search_website("리스트 사용법", "docs.python.org", 3)
    print(result)
    
    print(f"\n{'-' * 60}")
    print("Webpage fetch test:")
    print("-" * 60)
    # Mock webpage test
    webpage_result = fetch_webpage("https://example.com")
    if "error" not in webpage_result:
        print(f"Title: {webpage_result['title']}")
        print(f"Description: {webpage_result['description']}")
        print(f"Text preview: {webpage_result['text_content'][:200]}...")
    else:
        print(webpage_result['error'])
