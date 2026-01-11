print("Starting import check...")
try:
    import chromadb
    print("ChromaDB imported.")
    from sentence_transformers import SentenceTransformer
    print("SentenceTransformers imported.")
except ImportError as e:
    print(f"Import failed: {e}")
except Exception as e:
    print(f"Other error: {e}")
print("Done.")
