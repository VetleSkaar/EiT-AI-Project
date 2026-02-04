import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import pickle

class VectorStore:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.dimension = 384  # Dimension for all-MiniLM-L6-v2
        self.index = faiss.IndexFlatL2(self.dimension)
        self.notices = []
        self.index_file = "faiss_index.bin"
        self.notices_file = "notices.pkl"
        
        # Load or initialize with sample data
        self._load_or_initialize()
    
    def _load_or_initialize(self):
        """Load existing index or create sample data"""
        if os.path.exists(self.index_file) and os.path.exists(self.notices_file):
            self.index = faiss.read_index(self.index_file)
            with open(self.notices_file, "rb") as f:
                self.notices = pickle.load(f)
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
        embeddings = self.model.encode(sample_notices)
        self.index.add(np.array(embeddings).astype('float32'))
        
        # Save index
        self.save()
    
    def search(self, query: str, top_k: int = 10):
        """Search for similar notices"""
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(
            np.array(query_embedding).astype('float32'), 
            min(top_k, len(self.notices))
        )
        
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.notices):
                results.append({
                    "notice": self.notices[idx],
                    "similarity": float(1 / (1 + distance))  # Convert distance to similarity
                })
        
        return results
    
    def add_notice(self, notice: str):
        """Add a new notice to the index"""
        embedding = self.model.encode([notice])
        self.index.add(np.array(embedding).astype('float32'))
        self.notices.append(notice)
        self.save()
    
    def save(self):
        """Save index and notices to disk"""
        faiss.write_index(self.index, self.index_file)
        with open(self.notices_file, "wb") as f:
            pickle.dump(self.notices, f)

# Global instance
vector_store = VectorStore()
