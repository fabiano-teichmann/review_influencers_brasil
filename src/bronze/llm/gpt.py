import io
from typing import List

import openai
import pandas as pd

from src.utils.dto import ConfigModel, GPTPrompt


def call_gpt(config: ConfigModel, messages: List) -> pd.DataFrame:
    try:
        GPTPrompt(messages=messages)
    except Exception as e:
        print(f" Invalid messages {messages}")
        raise e

    resp = openai.chat.completions.create(
        model=config.model,
        messages=messages
    )

    response = resp.choices[0].message.content.strip()


    data = io.StringIO(response)
    return pd.read_json(data)
