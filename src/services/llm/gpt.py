import io
import json
from typing import List

import openai
import pandas as pd
from openai import AsyncOpenAI

from src.utils.dto import ConfigModel, GPTPrompt
from src.utils.logger import logger
from src.utils.util import timing_decorator


@timing_decorator
def call_gpt(messages: List, config: ConfigModel = ConfigModel()) -> pd.DataFrame:
    try:
        GPTPrompt(messages=messages)
    except Exception as e:
        logger.error(f" Invalid messages {messages}")
        raise e

    resp = openai.chat.completions.create(
        model=config.model,
        messages=messages,
        temperature=config.temperature
    )

    response = resp.choices[0].message.content.strip()
    logger.info("Success response GPT")
    data = io.StringIO(response)
    return pd.read_json(data)


def set_history(cl, prompt: str, role: str) ->list:
    history = cl.user_session.get("history", [])
    history.append({"role": role, "content": prompt})
    cl.user_session.set("history", history[-8:])
    return cl.user_session.get("history", [])


@timing_decorator
async def call_gpt_async(cl, content_system: str, content_user: str):
    client = AsyncOpenAI()
    history = set_history(cl, prompt=content_user, role="user")
    messages = [{
                "content": content_system,
                "role": "system"
            }] + history
    config = ConfigModel()
    response = await client.chat.completions.create(
        messages=messages,
        model=config.model,
        temperature=config.temperature
    )
    gpt_reply = response.choices[0].message.content
    try:
        data = json.loads(gpt_reply)
    except Exception as e:
        data = {"explain": gpt_reply, "suggestion": "", "query": ""}
        logger.error(e)
    set_history(cl, prompt=data["resume"], role="assistant")
    return data
