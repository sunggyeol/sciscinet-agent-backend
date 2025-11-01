import aiosqlite
import os
from typing import List, Dict, Any

DATABASE_PATH = os.getenv("DATABASE_PATH", "data/sciscinet_vt_cs_2013_2022.db")

async def get_db_connection():
    """Get async database connection"""
    return await aiosqlite.connect(DATABASE_PATH)

async def execute_query(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """Execute a query and return results as list of dicts"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(query, params) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

async def get_papers_by_year() -> List[Dict[str, Any]]:
    """Get count of papers by year"""
    query = """
        SELECT year, COUNT(*) as count
        FROM papers
        WHERE year IS NOT NULL
        GROUP BY year
        ORDER BY year
    """
    return await execute_query(query)

async def get_papers_by_field() -> List[Dict[str, Any]]:
    """Get count of papers by field"""
    query = """
        SELECT f.field_name, COUNT(DISTINCT pf.paper_id) as count
        FROM fields f
        JOIN paper_fields pf ON f.field_id = pf.field_id
        GROUP BY f.field_name
        ORDER BY count DESC
    """
    return await execute_query(query)

async def get_top_cited_papers(limit: int = 10) -> List[Dict[str, Any]]:
    """Get top cited papers"""
    query = """
        SELECT paper_id, title, citation_count, year
        FROM papers
        WHERE citation_count IS NOT NULL
        ORDER BY citation_count DESC
        LIMIT ?
    """
    return await execute_query(query, (limit,))

async def get_papers_by_year_range(start_year: int, end_year: int) -> List[Dict[str, Any]]:
    """Get papers within a year range"""
    query = """
        SELECT paper_id, title, year, citation_count
        FROM papers
        WHERE year >= ? AND year <= ?
        ORDER BY year, citation_count DESC
    """
    return await execute_query(query, (start_year, end_year))

async def get_collaboration_stats() -> List[Dict[str, Any]]:
    """Get collaboration statistics by year"""
    query = """
        SELECT p.year, COUNT(DISTINCT paa.author_id) as author_count,
               COUNT(DISTINCT p.paper_id) as paper_count
        FROM papers p
        JOIN paper_author_affiliations paa ON p.paper_id = paa.paper_id
        WHERE p.year IS NOT NULL
        GROUP BY p.year
        ORDER BY p.year
    """
    return await execute_query(query)

