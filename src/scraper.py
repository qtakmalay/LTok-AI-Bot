import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text(separator="\n")
            lines = [line.strip() for line in text.splitlines()]
            text = "\n".join(line for line in lines if line)
            return text
        else:
            print(f"Error: {url} returned status code {response.status_code}")
            return ""
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""
