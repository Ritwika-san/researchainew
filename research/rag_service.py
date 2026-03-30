import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = str(BASE_DIR / "chroma_db")

client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection(name="research_knowledge")
model = SentenceTransformer('all-MiniLM-L6-v2')

def store_research(topic, result, user_id):
    try:
        embedding = model.encode(topic).tolist()
        doc_id = f"user_{user_id}_topic_{abs(hash(topic))}"
        
        collection.upsert(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[result],
            metadatas=[{"topic": topic, "user_id": str(user_id)}]
        )
        return True
    except Exception as e:
        print(f"Error storing research: {e}")
        return False

def retrieve_similar(topic, user_id, n_results=2):
    try:
        count = collection.count()
        if count == 0:
            return ""
        
        embedding = model.encode(topic).tolist()
        
        results = collection.query(
            query_embeddings=[embedding],
            n_results=min(n_results, count),
            where={"user_id": str(user_id)}
        )
        
        if results['documents'] and results['documents'][0]:
            context = "\n\n".join(results['documents'][0])
            return context
        return ""
    
    except Exception as e:
        print(f"Error retrieving research: {e}")
        return ""