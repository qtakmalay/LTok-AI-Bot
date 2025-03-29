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
    global website_texts
    if os.path.exists(settings.WEBSITE_TEXTS_FILE_PATH):
        print("Website texts file found. Loading website texts...")
        with open(settings.WEBSITE_TEXTS_FILE_PATH, "rb") as file:
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
    global website_texts, website_embeddings

    question_embedding = get_embedding(question)
    
    best_similarity = -1
    top_similarities = {}
    best_url = None
    for url, embedding in website_embeddings.items():
        similarity = cosine_similarity(question_embedding, embedding)
        print(f"Similarity with {url}: {similarity}")
        top_similarities[url] = similarity
        if similarity > best_similarity:
            best_similarity = similarity
            best_url = url

    if best_url is None:
        return "No relevant website found."

    sorted_similarities = sorted(top_similarities.items(), key=lambda x: x[1], reverse=True)
    top3 = sorted_similarities[:3]
    print("Top 3 Similarities:")
    for url, sim in top3:
        print(f"{url}: {sim}")

    context = website_texts[best_url]
    
    extra_info = ""
    if os.path.exists(settings.TEXT_PATH):
        with open(settings.TEXT_PATH, "r", encoding="utf-8") as file:
            extra_info = file.read()
    else:
        print("Additional info file not found at:", settings.TEXT_PATH)
    
    prompt = (
        f"Using the following website content as context:\n\n"
        f"{context}\n\n"
        f"Additional Information:\n\n"
        f"{extra_info}\n\n"
        f"Please answer the question below in a detailed, descriptive, and professional manner. "
        f"Ensure the response is clear, comprehensive, and includes all relevant information from the context.\n\n"
        f"Question: {question}\n"
    )
    print(f"Using content from: {best_url}")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0.3,
    )
    answer = response.choices[0].message.content.strip()
    return answer
