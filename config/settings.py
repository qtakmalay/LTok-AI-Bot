import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

BASE_DATA_PATH = os.path.join("data")
LINKS_PICKLE_PATH = os.path.join(BASE_DATA_PATH, "links.pkl")
EMBEDDINGS_FILE_PATH = os.path.join(BASE_DATA_PATH, "embeddings.pkl")
WEBSITE_TEXTS_FILE_PATH = os.path.join(BASE_DATA_PATH, "website_texts.pkl")
TEXT_PATH = os.path.join(BASE_DATA_PATH, "info.txt")