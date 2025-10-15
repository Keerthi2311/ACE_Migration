"""
Vector Database Service using Qdrant.

Manages storage and retrieval of historical project data
for RAG (Retrieval Augmented Generation).
"""

from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    Range
)
from openai import AsyncOpenAI
import uuid

from app.core.config import settings


class VectorDBService:
    """
    Service for interacting with Qdrant vector database.
    
    Manages:
    - Historical project storage
    - Semantic search for similar projects
    - Vector embeddings generation
    """
    
    def __init__(self):
        """Initialize Qdrant client"""
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY
        )
        self.collection_name = settings.QDRANT_COLLECTION_NAME
        self.embedding_dimension = settings.EMBEDDING_DIMENSION
        
        # Initialize OpenAI client for embeddings
        if settings.OPENAI_API_KEY:
            self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        else:
            self.openai_client = None
        
        # Ensure collection exists
        self._ensure_collection()
    
    def _ensure_collection(self):
        """Create collection if it doesn't exist"""
        try:
            self.client.get_collection(self.collection_name)
        except Exception:
            # Collection doesn't exist, create it
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.embedding_dimension,
                    distance=Distance.COSINE
                )
            )
    
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")
        
        response = await self.openai_client.embeddings.create(
            model=settings.EMBEDDING_MODEL,
            input=text
        )
        
        return response.data[0].embedding
    
    def create_project_text(self, project: Dict[str, Any]) -> str:
        """
        Create searchable text representation of project.
        
        Args:
            project: Project data dictionary
            
        Returns:
            Text representation for embedding
        """
        parts = [
            f"Migration from {project.get('source_version', 'Unknown')} to {project.get('target_version', 'Unknown')}",
            f"Flow count: {project.get('flow_count', 0)}",
            f"Infrastructure: {project.get('infrastructure', 'Unknown')}",
            f"Has MQ: {project.get('has_mq', False)}",
            f"Custom plugins: {project.get('has_custom_plugins', False)}",
            f"Complexity score: {project.get('complexity_score', 5.0)}"
        ]
        
        if project.get('issues_encountered'):
            parts.append(f"Issues: {', '.join(project['issues_encountered'])}")
        
        if project.get('lessons_learned'):
            parts.append(f"Lessons: {project['lessons_learned']}")
        
        return ". ".join(parts)
    
    async def add_project(self, project: Dict[str, Any]) -> str:
        """
        Add a historical project to the vector database.
        
        Args:
            project: Project data with required fields
            
        Returns:
            Project ID
        """
        # Generate project ID if not provided
        project_id = project.get('project_id') or f"PROJ_{uuid.uuid4().hex[:8]}"
        
        # Create searchable text
        project_text = self.create_project_text(project)
        
        # Generate embedding
        embedding = await self.generate_embedding(project_text)
        
        # Create point
        point = PointStruct(
            id=project_id,
            vector=embedding,
            payload=project
        )
        
        # Upsert to collection
        self.client.upsert(
            collection_name=self.collection_name,
            points=[point]
        )
        
        return project_id
    
    async def search_similar_projects(
        self,
        project_profile: Dict[str, Any],
        top_k: int = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar historical projects.
        
        Args:
            project_profile: Current project characteristics
            top_k: Number of results to return
            filters: Additional filters to apply
            
        Returns:
            List of similar projects with similarity scores
        """
        if top_k is None:
            top_k = settings.VECTOR_SEARCH_TOP_K
        
        # Create search text
        search_text = self.create_project_text(project_profile)
        
        # Generate embedding
        query_vector = await self.generate_embedding(search_text)
        
        # Build filters if provided
        search_filter = None
        if filters:
            conditions = []
            
            if 'source_version' in filters:
                conditions.append(
                    FieldCondition(
                        key="source_version",
                        match=MatchValue(value=filters['source_version'])
                    )
                )
            
            if 'target_version' in filters:
                conditions.append(
                    FieldCondition(
                        key="target_version",
                        match=MatchValue(value=filters['target_version'])
                    )
                )
            
            if 'infrastructure' in filters:
                conditions.append(
                    FieldCondition(
                        key="infrastructure",
                        match=MatchValue(value=filters['infrastructure'])
                    )
                )
            
            if 'flow_count_range' in filters:
                min_flows, max_flows = filters['flow_count_range']
                conditions.append(
                    FieldCondition(
                        key="flow_count",
                        range=Range(gte=min_flows, lte=max_flows)
                    )
                )
            
            if conditions:
                search_filter = Filter(must=conditions)
        
        # Perform search
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k,
            query_filter=search_filter,
            score_threshold=settings.VECTOR_SEARCH_SCORE_THRESHOLD
        )
        
        # Format results
        similar_projects = []
        for result in results:
            project = result.payload
            project['similarity_score'] = result.score
            similar_projects.append(project)
        
        return similar_projects
    
    async def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific project by ID.
        
        Args:
            project_id: Project identifier
            
        Returns:
            Project data or None if not found
        """
        try:
            result = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[project_id]
            )
            
            if result:
                return result[0].payload
            return None
        except Exception:
            return None
    
    def delete_project(self, project_id: str):
        """
        Delete a project from the vector database.
        
        Args:
            project_id: Project identifier
        """
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=[project_id]
        )
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the collection.
        
        Returns:
            Collection statistics
        """
        info = self.client.get_collection(self.collection_name)
        
        return {
            "total_projects": info.points_count,
            "vector_dimension": info.config.params.vectors.size,
            "distance_metric": info.config.params.vectors.distance
        }


# Singleton instance
_vector_db_service: Optional[VectorDBService] = None


def get_vector_db_service() -> VectorDBService:
    """Get or create vector DB service singleton"""
    global _vector_db_service
    if _vector_db_service is None:
        _vector_db_service = VectorDBService()
    return _vector_db_service
