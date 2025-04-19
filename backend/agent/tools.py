# backend/agent/tools.py
import json
import requests
from typing import List, Dict, Any, Optional
from config import SERPER_API_KEY, GROQ_API_KEY, AVAILABLE_MODELS, DEFAULT_MODEL, GROQ_API_URL
import time
from datetime import datetime

# Rate limiting variables
LAST_REQUEST_TIME = 0
RATE_LIMIT_DELAY = 1.0  # Minimum seconds between requests
MAX_RETRIES = 3
RETRY_DELAY = 5.0  # Seconds to wait after rate limit error


def search_web(query: str, num_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search the web using Serper API
    
    Args:
        query: Search query string
        num_results: Number of results to return
        
    Returns:
        List of search result dictionaries
    """
    try:
        url = "https://google.serper.dev/search"
        payload = json.dumps({
            "q": query,
            "num": num_results
        })
        headers = {
            'X-API-KEY': SERPER_API_KEY,
            'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()
        
        search_results = response.json()
        
        # Extract and format the search results
        formatted_results = []
        if "organic" in search_results:
            for result in search_results["organic"][:num_results]:
                formatted_results.append({
                    "title": result.get("title", ""),
                    "link": result.get("link", ""),
                    "snippet": result.get("snippet", ""),
                    "source": "google"
                })
                
        return formatted_results
    
    except Exception as e:
        print(f"Error in search_web: {str(e)}")
        return []





def query_llm(prompt: str, system_prompt: str = None, model: str = None) -> str:
    """
    Query an LLM using Groq API with rate limiting and retry logic
    
    Args:
        prompt: User prompt
        system_prompt: Optional system prompt
        model: LLM model to use (from available models in config)
        
    Returns:
        Model response as string or error message
    """
    global LAST_REQUEST_TIME
    
    if not model or model not in AVAILABLE_MODELS:
        model = DEFAULT_MODEL
    
    # Rate limiting
    elapsed = time.time() - LAST_REQUEST_TIME
    if elapsed < RATE_LIMIT_DELAY:
        time.sleep(RATE_LIMIT_DELAY - elapsed)
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": []
    }
    
    if system_prompt:
        payload["messages"].append({
            "role": "system",
            "content": system_prompt
        })
    
    payload["messages"].append({
        "role": "user",
        "content": prompt
    })
    
    for attempt in range(MAX_RETRIES):
        try:
            LAST_REQUEST_TIME = time.time()
            response = requests.post(
                GROQ_API_URL,
                headers=headers,
                json=payload,
                timeout=30  # 30-second timeout
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:  # Rate limited
                retry_after = float(response.headers.get('Retry-After', RETRY_DELAY))
                print(f"Rate limited. Waiting {retry_after} seconds (attempt {attempt + 1}/{MAX_RETRIES})")
                time.sleep(retry_after)
                continue
            print(f"HTTP Error in query_llm: {str(e)}")
            return f"HTTP Error: {str(e)}"
            
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            return f"Request Error: {str(e)}"
            
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return f"Error: {str(e)}"
    
    return "Error: Max retries reached. Please try again later."


def extract_information(text: str, schema: Dict[str, Any], model: str = None) -> Dict[str, Any]:
    """
    Extract structured information from text based on a schema
    
    Args:
        text: Text to extract information from
        schema: Dictionary defining the expected structure
        model: LLM model to use
        
    Returns:
        Dictionary of extracted information
    """
    # For simplicity, we'll use the LLM to extract information
    schema_str = json.dumps(schema, indent=2)
    
    prompt = f"""
    Extract information from the following text according to this JSON schema:
    
    {schema_str}
    
    Text:
    {text}
    
    Return only a valid JSON object that follows the schema exactly.
    """
    
    response = query_llm(prompt, model=model)
    
    try:
        # Try to parse the response as JSON
        extracted_info = json.loads(response)
        return extracted_info
    except json.JSONDecodeError:
        # If parsing fails, return a simple error structure
        return {"error": "Failed to extract structured information", "raw_text": response}
