# Análise de Planilha com Avaliações de Influenciadores Digitais do Brasil

## **Introdução**
Em janeiro de 2025, vazou uma planilha contendo avaliações supostamente realizadas por profissionais que trabalham em agências de marketing. Essas avaliações abrangem diversos influenciadores digitais do Brasil, fornecendo insights sobre experiências de colaboração profissional.

A partir do conteúdo do PDF divulgado, foi criado um formulário no Google Forms para reunir mais feedback de profissionais da área, que compartilharam suas experiências ao trabalhar com diferentes influenciadores.

## **Objetivo do Projeto**
O objetivo principal deste projeto é explorar o potencial dos Large Language Models (LLMs), como o GPT, para:

- Análise de sentimentos em avaliações textuais.
- Extração e exploração de dados relevantes.
- Geração de insights para entender padrões de comportamento e profissionalismo de influenciadores.

## **Ferramentas e Tecnologias Utilizadas**
- **Python**: Linguagem principal para o processamento de dados.
- **tabula-py**: Biblioteca utilizada para extrair dados de arquivos PDF em formato tabular.
- **OpenAI GPT-4 API (gpt-4-turbo-mini)**: Modelo de linguagem utilizado para classificação e análise dos reviews.

## **Etapas do Projeto**
1. **Extração de Dados:**
   - Conversão do PDF contendo as avaliações em um formato estruturado (CSV) usando a biblioteca `tabula-py`.

2. **Processamento e Limpeza:**
   - Tratamento dos dados extraídos para padronizar informações e remover inconsistências.

3. **Análise com LLM:**
   - Classificação das avaliações em termos de:
     - Sentimento (positivo, negativo, neutro)
     - Personalidade (amistosa, hostil, neutra)
     - Profissionalismo (profissional, não profissional, neutro)

4. **Geração de Insights:**
   - Identificação de padrões comportamentais e avaliações frequentes.

## **Próximos Passos**
- Refinar a classificação com técnicas adicionais de machine learning.
- Desenvolver visualizações gráficas para os insights.
- Explorar outras bibliotecas de NLP para comparação de resultados.

## **Como Contribuir**
Se você tem interesse em colaborar com o projeto, sinta-se à vontade para abrir issues ou enviar pull requests.

## **Licença**
Este projeto está licenciado sob a [MIT License](LICENSE).

---
Este projeto busca mostrar como a inteligência artificial pode ser uma poderosa aliada na análise de dados qualitativos, abrindo novas possibilidades para a indústria de marketing digital.

