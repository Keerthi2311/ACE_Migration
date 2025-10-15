"""
Example: How to add your own historical project data

This script demonstrates how to add a single historical project
to the vector database for RAG retrieval.
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.vector_db_service import get_vector_db_service


async def add_custom_project():
    """Example of adding a custom project"""
    
    # Define your project
    # CUSTOMIZE THIS with your actual project data
    my_project = {
        "project_id": "PROJ_CUSTOM_001",  # Unique identifier
        "source_version": "IIB_v10",       # Source version
        "target_version": "ACE_v12",       # Target version
        "flow_count": 85,                  # Number of flows
        "infrastructure": "on_premise",    # Infrastructure type
        "has_mq": True,                    # Has MQ?
        "has_custom_plugins": False,       # Has custom plugins?
        
        # Results
        "estimated_days": 48,              # Original estimate
        "actual_days": 52,                 # Actual time taken
        "variance_percentage": 8.3,        # Variance %
        
        # Context (helps with similarity search)
        "issues_encountered": [
            "ESQL compatibility",
            "performance testing delays"
        ],
        "lessons_learned": "Performance testing took longer than expected due to new infrastructure. ESQL changes were minimal.",
        "complexity_score": 5.5            # 1-10 scale
    }
    
    # Get vector DB service
    vector_db_service = get_vector_db_service()
    
    # Add the project
    print(f"Adding project: {my_project['project_id']}")
    project_id = await vector_db_service.add_project(my_project)
    print(f"✓ Successfully added project: {project_id}")
    
    # Verify it was added
    retrieved = await vector_db_service.get_project(project_id)
    if retrieved:
        print(f"✓ Verified: Project can be retrieved")
        print(f"  Source: {retrieved['source_version']} → Target: {retrieved['target_version']}")
        print(f"  Estimated: {retrieved['estimated_days']} days, Actual: {retrieved['actual_days']} days")
    
    # Test similarity search
    print("\nTesting similarity search...")
    similar = await vector_db_service.search_similar_projects(
        project_profile={
            'source_version': 'IIB_v10',
            'target_version': 'ACE_v12',
            'flow_count': 90,
            'infrastructure': 'on_premise'
        },
        top_k=3
    )
    
    print(f"Found {len(similar)} similar projects:")
    for proj in similar:
        print(f"  - {proj['project_id']}: {proj['flow_count']} flows, "
              f"{proj['actual_days']} days (similarity: {proj['similarity_score']:.2f})")


if __name__ == "__main__":
    print("="*60)
    print("Adding Custom Historical Project")
    print("="*60)
    print()
    
    # Check if OpenAI API key is set
    from app.core.config import settings
    if not settings.OPENAI_API_KEY:
        print("⚠️  WARNING: OPENAI_API_KEY not set!")
        print("   Please set it in your .env file.")
        sys.exit(1)
    
    # Run the example
    asyncio.run(add_custom_project())
    
    print()
    print("="*60)
    print("Done! Your project is now in the database.")
    print("="*60)
