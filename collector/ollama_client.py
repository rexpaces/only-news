import requests
import json
import logging

logger = logging.getLogger(__name__)

OLLAMA_BASE_URL = "http://localhost:11434"
MODEL = "gemma3:12b"

VALID_CATEGORIES = {"World", "Politics", "Tech", "Science", "Sports", "Business"}

PROMPT_TEMPLATE = """You are a concise news editor. Given a news article's original title and description, generate a short title, short description, and category in English.

Original title: {title}
Original description: {description}

Rules:
- Short title: maximum 8 words, clear and informative, no clickbait
- Short description: 1-2 sentences, maximum 40 words, factual
- Category: pick exactly one from this list: World, Politics, Tech, Science, Sports, Business
- English only
- Respond with valid JSON only, no markdown, no extra text

{{"title": "...", "description": "...", "category": "..."}}"""


def process_article(title: str, description: str) -> dict:
    prompt = PROMPT_TEMPLATE.format(
        title=title,
        description=(description or "")[:500],
    )

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "format": "json",
            },
            timeout=90,
        )
        response.raise_for_status()

        result = response.json().get("response", "")
        parsed = json.loads(result)

        category = parsed.get("category", "World")
        if category not in VALID_CATEGORIES:
            category = "World"

        return {
            "title": str(parsed.get("title", title))[:120],
            "description": str(parsed.get("description", description or ""))[:300],
            "category": category,
        }

    except (requests.RequestException, json.JSONDecodeError, KeyError) as e:
        logger.warning(f"Ollama processing failed ({e}), using fallback")
        return {
            "title": title[:120],
            "description": (description or "")[:300],
            "category": "World",
        }
