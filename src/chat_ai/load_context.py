import json
from typing import Tuple

import duckdb
import pandas as pd

from src.utils.util import timing_decorator

conn = duckdb.connect(database='data/gold/influencer.duckdb', read_only=True)

def load_readme() :
    _, schema = get_info_table()

    schema = schema.to_markdown()
    info_prompt = get_info_prompt()
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

@timing_decorator
def get_info_prompt() -> str:
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
def get_info_table() ->Tuple[pd.DataFrame, pd.DataFrame]:
    sample_data = conn.execute("select * from influencer_review limit 10").df()
    schema = conn.execute("DESCRIBE influencer_review;").df()
    return  sample_data, schema

@timing_decorator
def build_prompt_role_system() -> str:
    sample_data = conn.execute("select * from influencer_review limit 10").df().to_csv(index=False)
    schema = conn.execute("DESCRIBE influencer_review;").df().to_csv(index=False)

    prompt = f""" 
      # Contexto 
      Você é um assistente especializado em consultas SQL em bancos de dado DuckDB. 
      Especificamente para a tabela influencer_review.
      ## Informações sobre a tabela e como os dados foram gerados
      **Schema da tabela:**  ```{schema}``` csv
      **Amostra de dados:**  ```{sample_data}``` csv
     
      ** Descrição dos campos da tabela influencer_review:**
          - nickname: Nome utilizado nas redes sociais.
          - name: Nome do influencer.
          - personality: Análise de sentimento relacionada a personalidade do influencer, como ele se relaciona com as pessoas, retornando a classificação (`positivo`, `negativo`, `neutro`, `misto`).
          - professional: Análise de sentimento relacionada ao profissionalismo do influencer, retornando a classificação (`positivo`, `negativo`, `neutro`, `misto`).
          - recommends_influencer:  Qual é a recomendação sobre o influencer (`positivo`, `negativo`, `neutro`, `misto`) .
          - strengths: Pontos fortes do influencer é uma lista pode conter 0 ou N, conforme foi classificado.
          - weaknesses: Pontos fracos do influencer, é uma lista pode conter 0 ou N  conforme foi classificado.
          - datetime: Data da avaliação do influencer.
          - evaluation_note: Nota atribuída ao influencer.
          - review: Relato detalhado da experiência de trabalhar com o influencer.
          - recommendation: Recomendações e dicas para colegas sobre o influencer.

      # Objetivo    
      Seu objetivo é ajudar os usuários a formular queries SQL  com base nas perguntas recebidas se atentando ao schema da tabela,
      **recebido e verifique se a query é compatível com a sintaxe do SQL do DuckDB.**
      Caso a pergunta do usuário tenha ambiguidade, ou não esteja claro, retorne dizendo que não compreendeu corretamente 
      e de sugestões de perguntas
      **Para cada pergunta, você deve:**
        - Gerar uma query SQL que você que atenda à solicitação do usuário.
        - Fornecer uma explicação clara sobre o que a query faz.
        -  Sugerir perguntas adicionais para incrementar as análises.

      **Formato de resposta: **      
      Sua resposta deve ser um objeto JSON contendo os seguintes campos:
      "query": A query SQL sugerida.
      "explain": Uma explicação detalhada do que a query realiza.
      "suggestion": Sugestões de novas buscas ou melhorias na consulta.
      **Atenção:** Retorne apenas o objeto JSON, sem nenhum texto extra, formatação ou sintaxe de markdown.
      **Exemplo de resposta esperado:**

  """

    example_json = {
        "query": "SELECT nickname, COUNT(*) AS total_reviews, AVG(evaluation_note) AS nota_media FROM influencer_review GROUP BY nickname",
        "explain": "Esta query agrupa os registros por 'nickname', contando o número de avaliações e calculando a nota média para cada influencer.",
        "suggestion": "Você pode também analisar os reviews com notas abaixo da média ou filtrar os dados por períodos específicos."
    }

    prompt = prompt + json.dumps(example_json)
    print(prompt)
    return prompt
