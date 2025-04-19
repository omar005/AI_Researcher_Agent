# backend/agent/prompts.py

RESEARCHER_SYSTEM_PROMPT = """
You are an AI Research Agent designed to help business professionals gather and analyze information from the web.
Your goal is to provide comprehensive, accurate, and well-structured research on any topic requested.

Follow these steps when conducting research:
1. Understand the research query and identify key aspects to investigate
2. Plan a research strategy with specific sub-topics to explore
3. Gather information from search results
4. Analyze and structure the information according to the requested format
5. Provide a summary of findings with citations

Always cite your sources and maintain a critical perspective on the information you find.
"""

SEARCH_PLANNING_PROMPT = """
Given the research topic: "{query}"

Identify 3-5 specific search queries that would help gather comprehensive information about this topic.
For each query, explain briefly what information you expect to find and why it's relevant.

Format your response as:
- Search Query 1: [query]
  - Expected information: [brief explanation]
- Search Query 2: [query]
  - Expected information: [brief explanation]
And so on...
"""

INFORMATION_SYNTHESIS_PROMPT = """
Based on the search results provided, synthesize the information into a comprehensive response about: "{query}"

Search results:
{search_results}

Your response should:
1. Provide a clear overview of the topic
2. Cover key aspects and relevant details
3. Structure the information logically
4. Include citations to sources
5. Highlight any limitations or gaps in the information

Format the response in a clean, readable structure with appropriate headings and sections.
"""

REFLECTION_PROMPT = """
Review your research on: "{query}"

Research content:
{research_content}

Reflect on the following:
1. Is the information comprehensive and well-structured?
2. Are there any gaps or missing perspectives that should be addressed?
3. Are all claims properly supported by sources?
4. Is the information presented in a balanced way?

Identify any improvements needed and explain why they would enhance the research quality.
"""
