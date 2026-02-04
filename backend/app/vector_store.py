import numpy as np
import os
import pickle
import hashlib

class VectorStore:
    def __init__(self):
        self.notices = []
        self.embeddings = []
        self.notices_file = "notices.pkl"
        
        # Load or initialize with sample data
        self._load_or_initialize()
    
    def _load_or_initialize(self):
        """Load existing data or create sample data"""
        if os.path.exists(self.notices_file):
            with open(self.notices_file, "rb") as f:
                data = pickle.load(f)
                self.notices = data['notices']
                self.embeddings = data['embeddings']
        else:
            self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample tender notices"""
        sample_notices = [
            "Construction of sustainable energy infrastructure for commercial buildings",
            "Development of AI-powered healthcare monitoring systems",
            "Implementation of cloud-based enterprise resource planning solutions",
            "Supply of eco-friendly office equipment and furniture",
            "Design and construction of smart city transportation systems",
            "Provision of cybersecurity consulting and implementation services",
            "Development of mobile applications for government services",
            "Installation of renewable energy systems for public facilities",
            "Supply of advanced medical equipment for hospitals",
            "Implementation of blockchain-based supply chain solutions",
            "Construction of educational facilities with modern technology",
            "Development of data analytics platforms for business intelligence",
            "Provision of IT infrastructure modernization services",
            "Design of sustainable water management systems",
            "Supply and installation of industrial automation equipment"
        ]
        
        self.notices = sample_notices
        # Generate simple hash-based embeddings for demo purposes
        self.embeddings = [self._simple_embedding(notice) for notice in sample_notices]
        
        # Save data
        self.save()
    
    def _simple_embedding(self, text: str) -> np.ndarray:
        """Generate a simple hash-based embedding for demo purposes"""
        # Use character frequencies and n-grams for basic semantic representation
        text_lower = text.lower()
        
        # Create a simple 100-dimensional vector
        embedding = np.zeros(100)
        
        # Fill with character frequencies
        for i, char in enumerate(text_lower[:50]):
            idx = ord(char) % 100
            embedding[idx] += 1.0
        
        # Add word count features
        words = text_lower.split()
        embedding[50] = len(words)
        
        # Add some keyword-based features
        keywords = ['sustainable', 'ai', 'cloud', 'smart', 'cyber', 'mobile', 
                   'renewable', 'medical', 'blockchain', 'data', 'infrastructure']
        for i, keyword in enumerate(keywords):
            if keyword in text_lower:
                embedding[60 + i] = 1.0
        
        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        
        return embedding
    
    def search(self, query: str, top_k: int = 10):
        """Search for similar notices using cosine similarity"""
        if not self.notices:
            return []
        
        query_embedding = self._simple_embedding(query)
        
        # Calculate cosine similarities
        similarities = []
        for i, notice_embedding in enumerate(self.embeddings):
            # Cosine similarity
            similarity = np.dot(query_embedding, notice_embedding)
            similarities.append((i, similarity))
        
        # Sort by similarity (highest first)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Return top-k results
        results = []
        for idx, similarity in similarities[:min(top_k, len(similarities))]:
            results.append({
                "notice": self.notices[idx],
                "similarity": float(similarity)
            })
        
        return results
    
    def add_notice(self, notice: str):
        """Add a new notice to the index"""
        embedding = self._simple_embedding(notice)
        self.embeddings.append(embedding)
        self.notices.append(notice)
        self.save()
    
    def save(self):
        """Save notices and embeddings to disk"""
        with open(self.notices_file, "wb") as f:
            pickle.dump({
                'notices': self.notices,
                'embeddings': self.embeddings
            }, f)

# Global instance
vector_store = VectorStore()

