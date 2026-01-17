"""
SQLAlchemy database models for AI Observability Platform.

This module defines the core data schema for storing LLM telemetry data.

Design Principles:
- Analytics-friendly: Optimized for time-series queries
- Indexed: Fast lookups by app_id, model, and timestamp
- Flexible: JSON metadata for extensibility
- Type-safe: Proper column types and constraints

Author: Tanush Banchhod
Project: AI Observability Platform
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, Index
from sqlalchemy.orm import declarative_base

# Create base class for all models
# All our table classes will inherit from this
Base = declarative_base()


class LLMRequest(Base):
    """
    Stores telemetry data from LLM applications.
    
    This is the main "fact table" for analytics. Each row represents
    one LLM inference call with its input, output, and performance metrics.
    
    Usage Example:
        from database.models import LLMRequest
        from database.db import SessionLocal
        
        # Create a new request record
        request = LLMRequest(
            app_id="my_chatbot",
            model_name="gpt-3.5-turbo",
            prompt="What is AI?",
            response="AI stands for Artificial Intelligence...",
            latency_ms=342.5,
            metadata={"user_id": "user_123", "session": "abc"}
        )
        
        # Save to database
        session = SessionLocal()
        session.add(request)
        session.commit()
    """
    
    # Table name in SQLite database
    __tablename__ = "llm_requests"
    
    # ============================================
    # PRIMARY KEY
    # ============================================
    id = Column(
        Integer, 
        primary_key=True, 
        autoincrement=True,
        comment="Unique identifier for each LLM request"
    )
    
    # ============================================
    # IDENTIFICATION COLUMNS
    # ============================================
    app_id = Column(
        String(255),
        nullable=False,
        index=True,  # Index for fast filtering by app
        comment="Application identifier (e.g., 'chatbot', 'code_assistant')"
    )
    
    model_name = Column(
        String(255),
        nullable=False,
        index=True,  # Index for fast filtering by model
        comment="LLM model used (e.g., 'gpt-4', 'claude-2', 'llama3:8b')"
    )
    
    # ============================================
    # REQUEST CONTENT
    # ============================================
    prompt = Column(
        Text,
        nullable=False,
        comment="User input/prompt sent to the LLM"
    )
    
    response = Column(
        Text,
        nullable=False,
        comment="LLM generated response/completion"
    )
    
    # ============================================
    # PERFORMANCE METRICS
    # ============================================
    latency_ms = Column(
        Float,
        nullable=False,
        comment="Response time in milliseconds (end-to-end)"
    )
    
    # ============================================
    # TIMESTAMPS
    # ============================================
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,  # Auto-populate with current time
        index=True,  # Critical for time-series queries
        comment="Timestamp when request was received by observability platform"
    )
    
    # ============================================
    # FLEXIBLE METADATA
    # ============================================
    metadata = Column(
        JSON,
        nullable=True,
        comment="Additional context stored as JSON (e.g., user_id, session_id, tags)"
    )
    
    # ============================================
    # COMPOSITE INDEXES FOR PERFORMANCE
    # ============================================
    # These speed up common query patterns:
    # 1. "Show me all requests for app X over time"
    # 2. "Show me all requests for model Y over time"
    __table_args__ = (
        Index("idx_app_created", "app_id", "created_at"),
        Index("idx_model_created", "model_name", "created_at"),
    )
    
    def __repr__(self):
        """String representation for debugging."""
        return (
            f"<LLMRequest("
            f"id={self.id}, "
            f"app={self.app_id}, "
            f"model={self.model_name}, "
            f"created={self.created_at}"
            f")>"
        )
    
    def to_dict(self):
        """
        Convert model instance to dictionary.
        
        Useful for API responses and debugging.
        
        Returns:
            dict: Dictionary representation of the request
        """
        return {
            "id": self.id,
            "app_id": self.app_id,
            "model_name": self.model_name,
            "prompt": self.prompt,
            "response": self.response,
            "latency_ms": self.latency_ms,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "metadata": self.metadata
        }


# ============================================
# UTILITY FUNCTIONS
# ============================================

def get_model_info():
    """
    Returns information about all defined models.
    
    Useful for debugging and validation.
    """
    models = {
        "llm_requests": {
            "class": LLMRequest,
            "table": LLMRequest.__tablename__,
            "columns": len(LLMRequest.__table__.columns),
            "indexes": len(LLMRequest.__table__.indexes)
        }
    }
    return models


def validate_schema():
    """
    Validates that the schema is properly defined.
    
    This is a sanity check to ensure all models have the required
    attributes and indexes.
    """
    print("=" * 70)
    print("DATABASE SCHEMA VALIDATION - Day 2")
    print("=" * 70)
    
    # Check LLMRequest model
    print(f"✅ Model: {LLMRequest.__name__}")
    print(f"   Table name: {LLMRequest.__tablename__}")
    print(f"   Total columns: {len(LLMRequest.__table__.columns)}")
    print(f"   Indexed columns: app_id, model_name, created_at")
    print(f"   Composite indexes: {len(LLMRequest.__table__.indexes)}")
    
    # List all columns
    print(f"\n   Columns:")
    for column in LLMRequest.__table__.columns:
        col_type = str(column.type)
        nullable = "NULL" if column.nullable else "NOT NULL"
        indexed = "INDEXED" if column.index else ""
        print(f"     - {column.name:15s} {col_type:20s} {nullable:10s} {indexed}")
    
    print("\n" + "=" * 70)
    print("✅ Schema validation passed!")
    print("=" * 70)


# ============================================
# EXAMPLE USAGE (for learning)
# ============================================

if __name__ == "__main__":
    """
    This code runs when you execute: python database/models.py
    
    It's useful for:
    1. Understanding the model structure
    2. Validating the schema
    3. Testing model creation (without database)
    """
    
    print("\n🔍 AI Observability Platform - Database Models\n")
    
    # Validate schema
    validate_schema()
    
    # Create a sample instance (not saved to database)
    print("\n📝 Example: Creating a sample LLMRequest instance\n")
    
    sample_request = LLMRequest(
        app_id="demo_chatbot",
        model_name="gpt-3.5-turbo",
        prompt="What is the capital of France?",
        response="Paris is the capital of France.",
        latency_ms=342.5,
        created_at=datetime.utcnow(),
        metadata={
            "user_id": "user_123",
            "session": "session_abc",
            "source": "web_interface"
        }
    )
    
    print(f"Created instance: {sample_request}")
    print(f"\nAs dictionary:")
    
    import json
    print(json.dumps(sample_request.to_dict(), indent=2, default=str))
    
    print("\n" + "=" * 70)
    print("✅ Day 2 Complete! LLMRequest model is ready.")
    print("=" * 70)
    print("\nNext Steps:")
    print("- Day 3: Add LLMEvaluation and Alert models")
    print("- Day 4: Create database session management (db.py)")
    print("- Day 5: Build initialization script to create tables")
