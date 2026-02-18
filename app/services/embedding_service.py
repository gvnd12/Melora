from sentence_transformers import SentenceTransformer

model = SentenceTransformer(model_name_or_path="all-MiniLM-L6-v2")

def generate_song_embeddings(song_data:str):
    return model.encode(song_data).tolist()