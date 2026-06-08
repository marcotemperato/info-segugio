import chainlit as cl

from info_segugio.ai import ask_llm
from info_segugio.config import Config

from info_segugio.prompts import (
    ANALYSIS_PROMPT,
    NEXT_RESEARCH_PROMPT,
    FINAL_SUMMARY_PROMPT
)

MAX_CYCLES = 2


@cl.on_chat_start
async def start():
    await cl.Message(
        content="""
# Info Segugio

Inserisci una domanda.
"""
    ).send()


@cl.on_message
async def main(message: cl.Message):
    original_query = message.content.strip()
    if not original_query:
        await cl.Message(content="Per favore inserisci una domanda valida.").send()
        return

    current_query = original_query
    running_summary = []
    searched_queries = {original_query}

    status = cl.Message(content="🔍 Avvio ricerca...")
    await status.send()

    for cycle in range(MAX_CYCLES):
        status.content = f"🔍 Ricerca in corso... ({cycle + 1}/{MAX_CYCLES})"
        await status.update()

        analysis = ask_llm(
            ANALYSIS_PROMPT.format(query=current_query),
            model=Config.LLM_MODEL_LOW,
            temperature=0.0
        )
        running_summary.append(analysis)

        next_query = ask_llm(
            NEXT_RESEARCH_PROMPT.format(
                original_query=original_query,
                running_summary="\n\n".join(running_summary)
            ),
            model=Config.LLM_MODEL_LOW,
            temperature=0.0
        ).strip()

        if next_query.upper() == "STOP" or not next_query or next_query in searched_queries:
            break

        searched_queries.add(next_query)
        current_query = next_query

    status.content = "🧠 Elaborazione risposta finale..."
    await status.update()

    final_answer = ask_llm(
        FINAL_SUMMARY_PROMPT.format(
            original_query=original_query,
            running_summary="\n\n".join(running_summary)
        ),
        model=Config.LLM_MODEL,
        temperature=0.0
    )

    await cl.Message(content=final_answer).send()