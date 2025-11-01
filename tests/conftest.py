import pytest
import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

os.environ["DATABASE_PATH"] = str(project_root / "data" / "sciscinet_vt_cs_2013_2022.db")
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY", "test-key-placeholder")

@pytest.fixture
def sample_papers_by_year():
    """Sample data for papers by year"""
    return [
        {"year": 2013, "count": 1523},
        {"year": 2014, "count": 1687},
        {"year": 2015, "count": 1842},
        {"year": 2016, "count": 1956},
        {"year": 2017, "count": 2134},
        {"year": 2018, "count": 2298},
        {"year": 2019, "count": 2456},
        {"year": 2020, "count": 2687},
        {"year": 2021, "count": 2543},
        {"year": 2022, "count": 2398}
    ]

@pytest.fixture
def sample_papers_by_field():
    """Sample data for papers by field"""
    return [
        {"field_name": "Machine Learning", "count": 3456},
        {"field_name": "Computer Vision", "count": 2987},
        {"field_name": "Natural Language Processing", "count": 2654},
        {"field_name": "Robotics", "count": 1876},
        {"field_name": "Computer Networks", "count": 1543}
    ]

@pytest.fixture
def sample_top_cited():
    """Sample data for top cited papers"""
    return [
        {"paper_id": 123, "title": "Deep Learning Paper", "citation_count": 5000, "year": 2020},
        {"paper_id": 456, "title": "Neural Networks", "citation_count": 4500, "year": 2019},
        {"paper_id": 789, "title": "Computer Vision", "citation_count": 4000, "year": 2021}
    ]

@pytest.fixture
def sample_analysis_result():
    """Sample analysis result"""
    return {
        "summary": "Paper publication trends from 2013-2022",
        "key_findings": ["Peak in 2020", "Steady growth"],
        "viz_type": "bar",
        "x_field": "year",
        "y_field": "count"
    }

@pytest.fixture
def mock_llm_response():
    """Mock LLM response factory"""
    def _create_response(content):
        class MockResponse:
            def __init__(self, content):
                self.content = content
        return MockResponse(content)
    return _create_response

