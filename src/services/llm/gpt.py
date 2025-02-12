import io
from typing import List

import openai
import pandas as pd

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
