import chainlit as cl

from datetime import datetime

from tavily import TavilyClient

from info_segugio.ai import ask_llm
from info_segugio.config import Config

from info_segugio.prompts import (
    ANALYSIS_PROMPT,
    NEXT_RESEARCH_PROMPT,
    FINAL_SUMMARY_PROMPT
)

MAX_CYCLES = 2


def format_result(result):

    title = result.get("title", "")
    content = result.get("content", "")

    return f"""
Titolo:
{title}

Contenuto:
{content}
"""


def web_research(search_query):

    today = datetime.now().strftime("%Y-%m-%d")

    enhanced_query = f"""
Data attuale: {today}

{search_query}

Usa informazioni aggiornate.
Privilegia risultati recenti.
"""

    client = TavilyClient(
        api_key=Config.TAVILY_API_KEY
    )

    response = client.search(
        query=enhanced_query,
        max_results=5,
        include_raw_content=False
    )

    results = response.get("results", [])

    titles = [
        result.get("title", "")
        for result in results
    ]

    contents = [
        format_result(result)
        for result in results
    ]

    return {
        "sources": titles,
        "contents": contents
    }


@cl.on_chat_start
async def start():

    await cl.Message(
        content="""
# 🔎 Info Segugio

Agente di ricerca iterativa.

"""
    ).send()


@cl.on_message
async def main(message: cl.Message):

    original_query = message.content.strip()

    if not original_query:

        await cl.Message(
            content="⚠️ Inserisci una domanda valida."
        ).send()

        return

    current_query = original_query

    running_summary = []

    searched_queries = set()

    await cl.Message(
        content="🚀 Avvio ricerca..."
    ).send()

    for cycle in range(MAX_CYCLES):

        await cl.Message(
            content=f"""
## 🔍 Ciclo {cycle + 1}/{MAX_CYCLES}

Domanda:

{current_query}
"""
        ).send()

        search_data = web_research(current_query)

        sources = search_data["sources"]

        contents = search_data["contents"]

        source_text = "\n".join(
            f"• {source}"
            for source in sources
        )

        await cl.Message(
            content=f"""
### 📚 Fonti trovate

{source_text}
"""
        ).send()

        analysis = ask_llm(
            ANALYSIS_PROMPT.format(
                query=current_query,
                web_results="\n\n".join(contents)
            ),
            model=Config.LLM_MODEL_LOW,
            temperature=0.0
        )

        running_summary.append(analysis)

        await cl.Message(
            content=f"""
### 📝 Riassunto intermedio

{analysis}
"""
        ).send()

        next_query = ask_llm(
            NEXT_RESEARCH_PROMPT.format(
                original_query=original_query,
                running_summary="\n\n".join(running_summary)
            ),
            model=Config.LLM_MODEL_LOW,
            temperature=0.0
        ).strip()

        if (
            next_query.upper() == "STOP"
            or next_query in searched_queries
            or not next_query
        ):

            await cl.Message(
                content="✅ Ricerca completata."
            ).send()

            break

        searched_queries.add(next_query)

        await cl.Message(
            content=f"""
### 🔎 Nuovo approfondimento

{next_query}
"""
        ).send()

        current_query = next_query

    await cl.Message(
        content="🧠 Elaborazione risposta finale..."
    ).send()

    final_answer = ask_llm(
        FINAL_SUMMARY_PROMPT.format(
            original_query=original_query,
            running_summary="\n\n".join(running_summary)
        ),
        model=Config.LLM_MODEL,
        temperature=0.0
    )

    await cl.Message(
        content=f"""
# ✅ Risposta finale

{final_answer}
"""
    ).send()