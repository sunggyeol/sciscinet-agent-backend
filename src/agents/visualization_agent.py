from langchain_core.messages import AIMessage
from src.models.state import AgentState
from typing import Dict, Any

def create_vega_lite_spec(data: list, analysis: Dict[str, Any], user_query: str) -> Dict[str, Any]:
    """Generate Vega-Lite specification based on data and analysis"""
    viz_type = analysis.get("viz_type", "bar")
    x_field = analysis.get("x_field", list(data[0].keys())[0] if data else "x")
    y_field = analysis.get("y_field", list(data[0].keys())[1] if data and len(data[0]) > 1 else "y")
    
    x_type = "ordinal"
    if data and x_field in data[0]:
        if isinstance(data[0][x_field], (int, float)):
            x_type = "quantitative"
        elif "year" in x_field.lower():
            x_type = "temporal"
    
    y_type = "quantitative"
    
    spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": user_query,
        "data": {"values": data},
        "mark": {
            "type": viz_type,
            "tooltip": True
        },
        "encoding": {
            "x": {
                "field": x_field,
                "type": x_type,
                "axis": {"labelAngle": -45}
            },
            "y": {
                "field": y_field,
                "type": y_type
            }
        },
        "width": 600,
        "height": 400
    }
    
    if viz_type == "bar":
        spec["encoding"]["x"]["axis"]["labelAngle"] = -45
        spec["encoding"]["color"] = {
            "field": x_field,
            "type": "nominal",
            "legend": None
        }
    
    if viz_type == "line":
        spec["mark"] = {"type": "line", "point": True, "tooltip": True}
    
    if viz_type == "area":
        spec["mark"] = {"type": "area", "line": True, "point": True, "tooltip": True}
    
    spec["config"] = {
        "view": {"strokeWidth": 0},
        "axis": {"grid": True}
    }
    
    return spec

async def visualization_agent(state: AgentState) -> AgentState:
    """Generate Vega-Lite visualization specification"""
    data = state["data"]
    analysis_result = state["analysis_result"]
    user_query = state["user_query"]
    
    if not data or not analysis_result:
        return {
            **state,
            "vega_spec": None,
            "messages": state["messages"] + [AIMessage(content="Cannot generate visualization")],
            "next_step": "end"
        }
    
    vega_spec = create_vega_lite_spec(data, analysis_result, user_query)
    
    return {
        **state,
        "vega_spec": vega_spec,
        "messages": state["messages"] + [AIMessage(content="Visualization generated")],
        "next_step": "end"
    }

