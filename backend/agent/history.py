# backend/agent/history.py
from typing import Dict, List, Any
import time

# Simple in-memory storage for chat history
# In a production app, you'd use a database instead
chat_histories = {}

def save_research_query(user_id: str, query: str, results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Save a research query and its results to the chat history
    Args:
        user_id: Identifier for the user (can be a session ID)
        query: The research query
        results: The research results
    Returns:
        The saved history entry with timestamp
    """
    if user_id not in chat_histories:
        chat_histories[user_id] = []
    
    # Create history entry
    entry = {
        "id": f"query_{int(time.time())}",
        "timestamp": time.time(),
        "query": query,
        "results": results
    }
    
    # Add to history
    chat_histories[user_id].append(entry)
    
    return entry

def get_user_history(user_id: str) -> List[Dict[str, Any]]:
    """
    Get all history entries for a user
    Args:
        user_id: Identifier for the user
    Returns:
        List of history entries, sorted by timestamp (newest first)
    """
    if user_id not in chat_histories:
        return []
    
    # Sort by timestamp, newest first
    sorted_history = sorted(
        chat_histories[user_id], 
        key=lambda x: x["timestamp"], 
        reverse=True
    )
    
    return sorted_history

def clear_user_history(user_id: str) -> bool:
    """
    Clear all history for a user
    Args:
        user_id: Identifier for the user
    Returns:
        True if history was cleared, False if user had no history
    """
    if user_id in chat_histories:
        chat_histories[user_id] = []
        return True
    return False