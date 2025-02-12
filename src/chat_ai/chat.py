import json
from typing import Union

import duckdb
import pandas as pd
from openai import AsyncOpenAI
import chainlit as cl

from src.chat_ai.prompt import PromptChat
from src.utils.dto import ConfigModel
from src.utils.util import timing_decorator
from src.utils.logger import logger

client = AsyncOpenAI()

cl.instrument_openai()
config = ConfigModel()
conn = duckdb.connect(database='data/gold/influencer.duckdb', read_only=True)
prompt = PromptChat(conn)

@timing_decorator
async def call_llm(content: str):
    response = await client.chat.completions.create(
        messages=[
            {
                "content": prompt.prompt_role_system,
                "role": "system"
            },
            {
                "content": content,
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
    # conn = duckdb.connect(database='data/gold/influencer.duckdb', read_only=True)
    # prompt = PromptChat(conn)
    msg = ("Olá sou um Chat que um GenAi para lhe ajudar a fazer analise de dados de reviews de influencer, "
           "que foram avaliados supostamente por pessoas que trabalham com eles em campanhas de marketing. "
           "Em agências de marketing. \n")
    await cl.AskUserMessage(content=msg).send()


@timing_decorator
def get_result(query: str) -> Union[pd.DataFrame, str]:
    try:
        if query:
            df = conn.execute(query).df()
            print(query)
            return df
        return ""
    except Exception as e:
        logger.error(e)
        return str(e)

async def response_chat(data:dict):
    explain = data["explain"]
    suggestion = data["suggestion"]
    query = data["query"]
    elements = [
        cl.Text(name="Query", content=query, language="sql"),
        cl.Text(name="Sugestão", content=suggestion)
    ]
    actions = [
        cl.Action(
            name="action_run_query",
            icon="square-play",
            payload={"query": query},
            label="Executar"
        )
    ]
    await cl.Message(content=explain, elements=elements, actions=actions).send()


@timing_decorator
@cl.on_message
async def on_message(message: cl.Message):
    data = await call_llm(content=message.content)
    await  response_chat(data)


@cl.action_callback("action_run_query")
async def on_action(action: cl.Action):
    results = get_result(query=action.payload["query"])
    if isinstance(results, pd.DataFrame):
        actions = [
            cl.Action(
                name="action_analyze_data",
                icon="sparkle",
                payload={"query": action.payload["query"], "data": results.to_csv(index=False) },
                label="Analise os dados"
            )
        ]
        await cl.Message(content="Resultado",
                         actions=actions,
                         elements=[cl.Dataframe(name="Resultado query", data=results)]).send()

    else:
        actions = [
            cl.Action(
                name="action_fix_query",
                icon="circle-x",
                payload={"query": action.payload["query"], "error": results},
                label="Analise os dados"
            )
        ]
        await cl.Message(content="Erro rodar a query",
                         actions=actions,
                         elements=[cl.Text(name="Resultado query", content=results)]).send()

@cl.action_callback("action_analyze_data")
async def on_action_analyze_data(action: cl.Action):
    message = prompt.prompt_analyze_data(query=action.payload["query"], data=action.payload["data"])
    data = await call_llm(content=message)
    await cl.Message(content=data["explain"], elements=[cl.Text(name="Sugestão", content=data["suggestion"])]).send()


@cl.action_callback("action_fix_query")
async def on_fix_query(action: cl.Action):
    message = prompt.prompt_fix_query(query=action.payload["query"], error=action.payload["data"])
    data = await call_llm(content=message)
    await response_chat(data)



if __name__ == "__main__":
    from chainlit.cli import run_chainlit

    try:
        run_chainlit(__file__)
    except Exception as e:
        conn.close()
