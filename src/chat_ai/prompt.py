import json

class PromptChat:
    def __init__(self, conn):
        self.conn = conn
        self.sample_data = self.conn.execute("select * from influencer_review limit 25").df().to_csv(index=False)
        self.schema = self.conn.execute("DESCRIBE influencer_review;").df().to_csv(index=False)


    def prompt_fix_query(self, query: str, error: str):
        prompt = f"""       
        # Objetivo:
        Analise a query ```{query}``` gerada que foi executada no banco de dados DuckDB. Ela está com o 
        erro: ```{error} ```, corrija o erro na query atentado para a  ** Semântica do DuckDB** retornando o a nova query
        em ```query```
        em ```explain`` coloque a explicação do erro e o que a foi feito para corrigir o erro, 
        em```suggestion``` coloque outras opções para resolver o problema
        
        
        """
        return  prompt + self.example_response_expected

    def prompt_analyze_data(self, query: str, data: str) -> str:
        return f"""
            # Objetivo:
            A query ```{query}``` gerou esse resultado ```{data}``` CSV, faça uma analise desses resultados levando em conta o 
            contexto passado sobre essa base de dados.
            Retornando sua analise em ```explain``` e também retonado sugesntões de analises em ```suggestion```
        """

    @property
    def context(self) -> str:
        return f"""
         # Contexto 
          Você é um assistente especializado em consultas SQL em bancos de dado DuckDB. 
          Especificamente para a tabela influencer_review. Que contém avaliações feita por pessoas que trabalharam com 
          esses influencer onde é feito uma classificação de sentimento das caracteristicas Pessoal / Profissional (personality, professional)
          Pontos Fortes / Pontos Fracos (strengths, weaknesses), recomendação a colegas (recommends_influencer)
          ## Informações sobre a tabela e como os dados foram gerados
          **Schema da tabela:**  ```{self.schema}``` csv
          **Amostra de dados:**  ```{self.sample_data}``` csv
        """

    @property
    def example_response_expected(self) -> str:
        result_expected = """
         **Formato de resposta: **      
          Sua resposta deve ser um objeto JSON contendo os seguintes campos:
          "query": A query SQL sugerida. Quero que ela esteja com indentação
          "explain": Uma explicação detalhada do que a query realiza.
          "suggestion": Sugestões de novas buscas ou melhorias na consulta.
          **Atenção:** Retorne apenas o objeto JSON, sem nenhum texto extra, formatação ou sintaxe de markdown.
          Adicione um limite de 100 registros
          **Exemplo de resposta esperado:**
          
        """

        example =  json.dumps({
            "query": "SELECT nickname, COUNT(*) AS total_reviews FROM influencer_review GROUP BY nickname",
            "explain": "Esta query agrupa os registros por 'nickname', contando o número de avaliações e calculando a nota média para cada influencer.",
            "suggestion": "Você pode também analisar os reviews com notas abaixo da média ou filtrar os dados por períodos específicos.",
        }, indent=4)
        return  result_expected + example

    @property
    def prompt_role_system(self) -> str:
        prompt = f""" 
          {self.context}
         
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
          **Atenção**  Nas queries retorne somente  os campos citados acima  
          # Objetivo    
          Seu objetivo é ajudar os usuários a formular queries SQL  com base nas perguntas recebidas se atentando ao schema da tabela,
          **recebido e verifique se a query é compatível com a sintaxe do SQL do DuckDB.**
          Caso a pergunta do usuário tenha ambiguidade, ou não esteja claro, retorne dizendo que não compreendeu corretamente 
          e de sugestões de perguntas
          **Para cada pergunta, você deve:**
            - Gerar uma query SQL que você que atenda à solicitação do usuário.
            - Fornecer uma explicação clara sobre o que a query faz.
            - Sugerir perguntas adicionais para incrementar as análises.
          Pesquisas sobre nome do influencer use ILIKE         
     
        """
        prompt = prompt + self.example_response_expected
        print(prompt)
        return prompt
