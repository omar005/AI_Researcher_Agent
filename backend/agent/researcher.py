# backend/agent/researcher.py (modified)
from typing import Dict, List, Any, Tuple, Optional, TypedDict, Annotated, Callable
import json
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field
from .tools import search_web, query_llm, extract_information
from .prompts import (
    RESEARCHER_SYSTEM_PROMPT,
    SEARCH_PLANNING_PROMPT,
    INFORMATION_SYNTHESIS_PROMPT,
    REFLECTION_PROMPT
)

# Define the state schema as a TypedDict
class ResearchState(TypedDict, total=False):
    query: str
    model: str  # Added model field
    search_queries: List[str]
    search_results: List[Dict[str, Any]]
    draft_research: str
    final_research: str
    status: str
    progress: Dict[str, Any]
    error: Optional[str]

def create_research_agent(progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None):
    """
    Create and return a research agent using LangGraph
    
    Args:
        progress_callback: Optional callback function to report progress
    """
    # Helper function to report progress
    def report_progress(state: ResearchState, step: str, message: str, percent: float) -> None:
        """Report progress through the callback if available"""
        if progress_callback:
            progress_data = {
                "step": step,
                "message": message,
                "percent": percent,
                "query": state.get("query", "")
            }
            state["progress"] = progress_data
            progress_callback(progress_data)

    # Define the graph nodes (steps in the research process)
    def plan_search_queries(state: ResearchState) -> ResearchState:
        """Generate search queries based on the research question"""
        try:
            report_progress(state, "planning", "Planning search queries...", 10)
            
            prompt = SEARCH_PLANNING_PROMPT.format(query=state["query"])
            report_progress(state, "planning", f"Generating optimal search queries using {state.get('model', 'default model')}...", 15)
            
            response = query_llm(prompt, system_prompt=RESEARCHER_SYSTEM_PROMPT, model=state.get("model"))
            
            # Extract search queries from the response
            queries = []
            for line in response.split("\n"):
                if line.strip().startswith("- Search Query"):
                    query_text = line.split(":", 1)[1].strip() if ":" in line else ""
                    if query_text:
                        queries.append(query_text)
            
            if not queries:
                queries = [state["query"]]
            
            report_progress(state, "planning", f"Generated {len(queries)} search queries", 20)    
                
            return {"search_queries": queries, "status": "searching"}
        except Exception as e:
            report_progress(state, "error", f"Error in planning search: {str(e)}", 0)
            return {"error": f"Error in planning search: {str(e)}", "status": "error"}
    
    def execute_searches(state: ResearchState) -> ResearchState:
        """Execute the planned search queries"""
        try:
            all_results = []
            query_count = len(state["search_queries"])
            
            report_progress(state, "searching", f"Starting web searches with {query_count} queries...", 25)
            
            for i, query in enumerate(state["search_queries"]):
                percent = 25 + (i / query_count * 25)  # Progress from 25% to 50%
                report_progress(state, "searching", f"Searching the web [{i+1}/{query_count}]: '{query}'", percent)
                
                results = search_web(query)
                all_results.extend(results)
                
                report_progress(state, "searching", f"Found {len(results)} results for query {i+1}", percent + 5)
            
            report_progress(state, "searching", f"Web search complete. Found {len(all_results)} total results", 50)
            
            return {"search_results": all_results, "status": "synthesizing"}
        except Exception as e:
            report_progress(state, "error", f"Error in executing searches: {str(e)}", 0)
            return {"error": f"Error in executing searches: {str(e)}", "status": "error"}
    
    def synthesize_information(state: ResearchState) -> ResearchState:
        """Synthesize information from search results"""
        try:
            report_progress(state, "synthesizing", "Analyzing search results...", 55)
            
            search_results_text = ""
            result_count = len(state["search_results"])
            
            report_progress(state, "synthesizing", f"Processing {result_count} search results...", 60)
            
            for i, result in enumerate(state["search_results"], 1):
                search_results_text += f"Result {i}:\n"
                search_results_text += f"Title: {result.get('title', 'No title')}\n"
                search_results_text += f"Source: {result.get('link', 'No link')}\n"
                search_results_text += f"Snippet: {result.get('snippet', 'No snippet')}\n\n"
            
            report_progress(state, "synthesizing", f"Synthesizing information using {state.get('model', 'default model')}...", 65)
            
            prompt = INFORMATION_SYNTHESIS_PROMPT.format(
                query=state["query"],
                search_results=search_results_text
            )
            
            report_progress(state, "synthesizing", "Generating initial research draft...", 70)
            
            draft_research = query_llm(prompt, system_prompt=RESEARCHER_SYSTEM_PROMPT, model=state.get("model"))
            
            report_progress(state, "synthesizing", "Draft research complete", 75)
            
            return {"draft_research": draft_research, "status": "reflecting"}
        except Exception as e:
            report_progress(state, "error", f"Error in synthesizing information: {str(e)}", 0)
            return {"error": f"Error in synthesizing information: {str(e)}", "status": "error"}
    
    def reflect_and_improve(state: ResearchState) -> ResearchState:
        """Reflect on the research and improve it"""
        try:
            report_progress(state, "reflecting", "Reflecting on research quality...", 80)
            
            prompt = REFLECTION_PROMPT.format(
                query=state["query"],
                research_content=state["draft_research"]
            )
            
            report_progress(state, "reflecting", f"Analyzing draft using {state.get('model', 'default model')}...", 85)
            
            reflection = query_llm(prompt, system_prompt=RESEARCHER_SYSTEM_PROMPT, model=state.get("model"))
            
            report_progress(state, "reflecting", "Improving research based on analysis...", 90)
            
            improved_prompt = f"""
            Your original research:
            
            {state["draft_research"]}
            
            Your reflection on areas to improve:
            
            {reflection}
            
            Now, provide an improved version of the research that addresses these points.
            """
            
            report_progress(state, "reflecting", "Finalizing research output...", 95)
            
            final_research = query_llm(improved_prompt, system_prompt=RESEARCHER_SYSTEM_PROMPT, model=state.get("model"))
            
            report_progress(state, "completed", "Research completed successfully", 100)
            
            return {"final_research": final_research, "status": "completed"}
        except Exception as e:
            report_progress(state, "error", f"Error in reflection: {str(e)}", 0)
            return {"error": f"Error in reflection: {str(e)}", "status": "error"}
    
    # Create the workflow graph with explicit state schema
    workflow = StateGraph(state_schema=ResearchState)
    
    # Add nodes
    workflow.add_node("planning", plan_search_queries)
    workflow.add_node("searching", execute_searches)
    workflow.add_node("synthesizing", synthesize_information)
    workflow.add_node("reflecting", reflect_and_improve)
    
    # Define conditional routing
    def router(state: ResearchState) -> str:
        """Route to the next node based on the current status"""
        if state.get("error"):
            return END
        return state.get("status", "planning")
    
    # Add edges - directly connect nodes based on the expected flow
    workflow.add_edge("planning", "searching")
    workflow.add_edge("searching", "synthesizing")
    workflow.add_edge("synthesizing", "reflecting")
    workflow.add_edge("reflecting", END)
    
    # Set start node
    workflow.set_entry_point("planning")
    
    # Compile the graph
    return workflow.compile()

def run_research_agent(query: str, model: str = None, progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None) -> Dict[str, Any]:
    """
    Run the research agent with a given query
    
    Args:
        query: Research query string
        model: LLM model to use
        progress_callback: Optional callback function to report progress
        
    Returns:
        Dictionary with research results and metadata
    """
    try:
        agent = create_research_agent(progress_callback)
        
        # Initialize state with the query and model
        initial_state = {"query": query, "model": model, "status": "planning"}
        
        # Execute the agent
        final_state = agent.invoke(initial_state)
        
        # Prepare response
        response = {
            "query": query,
            "model": model,
            "status": final_state.get("status", "unknown"),
            "research": final_state.get("final_research", "") or final_state.get("draft_research", ""),
            "search_queries": final_state.get("search_queries", []),
            "search_results": final_state.get("search_results", []),
            "error": final_state.get("error")
        }
        
        return response
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        
        if progress_callback:
            progress_callback({
                "step": "error",
                "message": f"Unexpected error: {str(e)}",
                "percent": 0,
                "query": query
            })
            
        return {
            "query": query,
            "model": model,
            "status": "error",
            "error": f"Unexpected error: {str(e)}",
            "research": "",
            "search_queries": [],
            "search_results": []
        }
