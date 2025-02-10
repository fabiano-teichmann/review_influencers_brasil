import json
from typing import Union

import duckdb
import pandas as pd
from openai import AsyncOpenAI
import chainlit as cl

from src.chat_ai.load_context import build_prompt_role_system, load_readme
from src.utils.dto import ConfigModel
from src.utils.util import timing_decorator
from src.utils.logger import logger

client = AsyncOpenAI()

cl.instrument_openai()
config = ConfigModel()
conn = duckdb.connect(database='data/gold/influencer.duckdb', read_only=True)
prompt_role_system = build_prompt_role_system()


@timing_decorator
async def call_llm(message):
    response = await client.chat.completions.create(
        messages=[
            {
                "content": prompt_role_system,
                "role": "system"
            },
            {
                "content": message.content,
                "role": "user"
            }
        ],
        model=config.model,
        temperature=config.temperature
    )
    gpt_reply = response.choices[0].message.content
    data = json.loads(gpt_reply)
    return data




@cl.on_chat_start
async def main():
   msg = ("Olá sou um Chat que um GenAi para lhe ajudar a fazer analise de dados de reviews de influencer, "
          "que foram avaliados supostamente por pessoas que trabalham com eles em campanhas de marketing. "
          "Em agências de marketing. \n")
   await cl.AskUserMessage(content=msg).send()


@timing_decorator
def get_result(query: str) -> Union[pd.DataFrame, str ]:
    try:
        if query:
            df = conn.execute(query).df()
            print(query)
            return df
        return ""
    except Exception as e:
        logger.error(e)
        return f'Não foi possivel realizar a query: `{query}`, Erro : {e}'


@timing_decorator
@cl.on_message
async def on_message(message: cl.Message):
    data  = await call_llm(message)
    explain = data["explain"]
    suggestion = data["suggestion"]
    query = data["query"]
    print(data["plot"])
    results = get_result(query)

    if isinstance(results, pd.DataFrame):
        elements = [
            cl.Text(name="Query", content=query, language="sql"),
            cl.Text(name="Explicação", content=explain),
            cl.Text(name="Resultado", content=results.to_markdown()),
            cl.Text(name="Sugestão", content=suggestion)
        ]
        await cl.Message(content=explain,
                         elements=elements
                         ).send()

    else:
        await cl.Message(content=results,
                         elements=[
                             cl.Text(name="Query", content=query, display="inline", language="sql"),
                             cl.Text(name="Explicação", content=explain, display="inline"),
                             cl.Text(name="Sugestão", content=suggestion, display="inline")
                         ]
                         ).send()

if __name__ == "__main__":
    from chainlit.cli import run_chainlit

    try:
        load_readme()
        run_chainlit(__file__)
    except Exception as e:
        conn.close()
