import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch

from src.main import app

@pytest.mark.asyncio
async def test_root_endpoint():
    """Test root endpoint"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "message" in data
    assert "docs" in data

@pytest.mark.asyncio
async def test_health_endpoint():
    """Test health check endpoint"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["message"] == "SciSciNet Agent API"

@pytest.mark.asyncio
async def test_query_endpoint_papers_by_year(sample_papers_by_year, mock_llm_response):
    """Test query endpoint with papers by year query"""
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
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/query",
                json={"query": "Show me papers by year"}
            )
    
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "Show me papers by year"
    assert data["query_type"] == "papers_by_year"
    assert data["analysis"] is not None
    assert data["vega_spec"] is not None
    assert data["data_count"] > 0

@pytest.mark.asyncio
async def test_query_endpoint_papers_by_field(sample_papers_by_field, mock_llm_response):
    """Test query endpoint with papers by field query"""
    with patch('src.agents.filtering_agent.ChatAnthropic') as mock_filter_llm, \
         patch('src.agents.analysis_agent.ChatAnthropic') as mock_analysis_llm, \
         patch('src.agents.filtering_agent.get_papers_by_field', return_value=sample_papers_by_field):
        
        filter_mock = AsyncMock()
        filter_mock.ainvoke = AsyncMock(return_value=mock_llm_response("papers_by_field"))
        mock_filter_llm.return_value = filter_mock
        
        analysis_mock = AsyncMock()
        analysis_json = '{"summary": "Test", "key_findings": [], "viz_type": "bar", "x_field": "field_name", "y_field": "count"}'
        analysis_mock.ainvoke = AsyncMock(return_value=mock_llm_response(analysis_json))
        mock_analysis_llm.return_value = analysis_mock
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/query",
                json={"query": "Show me papers by field"}
            )
    
    assert response.status_code == 200
    data = response.json()
    assert data["query_type"] == "papers_by_field"

@pytest.mark.asyncio
async def test_query_endpoint_validation():
    """Test query endpoint with invalid input"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/query",
            json={}
        )
    
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_cors_headers():
    """Test CORS headers are present"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(
            "/api/v1/health",
            headers={"Origin": "http://localhost:5173"}
        )
    
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers

