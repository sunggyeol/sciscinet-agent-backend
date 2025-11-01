import pytest
from unittest.mock import AsyncMock, patch
from langchain_core.messages import HumanMessage

from src.workflow.graph import create_workflow, process_query

@pytest.mark.asyncio
async def test_create_workflow():
    """Test workflow creation"""
    workflow = create_workflow()
    
    assert workflow is not None
    graph = workflow.get_graph()
    
    nodes = list(graph.nodes.keys())
    assert "filtering" in nodes
    assert "analysis" in nodes
    assert "visualization" in nodes
    assert "__start__" in nodes
    assert "__end__" in nodes

@pytest.mark.asyncio
async def test_workflow_edges():
    """Test workflow has correct edges"""
    workflow = create_workflow()
    graph = workflow.get_graph()
    
    edges = graph.edges
    
    edge_list = [(edge.source, edge.target) for edge in edges]
    assert ("__start__", "filtering") in edge_list
    assert ("filtering", "analysis") in edge_list
    assert ("analysis", "visualization") in edge_list
    assert ("visualization", "__end__") in edge_list

@pytest.mark.asyncio
async def test_process_query_mock(sample_papers_by_year, sample_analysis_result, mock_llm_response):
    """Test full query processing with mocks"""
    with patch('src.agents.filtering_agent.ChatAnthropic') as mock_filter_llm, \
         patch('src.agents.analysis_agent.ChatAnthropic') as mock_analysis_llm, \
         patch('src.agents.filtering_agent.get_papers_by_year', return_value=sample_papers_by_year):
        
        filter_mock = AsyncMock()
        filter_mock.ainvoke = AsyncMock(return_value=mock_llm_response("papers_by_year"))
        mock_filter_llm.return_value = filter_mock
        
        analysis_mock = AsyncMock()
        analysis_json = '{"summary": "Test", "key_findings": [], "viz_type": "bar", "x_field": "year", "y_field": "count"}'
        analysis_mock.ainvoke = AsyncMock(return_value=mock_llm_response(analysis_json))
        mock_analysis_llm.return_value = analysis_mock
        
        result = await process_query("Show me papers by year")
    
    assert result["query"] == "Show me papers by year"
    assert result["query_type"] == "papers_by_year"
    assert result["analysis"] is not None
    assert result["vega_spec"] is not None
    assert result["data_count"] == len(sample_papers_by_year)

@pytest.mark.asyncio
async def test_process_query_vega_spec_structure(sample_papers_by_year, mock_llm_response):
    """Test that process_query returns valid Vega-Lite spec"""
    with patch('src.agents.filtering_agent.ChatAnthropic') as mock_filter_llm, \
         patch('src.agents.analysis_agent.ChatAnthropic') as mock_analysis_llm, \
         patch('src.agents.filtering_agent.get_papers_by_year', return_value=sample_papers_by_year):
        
        filter_mock = AsyncMock()
        filter_mock.ainvoke = AsyncMock(return_value=mock_llm_response("papers_by_year"))
        mock_filter_llm.return_value = filter_mock
        
        analysis_mock = AsyncMock()
        analysis_json = '{"summary": "Test", "key_findings": [], "viz_type": "bar", "x_field": "year", "y_field": "count"}'
        analysis_mock.ainvoke = AsyncMock(return_value=mock_llm_response(analysis_json))
        mock_analysis_llm.return_value = analysis_mock
        
        result = await process_query("Show me papers by year")
    
    vega_spec = result["vega_spec"]
    assert "$schema" in vega_spec
    assert "data" in vega_spec
    assert "mark" in vega_spec
    assert "encoding" in vega_spec
    assert vega_spec["$schema"] == "https://vega.github.io/schema/vega-lite/v5.json"

