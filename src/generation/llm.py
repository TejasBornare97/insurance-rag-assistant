"""
The only place that talks to the language model.

Everything else calls generate(). To switch to a hosted model later
(OpenAI, Claude, Azure OpenAI), change this file only.
"""

import ollama

from src.config import LLM_MODEL


def generate(system_prompt, user_prompt):
    """Send a system prompt and a user prompt to the model and return its reply.

    temperature=0 makes the model pick the most likely words every time, so the
    same question gives the same answer. For factual answers about policy
    cover we want consistency, not creativity.
    """
    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        options={"temperature": 0},
    )
    return response["message"]["content"].strip()
