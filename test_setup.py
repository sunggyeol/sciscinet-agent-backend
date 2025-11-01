#!/usr/bin/env python3
"""Simple test script to verify the setup"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

async def test_database():
    """Test database connection and queries"""
    print("Testing database connection...")
    try:
        from src.utils.database import get_papers_by_year, get_papers_by_field
        
        papers_by_year = await get_papers_by_year()
        print(f"✓ Papers by year: {len(papers_by_year)} records")
        
        papers_by_field = await get_papers_by_field()
        print(f"✓ Papers by field: {len(papers_by_field)} records")
        
        return True
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False

async def test_workflow():
    """Test workflow creation"""
    print("\nTesting workflow creation...")
    try:
        from src.workflow.graph import create_workflow
        
        workflow = create_workflow()
        print(f"✓ Workflow created successfully")
        print(f"  Nodes: {list(workflow.get_graph().nodes.keys())}")
        
        return True
    except Exception as e:
        print(f"✗ Workflow test failed: {e}")
        return False

async def test_agents():
    """Test agent imports"""
    print("\nTesting agent imports...")
    try:
        from src.agents.filtering_agent import filtering_agent
        from src.agents.analysis_agent import analysis_agent
        from src.agents.visualization_agent import visualization_agent
        
        print("✓ All agents imported successfully")
        return True
    except Exception as e:
        print(f"✗ Agent import test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("=" * 50)
    print("SciSciNet Agent Backend - Setup Test")
    print("=" * 50)
    
    results = []
    
    results.append(await test_database())
    results.append(await test_workflow())
    results.append(await test_agents())
    
    print("\n" + "=" * 50)
    if all(results):
        print("✓ All tests passed!")
        print("\nYou can now start the server:")
        print("  uv run uvicorn src.main:app --reload")
    else:
        print("✗ Some tests failed. Please check the errors above.")
        sys.exit(1)
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())

