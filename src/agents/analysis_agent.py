from langchain_core.messages import AIMessage
from langchain_anthropic import ChatAnthropic
from src.models.state import AgentState
import json

async def analysis_agent(state: AgentState) -> AgentState:
    """Analyze the fetched data and prepare insights"""
    data = state["data"]
    query_type = state["query_type"]
    user_query = state["user_query"]
    
    if not data:
        return {
            **state,
            "analysis_result": {"error": "No data available"},
            "messages": state["messages"] + [AIMessage(content="No data found")],
            "next_step": "end"
        }
    
    llm = ChatAnthropic(model="claude-sonnet-4-5", temperature=0)
    
    data_summary = json.dumps(data[:10], indent=2) if len(data) > 10 else json.dumps(data, indent=2)
    
    prompt = f"""Analyze this data and provide insights for the user query.

User Query: {user_query}
Query Type: {query_type}
Data Sample (first 10 records):
{data_summary}

Total Records: {len(data)}

Provide a brief analysis including:
1. Key findings
2. Trends or patterns
3. Suggested visualization type (bar, line, area, scatter, etc.)

Respond in JSON format:
{{
    "summary": "brief summary",
    "key_findings": ["finding1", "finding2"],
    "viz_type": "bar|line|area|scatter",
    "x_field": "field name for x-axis",
    "y_field": "field name for y-axis"
}}"""
    
    response = await llm.ainvoke([{"role": "user", "content": prompt}])
    
    try:
        analysis_result = json.loads(response.content)
    except:
        analysis_result = {
            "summary": "Data analysis completed",
            "key_findings": [f"Found {len(data)} records"],
            "viz_type": "bar",
            "x_field": list(data[0].keys())[0] if data else "x",
            "y_field": list(data[0].keys())[1] if data and len(data[0]) > 1 else "y"
        }
    
    return {
        **state,
        "analysis_result": analysis_result,
        "messages": state["messages"] + [AIMessage(content=f"Analysis: {analysis_result['summary']}")],
        "next_step": "visualization"
    }

