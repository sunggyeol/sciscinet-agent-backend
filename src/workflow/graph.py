from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from src.models.state import AgentState
from src.agents.filtering_agent import filtering_agent
from src.agents.analysis_agent import analysis_agent
from src.agents.visualization_agent import visualization_agent

def create_workflow() -> StateGraph:
    """Create the multi-agent workflow using LangGraph"""
    workflow = StateGraph(AgentState)
    
    workflow.add_node("filtering", filtering_agent)
    workflow.add_node("analysis", analysis_agent)
    workflow.add_node("visualization", visualization_agent)
    
    workflow.set_entry_point("filtering")
    
    workflow.add_edge("filtering", "analysis")
    workflow.add_edge("analysis", "visualization")
    workflow.add_edge("visualization", END)
    
    return workflow.compile()

async def process_query(user_query: str) -> dict:
    """Process user query through the agent workflow"""
    app = create_workflow()
    
    initial_state = {
        "messages": [HumanMessage(content=user_query)],
        "user_query": user_query,
        "query_type": None,
        "data": None,
        "analysis_result": None,
        "vega_spec": None,
        "next_step": None
    }
    
    result = await app.ainvoke(initial_state)
    
    return {
        "query": user_query,
        "query_type": result.get("query_type"),
        "analysis": result.get("analysis_result"),
        "vega_spec": result.get("vega_spec"),
        "data_count": len(result.get("data", []))
    }

