from openai import OpenAI

from info_segugio.config import Config


client = OpenAI(
    api_key=Config.AI_API_KEY,
    base_url=Config.AI_API_URL
)


def ask_llm(
    prompt,
    model=None,
    temperature=0.0,
    max_tokens=None
):
    payload = {
        "model": model or Config.LLM_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": temperature
    }

    if max_tokens:
        payload["max_tokens"] = max_tokens

    response = client.chat.completions.create(**payload)

    return response.choices[0].message.content.strip()