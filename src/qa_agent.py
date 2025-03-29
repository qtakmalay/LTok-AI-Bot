import os
import pickle
from config import settings
from src.scraper import extract_text_from_url
from src.embedder import get_embedding, load_or_create_embeddings
from src.similarity import cosine_similarity
from openai import OpenAI

client = OpenAI()
client.api_key = settings.OPENAI_KEY

website_texts = {}
website_embeddings = {}

def initialize_agent():
    if os.path.exists(settings.WEBSITE_TEXTS_FILE_PATH):
        print("Website texts file found. Loading website texts...")
        with open(settings.WEBSITE_TEXTS_FILE_PATH, "rb") as file:
            global website_texts
            website_texts = pickle.load(file)
    else:
        print("No website texts file found. Extracting texts from websites...")
        with open(settings.LINKS_PICKLE_PATH, "rb") as file:
            links = pickle.load(file)
        website_texts_local = {}
        for url in links:
            print(f"Extracting text from {url} ...")
            website_texts_local[url] = extract_text_from_url(url)
        website_texts = website_texts_local
        with open(settings.WEBSITE_TEXTS_FILE_PATH, "wb") as file:
            pickle.dump(website_texts, file)
        print(f"Saved website texts to {settings.WEBSITE_TEXTS_FILE_PATH}.")

    global website_embeddings
    website_embeddings = load_or_create_embeddings(website_texts)

def answer_question(question):
    question_embedding = get_embedding(question)
    
    best_similarity = -1
    best_url = None
    for url, embedding in website_embeddings.items():
        similarity = cosine_similarity(question_embedding, embedding)
        print(f"Similarity with {url}: {similarity}")
        if similarity > best_similarity:
            best_similarity = similarity
            best_url = url

    if best_url is None:
        return "No relevant website found."

    context = website_texts[best_url]
    prompt = (
        f"Using the following website content as context:\n\n"
        f"{context}\n\n"
        f"Answer the following question:\n{question}\n"
    )
    print(f"Using content from: {best_url}")

    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=200,
        temperature=0.3,
    )
    answer = response.choices[0].text.strip()
    return answer
