# Assistente de analise de avaliações de influencer 
Eu sou um assistente que usa IA Generativa para ajudar a realizar query e analises de avaliações de influencersA fonte de dados é uma planinha vazada com avaliações de diversos influencers em janeiro de 2025  
## Descrição dos campos da tabela influencer_review:  
- nickname: Nome utilizado nas redes sociais. 
- name: Nome do influencer. 
- personality: Análise de sentimento relacionada a personalidade do influencer, como ele se relaciona com 
 as pessoas, retornando a classificação (`positivo`, `negativo`, `neutro`, `misto`).- professional: Análise de sentimento relacionada ao profissionalismo do influencer, retornando a classificação (`positivo`, `negativo`, `neutro`, `misto`). 
- recommends_influencer:  Qual é a recomendação sobre o influencer (`positivo`, `negativo`, `neutro`, `misto`).
- strengths: Pontos fortes do influencer é uma lista pode conter 0 ou N, conforme foi classificado. 
- weaknesses: Pontos fracos do influencer, é uma lista pode conter 0 ou N  conforme foi classificado. 
- datetime: Data da avaliação do influencer. 
- evaluation_note: Nota atribuída ao influencer.
- review: Relato detalhado da experiência de trabalhar com o influencer. 
- recommendation: Recomendações e dicas para colegas sobre o influencer. 
## Schema da tabela:
 |    | column_name                   | column_type              | null   | key   | default   | extra   |
|---:|:------------------------------|:-------------------------|:-------|:------|:----------|:--------|
|  0 | hash                          | VARCHAR                  | YES    |       |           |         |
|  1 | nickname                      | VARCHAR                  | YES    |       |           |         |
|  2 | name                          | VARCHAR                  | YES    |       |           |         |
|  3 | personality                   | VARCHAR                  | YES    |       |           |         |
|  4 | professional                  | VARCHAR                  | YES    |       |           |         |
|  5 | version_personal_professional | VARCHAR                  | YES    |       |           |         |
|  6 | strengths                     | VARCHAR[]                | YES    |       |           |         |
|  7 | weaknesses                    | VARCHAR[]                | YES    |       |           |         |
|  8 | version_strengths_weaknesses  | VARCHAR                  | YES    |       |           |         |
|  9 | recommends_influencer         | VARCHAR                  | YES    |       |           |         |
| 10 | version_recommendation        | VARCHAR                  | YES    |       |           |         |
| 11 | datetime                      | VARCHAR                  | YES    |       |           |         |
| 12 | evaluation_note               | INTEGER                  | YES    |       |           |         |
| 13 | date_work                     | VARCHAR                  | YES    |       |           |         |
| 14 | review                        | VARCHAR                  | YES    |       |           |         |
| 15 | recommendation                | VARCHAR                  | YES    |       |           |         |
| 16 | data_processing               | TIMESTAMP WITH TIME ZONE | YES    |       |           |         | 
 ## Analise de sentimentos que foram usados GenAi: 
### Pessoal / Profissional:
  **Versão:** gpt-4o-mini/v2 
**Prompt:** 
:   Você é um assistente de AI, especializado em analisar dados de CSV que contem avaliações de pessoas que trabalharam com esses influencers
Sua tarefa é analisar os dados que contem os campos `hash` e `review` e retornar analise estruturada
Para cada linha você deve fazer a seguinte classificação:
1. `personality`: Analise o comportamento pessoal da pessoa analisada (exemplo: se a pessoa teve comportamento é gentil ou rude),
 quero que seja usado a seguinte classificação:  (`positivo`, `negativo`, `neutro`, `misto`),
 caso não consiga compreender o que foi escrito retorne como `indefinido`.
2. `professional`: Analise o comportamento profissional da pessoa avaliada (exemplo: se cumpre os prazos e briefing, Não quero aqui avaliar
 aqui o comportamento pessoal se a pessoa é gentil ou rude por exemplo) quero que seja usado a seguinte classificação: (`positivo`, `negativo`, `neutro`, `misto`),
 caso não consiga compreender o que foi escrito retorne como `indefinido`.
Seja conciso, mas preciso em suas avaliações.

Sempre retorne uma entrada para cada linha no CSV, mesmo que a análise seja `indefinido` para ambos os campos.
Retorne apenas a saída JSON sem texto adicional, formatação ou sintaxe de markdown.
 
### Pontos fortes / Pontos fracos:
 Versão: gpt-4o-mini/v2 
**Prompt:**  
: Você é um assistente de AI, especializado em analisar dados de CSV que contem avaliações de pessoas que trabalharam com esses influencers
Sua tarefa é analisar os dados que contem os campos `hash` e `review` e retornar analise estruturada
Para cada linha você deve fazer a seguinte classificação:
1. `personality`: Analise o comportamento pessoal da pessoa analisada (exemplo: se a pessoa teve comportamento é gentil ou rude),
 quero que seja usado a seguinte classificação:  (`positivo`, `negativo`, `neutro`, `misto`),
 caso não consiga compreender o que foi escrito retorne como `indefinido`.
2. `professional`: Analise o comportamento profissional da pessoa avaliada (exemplo: se cumpre os prazos e briefing, Não quero aqui avaliar
 aqui o comportamento pessoal se a pessoa é gentil ou rude por exemplo) quero que seja usado a seguinte classificação: (`positivo`, `negativo`, `neutro`, `misto`),
 caso não consiga compreender o que foi escrito retorne como `indefinido`.
Seja conciso, mas preciso em suas avaliações.

Sempre retorne uma entrada para cada linha no CSV, mesmo que a análise seja `indefinido` para ambos os campos.
Retorne apenas a saída JSON sem texto adicional, formatação ou sintaxe de markdown.
 
### Recomenda trabalhar com o influencer:
**Versão:** gpt-4o-mini/v1  
**Prompt:**  
: You are an AI assistant specialized in analyzing CSV data with influencer reviews you will analyze whether the influencer is recommended .
Your task is to analyze data from the fields `hash` and `recommendation`  and return a structured analysis.
Each row must have the following classifications:
1. `recommends_influencer`: Analyze whether the influencer is recommended return classify (`recomendado`, `recomendado com relvas`, `não recomendado`).
 or, if the text is incomprehensible, irrelevant, or lacks meaningful content, return `indefinido`.
Be concise but accurate in your evaluations.

**Example output:**
    ```[
       {"hash": "9c1c437a5c2a86695799a46292e9392418815810892792b94579cf152508b49c",
        "recommends_influencer": "recomendado",
        }
    ] ```

Return only the JSON output with no additional text, formatting, or markdown syntax as per the example above.
Always return an entry for each row in the CSV, even if the analysis is `indefinido` for both fields.

 
