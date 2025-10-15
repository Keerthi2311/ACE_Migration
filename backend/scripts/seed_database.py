"""
Script to seed the vector database with sample historical projects.

This provides test data for the RAG system to demonstrate
how similar projects can be retrieved and used for insights.
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.vector_db_service import get_vector_db_service


# Sample historical projects
SAMPLE_PROJECTS = [
    {
        "project_id": "PROJ_2023_001",
        "source_version": "IIB_v10",
        "target_version": "ACE_v12",
        "flow_count": 100,
        "infrastructure": "container",
        "has_mq": True,
        "has_custom_plugins": True,
        "estimated_days": 55,
        "actual_days": 62,
        "variance_percentage": 12.7,
        "issues_encountered": [
            "container networking complexity",
            "custom adapter compatibility",
            "MQ configuration migration"
        ],
        "lessons_learned": "Container networking setup took longer than expected. Custom adapters required refactoring for ACE v12 compatibility.",
        "complexity_score": 7.5
    },
    {
        "project_id": "PROJ_2023_002",
        "source_version": "IIB_v9",
        "target_version": "ACE_v11",
        "flow_count": 75,
        "infrastructure": "on_premise",
        "has_mq": True,
        "has_custom_plugins": False,
        "estimated_days": 42,
        "actual_days": 44,
        "variance_percentage": 4.8,
        "issues_encountered": [
            "database driver updates",
            "SOAP endpoint testing"
        ],
        "lessons_learned": "Standard migration path. Database drivers needed updates but overall smooth transition.",
        "complexity_score": 5.0
    },
    {
        "project_id": "PROJ_2023_003",
        "source_version": "WMB_v8",
        "target_version": "ACE_v12",
        "flow_count": 150,
        "infrastructure": "cloud",
        "has_mq": False,
        "has_custom_plugins": True,
        "estimated_days": 68,
        "actual_days": 88,
        "variance_percentage": 29.4,
        "issues_encountered": [
            "major version jump complexity",
            "deprecated ESQL functions",
            "custom plugin rewrite required",
            "cloud security configurations"
        ],
        "lessons_learned": "Major version jump from WMB v8 required extensive testing. Custom plugins needed complete rewrite. Cloud security setup added significant time.",
        "complexity_score": 9.2
    },
    {
        "project_id": "PROJ_2024_001",
        "source_version": "IIB_v10",
        "target_version": "ACE_v12",
        "flow_count": 120,
        "infrastructure": "container",
        "has_mq": True,
        "has_custom_plugins": True,
        "estimated_days": 58,
        "actual_days": 64,
        "variance_percentage": 10.3,
        "issues_encountered": [
            "adapter compatibility",
            "container networking"
        ],
        "lessons_learned": "Custom adapters required 4 extra days for compatibility testing.",
        "complexity_score": 7.5
    },
    {
        "project_id": "PROJ_2024_002",
        "source_version": "IIB_v10",
        "target_version": "ACE_v12",
        "flow_count": 50,
        "infrastructure": "on_premise",
        "has_mq": False,
        "has_custom_plugins": False,
        "estimated_days": 28,
        "actual_days": 30,
        "variance_percentage": 7.1,
        "issues_encountered": [
            "minor ESQL adjustments"
        ],
        "lessons_learned": "Straightforward migration. Small flow count allowed thorough testing.",
        "complexity_score": 3.5
    },
    {
        "project_id": "PROJ_2024_003",
        "source_version": "ACE_v11",
        "target_version": "ACE_v12",
        "flow_count": 200,
        "infrastructure": "container",
        "has_mq": True,
        "has_custom_plugins": False,
        "estimated_days": 45,
        "actual_days": 48,
        "variance_percentage": 6.7,
        "issues_encountered": [
            "version-specific API changes"
        ],
        "lessons_learned": "Minor version upgrade was smooth. Containerization added minimal complexity.",
        "complexity_score": 4.0
    },
]


async def seed_database():
    """Seed the vector database with sample projects"""
    print("Starting database seeding...")
    
    try:
        # Get vector DB service
        vector_db_service = get_vector_db_service()
        
        print(f"Connected to Qdrant at {vector_db_service.client._client.rest_uri}")
        
        # Add each project
        for i, project in enumerate(SAMPLE_PROJECTS, 1):
            print(f"\nAdding project {i}/{len(SAMPLE_PROJECTS)}: {project['project_id']}")
            
            try:
                project_id = await vector_db_service.add_project(project)
                print(f"✓ Successfully added project: {project_id}")
                print(f"  - Source: {project['source_version']} → Target: {project['target_version']}")
                print(f"  - Flows: {project['flow_count']}")
                print(f"  - Estimated: {project['estimated_days']} days, Actual: {project['actual_days']} days")
            except Exception as e:
                print(f"✗ Error adding project: {str(e)}")
        
        # Get collection stats
        stats = vector_db_service.get_collection_stats()
        print(f"\n{'='*60}")
        print("Database seeding complete!")
        print(f"{'='*60}")
        print(f"Total projects in database: {stats['total_projects']}")
        print(f"Vector dimension: {stats['vector_dimension']}")
        print(f"Distance metric: {stats['distance_metric']}")
        
    except Exception as e:
        print(f"\nError during seeding: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("="*60)
    print("IBM ACE Migration Estimator - Database Seeder")
    print("="*60)
    
    # Check if OpenAI API key is set
    from app.core.config import settings
    if not settings.OPENAI_API_KEY:
        print("\n⚠️  WARNING: OPENAI_API_KEY not set in environment!")
        print("   Please set it in your .env file to generate embeddings.")
        sys.exit(1)
    
    # Run seeding
    asyncio.run(seed_database())
