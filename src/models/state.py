from typing import TypedDict, Annotated, Sequence, Optional, Dict, Any
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    """State shared across all agents in the workflow"""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    user_query: str
    query_type: Optional[str]
    data: Optional[list]
    analysis_result: Optional[Dict[str, Any]]
    vega_spec: Optional[Dict[str, Any]]
    next_step: Optional[str]

