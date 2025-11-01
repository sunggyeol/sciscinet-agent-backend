from langchain_core.messages import HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic
from src.models.state import AgentState
from src.utils.database import (
    get_papers_by_year,
    get_papers_by_field,
    get_top_cited_papers,
    get_papers_by_year_range,
    get_collaboration_stats
)

async def filtering_agent(state: AgentState) -> AgentState:
    """Analyze user query and fetch relevant data from database"""
    user_query = state["user_query"].lower()
    
    llm = ChatAnthropic(model="claude-sonnet-4-5", temperature=0)
    
    prompt = f"""Analyze this query and determine what type of data is needed:
Query: {user_query}

Classify into one of these categories:
- papers_by_year: queries about paper counts over time
- papers_by_field: queries about papers in different research fields
- top_cited: queries about most cited papers
- collaboration: queries about author collaborations
- year_range: queries about papers in a specific time period

Respond with ONLY the category name."""
    
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    query_type = response.content.strip().lower()
    
    data = None
    if "papers_by_year" in query_type:
        data = await get_papers_by_year()
    elif "papers_by_field" in query_type:
        data = await get_papers_by_field()
    elif "top_cited" in query_type:
        data = await get_top_cited_papers()
    elif "collaboration" in query_type:
        data = await get_collaboration_stats()
    elif "year_range" in query_type:
        data = await get_papers_by_year_range(2013, 2022)
    else:
        data = await get_papers_by_year()
    
    return {
        **state,
        "query_type": query_type,
        "data": data,
        "messages": state["messages"] + [AIMessage(content=f"Fetched {len(data)} records for {query_type}")],
        "next_step": "analysis"
    }

