import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from langchain_core.messages import HumanMessage, AIMessage

from src.agents.filtering_agent import filtering_agent
from src.agents.analysis_agent import analysis_agent
from src.agents.visualization_agent import visualization_agent, create_vega_lite_spec
from src.models.state import AgentState

@pytest.mark.asyncio
async def test_filtering_agent_papers_by_year(sample_papers_by_year, mock_llm_response):
    """Test filtering agent for papers by year query"""
    state = {
        "messages": [HumanMessage(content="Show me papers by year")],
        "user_query": "Show me papers by year",
        "query_type": None,
        "data": None,
        "analysis_result": None,
        "vega_spec": None,
        "next_step": None
    }
    
    with patch('src.agents.filtering_agent.ChatAnthropic') as mock_llm:
        mock_instance = AsyncMock()
        mock_instance.ainvoke = AsyncMock(return_value=mock_llm_response("papers_by_year"))
        mock_llm.return_value = mock_instance
        
        with patch('src.agents.filtering_agent.get_papers_by_year', return_value=sample_papers_by_year):
            result = await filtering_agent(state)
    
    assert result["query_type"] == "papers_by_year"
    assert result["data"] == sample_papers_by_year
    assert len(result["messages"]) == 2
    assert result["next_step"] == "analysis"

@pytest.mark.asyncio
async def test_filtering_agent_papers_by_field(sample_papers_by_field, mock_llm_response):
    """Test filtering agent for papers by field query"""
    state = {
        "messages": [HumanMessage(content="Show me papers by field")],
        "user_query": "Show me papers by field",
        "query_type": None,
        "data": None,
        "analysis_result": None,
        "vega_spec": None,
        "next_step": None
    }
    
    with patch('src.agents.filtering_agent.ChatAnthropic') as mock_llm:
        mock_instance = AsyncMock()
        mock_instance.ainvoke = AsyncMock(return_value=mock_llm_response("papers_by_field"))
        mock_llm.return_value = mock_instance
        
        with patch('src.agents.filtering_agent.get_papers_by_field', return_value=sample_papers_by_field):
            result = await filtering_agent(state)
    
    assert result["query_type"] == "papers_by_field"
    assert result["data"] == sample_papers_by_field
    assert result["next_step"] == "analysis"

@pytest.mark.asyncio
async def test_analysis_agent_with_data(sample_papers_by_year, mock_llm_response):
    """Test analysis agent with valid data"""
    state = {
        "messages": [HumanMessage(content="Show me papers by year")],
        "user_query": "Show me papers by year",
        "query_type": "papers_by_year",
        "data": sample_papers_by_year,
        "analysis_result": None,
        "vega_spec": None,
        "next_step": None
    }
    
    analysis_json = '''
    {
        "summary": "Paper publication trends",
        "key_findings": ["Growth observed", "Peak in 2020"],
        "viz_type": "bar",
        "x_field": "year",
        "y_field": "count"
    }
    '''
    
    with patch('src.agents.analysis_agent.ChatAnthropic') as mock_llm:
        mock_instance = AsyncMock()
        mock_instance.ainvoke = AsyncMock(return_value=mock_llm_response(analysis_json))
        mock_llm.return_value = mock_instance
        
        result = await analysis_agent(state)
    
    assert result["analysis_result"] is not None
    assert "summary" in result["analysis_result"]
    assert "viz_type" in result["analysis_result"]
    assert result["next_step"] == "visualization"

@pytest.mark.asyncio
async def test_analysis_agent_no_data():
    """Test analysis agent with no data"""
    state = {
        "messages": [HumanMessage(content="Test")],
        "user_query": "Test",
        "query_type": "papers_by_year",
        "data": None,
        "analysis_result": None,
        "vega_spec": None,
        "next_step": None
    }
    
    result = await analysis_agent(state)
    
    assert result["analysis_result"] is not None
    assert "error" in result["analysis_result"]
    assert result["next_step"] == "end"

@pytest.mark.asyncio
async def test_visualization_agent(sample_papers_by_year, sample_analysis_result):
    """Test visualization agent"""
    state = {
        "messages": [HumanMessage(content="Show me papers by year")],
        "user_query": "Show me papers by year",
        "query_type": "papers_by_year",
        "data": sample_papers_by_year,
        "analysis_result": sample_analysis_result,
        "vega_spec": None,
        "next_step": None
    }
    
    result = await visualization_agent(state)
    
    assert result["vega_spec"] is not None
    assert "$schema" in result["vega_spec"]
    assert "data" in result["vega_spec"]
    assert "mark" in result["vega_spec"]
    assert "encoding" in result["vega_spec"]
    assert result["next_step"] == "end"

def test_create_vega_lite_spec_bar_chart(sample_papers_by_year, sample_analysis_result):
    """Test Vega-Lite spec generation for bar chart"""
    spec = create_vega_lite_spec(
        sample_papers_by_year,
        sample_analysis_result,
        "Show me papers by year"
    )
    
    assert spec["$schema"] == "https://vega.github.io/schema/vega-lite/v5.json"
    assert spec["data"]["values"] == sample_papers_by_year
    assert spec["mark"]["type"] == "bar"
    assert spec["mark"]["tooltip"] == True
    assert spec["encoding"]["x"]["field"] == "year"
    assert spec["encoding"]["y"]["field"] == "count"
    assert spec["width"] == 600
    assert spec["height"] == 400

def test_create_vega_lite_spec_line_chart(sample_papers_by_year):
    """Test Vega-Lite spec generation for line chart"""
    analysis = {
        "viz_type": "line",
        "x_field": "year",
        "y_field": "count"
    }
    
    spec = create_vega_lite_spec(
        sample_papers_by_year,
        analysis,
        "Show trend over time"
    )
    
    assert spec["mark"]["type"] == "line"
    assert spec["mark"]["point"] == True

def test_create_vega_lite_spec_area_chart(sample_papers_by_year):
    """Test Vega-Lite spec generation for area chart"""
    analysis = {
        "viz_type": "area",
        "x_field": "year",
        "y_field": "count"
    }
    
    spec = create_vega_lite_spec(
        sample_papers_by_year,
        analysis,
        "Show cumulative growth"
    )
    
    assert spec["mark"]["type"] == "area"
    assert spec["mark"]["line"] == True

