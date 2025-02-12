import os
from typing import Tuple
from datetime import  datetime

import pandas as pd

from src.utils.util import timing_decorator


@timing_decorator
def get_info_prompt(conn) -> str:
    query = """
    SELECT
           (select description from versions_prompts where name = 'personal_professional' and version = split_part(version_personal_professional, '/', 2)) prompt_personal_professional,         
           version_personal_professional,
           (select description from versions_prompts where name = 'strengths_weaknesses' and version = split_part(version_strengths_weaknesses, '/', 2)) prompt_strengths_weaknesses,
           version_strengths_weaknesses,
           (select description from versions_prompts where name = 'recommendation' and version = split_part(version_recommendation, '/', 2)) prompt_recommendation,
           version_recommendation
       FROM influencer_review 
       LIMIT 1;
    """
    df = conn.execute(query).df()
    msg = ("## Analise de sentimentos que foram usados GenAi: \n"
           "### Pessoal / Profissional:\n  "
           f"**Versão:** {df['version_personal_professional'][0]} \n"
           f"**Prompt:** \n:   {df['prompt_personal_professional'][0]} \n"
           "### Pontos fortes / Pontos fracos:\n "
           f"Versão: {df['version_strengths_weaknesses'][0]} \n"
           f"**Prompt:**  \n: {df['prompt_personal_professional'][0]} \n"
           "### Recomenda trabalhar com o influencer:\n"
           f"**Versão:** {df['version_recommendation'][0]}  \n"
           f"**Prompt:**  \n: {df['prompt_recommendation'][0]} \n"
           )

    return msg


@timing_decorator
def get_info_table(conn) -> Tuple[pd.DataFrame, pd.DataFrame]:
    sample_data = conn.execute("select * from influencer_review limit 10").df()
    schema = conn.execute("DESCRIBE influencer_review;").df()
    return sample_data, schema


def write_readme(conn):
    _, schema = get_info_table(conn)

    schema = schema.to_markdown()
    info_prompt = get_info_prompt(conn)
    msg = ("# Assistente de analise de avaliações de influencer \n"
           "Eu sou um assistente que usa IA Generativa para ajudar a realizar query e analises de avaliações de influencers"
           "A fonte de dados é uma planinha vazada com avaliações de diversos influencers em janeiro de 2025  \n"
           "## Descrição dos campos da tabela influencer_review:  \n"
           "- nickname: Nome utilizado nas redes sociais. \n"
           "- name: Nome do influencer. \n"
           "- personality: Análise de sentimento relacionada a personalidade do influencer, como ele se relaciona com \n"
           " as pessoas, retornando a classificação (Vide Analise de sentimento.)"
           "- professional: Análise de sentimento relacionada ao profissionalismo do influencer, retornando a "
           "classificação. (Vide Analise de sentimento.) \n"
           "- recommends_influencer:  Qual é a recomendação sobre o influencer. (Vide Analise de sentimento.)\n"
           "- strengths: Pontos fortes do influencer é uma lista pode conter 0 ou N, conforme foi classificado. \n"
           "- weaknesses: Pontos fracos do influencer, é uma lista pode conter 0 ou N  conforme foi classificado. \n"
           "- datetime: Data da avaliação do influencer. \n"
           "- evaluation_note: Nota atribuída ao influencer.\n"
           "- review: Relato detalhado da experiência de trabalhar com o influencer. \n"
           "- recommendation: Recomendações e dicas para colegas sobre o influencer. \n"
           )
    msg = msg + f"## Schema da tabela:\n {schema} \n "
    msg = msg + info_prompt
    open("chainlit.md", "w").write(msg)


def save_versions_prompts(conn, directory):
    """
    Recursively opens each file within the specified directory.

    Args:
        directory (str): The path to the root directory.
    """
    cmd = """
    CREATE TABLE IF NOT EXISTS versions_prompts (
        name VARCHAR,
        version VARCHAR,
        description VARCHAR,
        datetime_modified TIMESTAMP
    );
    """
    conn.execute(cmd)
    conn.execute("delete from versions_prompts")

    for root, subdirectories, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            try:
                with open(full_path, 'r') as f:  # Open the file for reading ('r')
                    contents = f.read()
                    name, version = full_path.split("/")[-2:]
                    insert = f"""INSERT INTO versions_prompts (name, version, description, datetime_modified)
                                VALUES ('{name}', '{version.replace('.txt', '')}', '{contents}', '{datetime.now()}');"""
                    conn.execute(insert)
            except Exception as e:
                print(f"Error opening file {full_path}: {e}")
