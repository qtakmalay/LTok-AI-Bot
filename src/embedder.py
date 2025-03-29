import os
import pickle
from config import settings
from openai import OpenAI

client = OpenAI()
client.api_key = settings.OPENAI_KEY
if not client.api_key:
    raise Exception("OPENAI_KEY environment variable not set.")

def get_embedding(text, model="text-embedding-3-large"):
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding

def load_or_create_embeddings(website_texts):
    embeddings_file = settings.EMBEDDINGS_FILE_PATH

    if os.path.exists(embeddings_file):
        print("Embedding file found. Loading precomputed embeddings and skipping API calls...")
        with open(embeddings_file, "rb") as f:
            website_embeddings = pickle.load(f)
    else:
        print("No embeddings file found. Computing embeddings via API...")
        website_embeddings = {}
        for url, text in website_texts.items():
            if text:
                print(f"Creating embedding for {url} ...")
                website_embeddings[url] = get_embedding(text)
            else:
                print(f"No text extracted from {url}")
        with open(embeddings_file, "wb") as f:
            pickle.dump(website_embeddings, f)
        print(f"Saved embeddings to {embeddings_file}.")
    return website_embeddings
