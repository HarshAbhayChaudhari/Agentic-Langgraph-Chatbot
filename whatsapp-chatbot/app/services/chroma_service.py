import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional, Any
import os
from datetime import datetime

class ChromaService:
    def __init__(self, persist_directory: str = "./data/chroma_db"):
        """
        Initialize ChromaDB service
        
        Args:
            persist_directory: Directory to persist ChromaDB data
        """
        self.persist_directory = persist_directory
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """
        Initialize ChromaDB client
        """
        try:
            # Check if running on Vercel (serverless environment)
            is_vercel = os.getenv('VERCEL') == '1'
            
            if is_vercel:
                # Use in-memory client for Vercel deployment
                self.client = chromadb.Client()
                print("ChromaDB client initialized in-memory for Vercel deployment")
            else:
                # Create persist directory if it doesn't exist
                os.makedirs(self.persist_directory, exist_ok=True)
                
                # Initialize ChromaDB client with persistence
                self.client = chromadb.PersistentClient(
                    path=self.persist_directory
                )
                print(f"ChromaDB client initialized with persist directory: {self.persist_directory}")
            
        except Exception as e:
            print(f"Error initializing ChromaDB client: {str(e)}")
            raise
    
    def create_collection(self, collection_name: str, metadata: Optional[Dict] = None) -> chromadb.Collection:
        """
        Create a new collection
        
        Args:
            collection_name: Name of the collection
            metadata: Optional metadata for the collection
            
        Returns:
            ChromaDB collection object
        """
        if not self.client:
            raise Exception("ChromaDB client not initialized")
        
        try:
            # Check if collection already exists
            existing_collections = self.client.list_collections()
            collection_exists = any(col.name == collection_name for col in existing_collections)
            
            if collection_exists:
                print(f"Collection '{collection_name}' already exists, getting existing collection")
                return self.client.get_collection(collection_name)
            
            # Create new collection
            collection = self.client.create_collection(
                name=collection_name,
                metadata=metadata or {"description": f"WhatsApp messages collection - {collection_name}"}
            )
            
            print(f"Created new collection: {collection_name}")
            return collection
            
        except Exception as e:
            print(f"Error creating collection '{collection_name}': {str(e)}")
            raise
    
    def get_collection(self, collection_name: str) -> chromadb.Collection:
        """
        Get an existing collection
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            ChromaDB collection object
        """
        if not self.client:
            raise Exception("ChromaDB client not initialized")
        
        try:
            return self.client.get_collection(collection_name)
        except Exception as e:
            print(f"Error getting collection '{collection_name}': {str(e)}")
            raise
    
    def store_embeddings(self, collection_name: str, documents: List[str], 
                        embeddings: List[List[float]], metadata: Optional[List[Dict]] = None):
        """
        Store documents and their embeddings in a collection
        
        Args:
            collection_name: Name of the collection
            documents: List of document texts
            embeddings: List of embedding vectors
            metadata: Optional list of metadata dictionaries
        """
        if not documents or not embeddings:
            print("No documents or embeddings provided")
            return
        
        try:
            # Get or create collection
            collection = self.get_collection(collection_name)
            
            # Prepare metadata if not provided
            if metadata is None:
                metadata = [{"timestamp": datetime.now().isoformat()} for _ in documents]
            
            # Generate IDs for documents
            ids = [f"doc_{i}_{datetime.now().timestamp()}" for i in range(len(documents))]
            
            # Add documents to collection
            collection.add(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadata,
                ids=ids
            )
            
            print(f"Successfully stored {len(documents)} documents in collection '{collection_name}'")
            
        except Exception as e:
            print(f"Error storing embeddings in collection '{collection_name}': {str(e)}")
            raise
    
    def search_similar(self, collection_name: str, query_embedding: List[float], 
                      top_k: int = 5) -> Dict[str, Any]:
        """
        Search for similar documents using a query embedding
        
        Args:
            collection_name: Name of the collection to search in
            query_embedding: Query embedding vector
            top_k: Number of similar documents to retrieve
            
        Returns:
            Dictionary containing search results
        """
        try:
            collection = self.get_collection(collection_name)
            
            # Search for similar documents
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            
            return results
            
        except Exception as e:
            print(f"Error searching in collection '{collection_name}': {str(e)}")
            raise
    
    def get_collection_info(self, collection_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a collection
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            Dictionary containing collection information
        """
        try:
            collection = self.get_collection(collection_name)
            count = collection.count()
            
            return {
                "name": collection_name,
                "count": count,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error getting collection info for '{collection_name}': {str(e)}")
            return None
    
    def list_collections(self) -> List[str]:
        """
        List all collections
        
        Returns:
            List of collection names
        """
        if not self.client:
            return []
        
        try:
            collections = self.client.list_collections()
            return [col.name for col in collections]
        except Exception as e:
            print(f"Error listing collections: {str(e)}")
            return []
    
    def delete_collection(self, collection_name: str):
        """
        Delete a collection
        
        Args:
            collection_name: Name of the collection to delete
        """
        if not self.client:
            raise Exception("ChromaDB client not initialized")
        
        try:
            self.client.delete_collection(collection_name)
            print(f"Successfully deleted collection: {collection_name}")
        except Exception as e:
            print(f"Error deleting collection '{collection_name}': {str(e)}")
            raise
    
    def clear_collection(self, collection_name: str):
        """
        Clear all documents from a collection
        
        Args:
            collection_name: Name of the collection to clear
        """
        try:
            collection = self.get_collection(collection_name)
            collection.delete(where={})  # Delete all documents
            print(f"Successfully cleared collection: {collection_name}")
        except Exception as e:
            print(f"Error clearing collection '{collection_name}': {str(e)}")
            raise 