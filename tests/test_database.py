import pytest
from src.utils.database import (
    get_papers_by_year,
    get_papers_by_field,
    get_top_cited_papers,
    get_papers_by_year_range,
    get_collaboration_stats,
    execute_query
)

@pytest.mark.asyncio
async def test_get_papers_by_year():
    """Test fetching papers by year"""
    result = await get_papers_by_year()
    
    assert isinstance(result, list)
    assert len(result) > 0
    
    for row in result:
        assert "year" in row
        assert "count" in row
        assert isinstance(row["year"], int)
        assert isinstance(row["count"], int)
        assert 2013 <= row["year"] <= 2022

@pytest.mark.asyncio
async def test_get_papers_by_field():
    """Test fetching papers by field"""
    result = await get_papers_by_field()
    
    assert isinstance(result, list)
    assert len(result) > 0
    
    for row in result:
        assert "field_name" in row
        assert "count" in row
        assert isinstance(row["field_name"], str)
        assert isinstance(row["count"], int)
        assert row["count"] > 0

@pytest.mark.asyncio
async def test_get_top_cited_papers():
    """Test fetching top cited papers"""
    limit = 5
    result = await get_top_cited_papers(limit=limit)
    
    assert isinstance(result, list)
    assert len(result) <= limit
    
    for row in result:
        assert "paper_id" in row
        assert "title" in row
        assert "citation_count" in row
        assert "year" in row
    
    if len(result) > 1:
        for i in range(len(result) - 1):
            assert result[i]["citation_count"] >= result[i + 1]["citation_count"]

@pytest.mark.asyncio
async def test_get_papers_by_year_range():
    """Test fetching papers within year range"""
    start_year = 2018
    end_year = 2020
    result = await get_papers_by_year_range(start_year, end_year)
    
    assert isinstance(result, list)
    assert len(result) > 0
    
    for row in result:
        assert "year" in row
        assert start_year <= row["year"] <= end_year

@pytest.mark.asyncio
async def test_get_collaboration_stats():
    """Test fetching collaboration statistics"""
    result = await get_collaboration_stats()
    
    assert isinstance(result, list)
    assert len(result) > 0
    
    for row in result:
        assert "year" in row
        assert "author_count" in row
        assert "paper_count" in row
        assert isinstance(row["year"], int)
        assert isinstance(row["author_count"], int)
        assert isinstance(row["paper_count"], int)

@pytest.mark.asyncio
async def test_execute_query():
    """Test custom query execution"""
    query = "SELECT COUNT(*) as total FROM papers"
    result = await execute_query(query)
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert "total" in result[0]
    assert result[0]["total"] > 0

@pytest.mark.asyncio
async def test_execute_query_with_params():
    """Test query execution with parameters"""
    query = "SELECT COUNT(*) as count FROM papers WHERE year = ?"
    result = await execute_query(query, (2020,))
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert "count" in result[0]

