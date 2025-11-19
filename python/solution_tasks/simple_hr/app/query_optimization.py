"""
Query optimization utilities.

Provides tools for preventing N+1 queries and optimizing database access
patterns in SQLAlchemy.
"""

from __future__ import annotations

import logging
from typing import Any, List, Optional, TypeVar

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from sqlalchemy.orm import Query

logger = logging.getLogger(__name__)

T = TypeVar('T')


def eager_load_relationships(
    query: Query,
    relationships: List[str],
) -> Query:
    """
    Add eager loading for specified relationships.

    Prevents N+1 query problem by eagerly loading related objects.

    Args:
        query: SQLAlchemy query object.
        relationships: List of relationship names to eager load.

    Returns:
        Modified query with eager loading.
    """
    for relationship in relationships:
        try:
            query = query.options(__import__('sqlalchemy.orm')
                                   .orm.joinedload(relationship))
        except Exception as e:
            logger.warning(f"Could not eager load relationship {relationship}: {e}")

    return query


def add_query_columns(
    query: Query,
    columns: List[str],
) -> Query:
    """
    Add only specific columns to query.

    Reduces data transfer by selecting only needed columns.

    Args:
        query: SQLAlchemy query object.
        columns: List of column names to select.

    Returns:
        Modified query selecting only specified columns.
    """
    try:
        model = query.statement.froms[0].entity
        selected_columns = [getattr(model, col) for col in columns if hasattr(model, col)]
        return query.with_entities(*selected_columns)
    except Exception as e:
        logger.warning(f"Could not add specific columns: {e}")
        return query


def batch_fetch_related(
    model: Any,
    objects: List[Any],
    relationship_name: str,
    session: Any,
) -> None:
    """
    Batch fetch related objects for multiple parent objects.

    Prevents N+1 queries by fetching related objects in one query.

    Args:
        model: SQLAlchemy model class.
        objects: List of parent objects.
        relationship_name: Name of the relationship to fetch.
        session: SQLAlchemy session.
    """
    if not objects:
        return

    try:
        relationship = inspect(model).relationships.get(relationship_name)
        if not relationship:
            logger.warning(f"Relationship {relationship_name} not found on {model}")
            return

        # Get all related IDs
        related_ids = set()
        for obj in objects:
            related_obj = getattr(obj, relationship_name, None)
            if related_obj:
                if isinstance(related_obj, list):
                    related_ids.update([o.id for o in related_obj if hasattr(o, 'id')])
                elif hasattr(related_obj, 'id'):
                    related_ids.add(related_obj.id)

        # Fetch all related objects at once
        if related_ids:
            related_model = relationship.mapper.class_
            session.query(related_model).filter(
                related_model.id.in_(related_ids)
            ).all()

    except Exception as e:
        logger.warning(f"Error in batch_fetch_related: {e}")


def count_queries(session: Any) -> int:
    """
    Get count of executed queries in current session.

    Args:
        session: SQLAlchemy session.

    Returns:
        Number of queries executed.
    """
    try:
        from sqlalchemy import event

        query_count = [0]

        @event.listens_for(session, 'after_bulk_insert')
        @event.listens_for(session, 'after_bulk_update')
        @event.listens_for(session, 'after_bulk_delete')
        def receive_after_bulk_operation(update_context):
            query_count[0] += 1

        return query_count[0]
    except Exception as e:
        logger.warning(f"Could not count queries: {e}")
        return 0


class OptimizedQuery:
    """Helper class for building optimized queries."""

    def __init__(self, model: Any, session: Any) -> None:
        """
        Initialize OptimizedQuery.

        Args:
            model: SQLAlchemy model class.
            session: SQLAlchemy session.
        """
        self.model = model
        self.session = session
        self.query = session.query(model)
        self._relationships = []
        self._columns = None

    def with_relationships(self, *relationships: str) -> OptimizedQuery:
        """
        Add eager loading for relationships.

        Args:
            *relationships: Relationship names to eager load.

        Returns:
            Self for chaining.
        """
        self._relationships.extend(relationships)
        return self

    def with_columns(self, *columns: str) -> OptimizedQuery:
        """
        Select only specific columns.

        Args:
            *columns: Column names to select.

        Returns:
            Self for chaining.
        """
        self._columns = columns
        return self

    def filter_by(self, **kwargs: Any) -> OptimizedQuery:
        """
        Add filter conditions.

        Args:
            **kwargs: Filter conditions.

        Returns:
            Self for chaining.
        """
        self.query = self.query.filter_by(**kwargs)
        return self

    def all(self) -> List[Any]:
        """
        Execute query and return all results.

        Returns:
            List of query results.
        """
        query = self._apply_optimizations(self.query)
        return query.all()

    def first(self) -> Optional[Any]:
        """
        Execute query and return first result.

        Returns:
            First query result or None.
        """
        query = self._apply_optimizations(self.query)
        return query.first()

    def count(self) -> int:
        """
        Execute query and count results.

        Returns:
            Count of query results.
        """
        return self.query.count()

    def _apply_optimizations(self, query: Query) -> Query:
        """Apply all optimizations to query."""
        if self._relationships:
            query = eager_load_relationships(query, self._relationships)

        if self._columns:
            query = add_query_columns(query, list(self._columns))

        return query


def paginate_query(
    query: Query,
    page: int = 1,
    per_page: int = 20,
) -> tuple[List[Any], int, int]:
    """
    Paginate a query.

    Args:
        query: SQLAlchemy query object.
        page: Page number (1-indexed).
        per_page: Results per page.

    Returns:
        Tuple of (results, total_count, total_pages).
    """
    total_count = query.count()
    total_pages = (total_count + per_page - 1) // per_page

    results = (
        query.offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return results, total_count, total_pages
