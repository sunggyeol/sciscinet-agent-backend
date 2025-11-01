import pytest
import os
from unittest.mock import AsyncMock, patch

from src.workflow.graph import process_query

pytestmark = pytest.mark.skipif(
    not os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY") == "test-key-placeholder",
    reason="Requires real ANTHROPIC_API_KEY for integration tests"
)

@pytest.mark.asyncio
@pytest.mark.integration
async def test_real_query_papers_by_year():
    """Integration test with real LLM - papers by year"""
    result = await process_query("Show me the number of papers by year")
    
    assert result["query"] == "Show me the number of papers by year"
    assert result["query_type"] is not None
    assert result["analysis"] is not None
    assert result["vega_spec"] is not None
    assert result["data_count"] > 0
    
    assert "$schema" in result["vega_spec"]
    assert "data" in result["vega_spec"]
    assert len(result["vega_spec"]["data"]["values"]) > 0

@pytest.mark.asyncio
@pytest.mark.integration
async def test_real_query_papers_by_field():
    """Integration test with real LLM - papers by field"""
    result = await process_query("Show me papers by field")
    
    assert result["query_type"] is not None
    assert result["vega_spec"] is not None
    assert result["data_count"] > 0

@pytest.mark.asyncio
@pytest.mark.integration
async def test_real_query_top_cited():
    """Integration test with real LLM - top cited papers"""
    result = await process_query("What are the most cited papers?")
    
    assert result["vega_spec"] is not None
    assert result["data_count"] > 0

@pytest.mark.asyncio
@pytest.mark.integration
async def test_real_query_collaboration():
    """Integration test with real LLM - collaboration stats"""
    result = await process_query("Show me collaboration statistics")
    
    assert result["vega_spec"] is not None
    assert result["data_count"] > 0

@pytest.mark.asyncio
@pytest.mark.integration
async def test_vega_spec_validity():
    """Test that generated Vega-Lite specs are valid"""
    result = await process_query("Show me papers by year")
    
    spec = result["vega_spec"]
    
    assert spec["$schema"] == "https://vega.github.io/schema/vega-lite/v5.json"
    assert "mark" in spec
    assert "encoding" in spec
    assert "data" in spec
    assert "values" in spec["data"]
    
    assert "x" in spec["encoding"]
    assert "y" in spec["encoding"]
    assert "field" in spec["encoding"]["x"]
    assert "field" in spec["encoding"]["y"]

@pytest.mark.asyncio
@pytest.mark.integration
async def test_analysis_quality():
    """Test that analysis results have required fields"""
    result = await process_query("Show me papers by year")
    
    analysis = result["analysis"]
    
    assert "summary" in analysis
    assert "key_findings" in analysis
    assert "viz_type" in analysis
    assert "x_field" in analysis
    assert "y_field" in analysis
    
    assert isinstance(analysis["summary"], str)
    assert isinstance(analysis["key_findings"], list)
    assert len(analysis["key_findings"]) > 0

