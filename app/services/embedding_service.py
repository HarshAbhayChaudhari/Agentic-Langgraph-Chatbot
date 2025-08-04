from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np
import os

class EmbeddingService:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the embedding service with a sentence transformer model
        
        Args:
            model_name: Name of the sentence transformer model to use
        """
        self.model_name = model_name
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """
        Load the sentence transformer model
        """
        try:
            print(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            print("Embedding model loaded successfully")
        except Exception as e:
            print(f"Error loading embedding model: {str(e)}")
            # Fallback to a smaller model if the main one fails
            try:
                print("Trying fallback model: sentence-transformers/paraphrase-MiniLM-L3-v2")
                self.model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L3-v2")
                print("Fallback embedding model loaded successfully")
            except Exception as e2:
                print(f"Error loading fallback model: {str(e2)}")
                raise Exception("Failed to load any embedding model")
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors (each vector is a list of floats)
        """
        if not self.model:
            raise Exception("Embedding model not loaded")
        
        if not texts:
            return []
        
        try:
            # Generate embeddings
            embeddings = self.model.encode(texts, convert_to_tensor=False)
            
            # Convert to list of lists
            if isinstance(embeddings, np.ndarray):
                embeddings = embeddings.tolist()
            
            return embeddings
            
        except Exception as e:
            print(f"Error generating embeddings: {str(e)}")
            raise
    
    def generate_single_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        
        Args:
            text: Text string to embed
            
        Returns:
            Embedding vector as a list of floats
        """
        embeddings = self.generate_embeddings([text])
        return embeddings[0] if embeddings else []
    
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of the embeddings
        
        Returns:
            Dimension of the embedding vectors
        """
        if not self.model:
            return 0
        
        # Generate a dummy embedding to get the dimension
        dummy_embedding = self.generate_single_embedding("test")
        return len(dummy_embedding)
    
    def compute_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Compute cosine similarity between two embeddings
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Cosine similarity score between 0 and 1
        """
        if not embedding1 or not embedding2:
            return 0.0
        
        # Convert to numpy arrays
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        
        # Compute cosine similarity
        similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        
        return float(similarity) 