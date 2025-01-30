import io
import glob
import os
import re
import openai
import pandas as pd
from pydantic import BaseModel


class ConfigAgent(BaseModel):
    model: str = "gpt-4o-mini"
    instruct: str = "Todas as respostas devem ser respondidas em português brasileiro com o máximo de 500 palavras"


config = ConfigAgent()

files_csv = glob.glob("raw/*.csv")


def extract_number(file):
    match = re.search(r'(\d+)', file)
    return int(match.group()) if match else 0


def load_dataframe(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = ["datetime", "name", "nickname", "evaluation_note", "date_work", "review", "recommendation"]
    return df

def classify_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    df = df[["nickname", "review"]]
    messages = [
        {"role": "system",
         "content": (
             "You are an AI assistant specialized in analyzing CSV data with influencer reviews to classify reviews."
             " Your task is to analyze data from the fields `nickname` and `review` and return a structured analysis."
             " Each row must have the following classifications:"
             "\n2. `personality`: Assess whether the reviews reflects a positive, negative, or neutral personality (e.g., friendly vs rude)."
             "\n3. `professional`: Assess whether the behavior displayed by the person being evaluated is considered professional, unprofessional or not reported."
             " Be concise but accurate in your evaluations. Return only result delimited by ','"
         )},
        {"role": "user",
         "content": f"Analyze the table below and classify each entry as instructed:\n```\n{df.to_markdown()}\n```"}
    ]
    resp = openai.chat.completions.create(
        model=config.model,
        messages=messages)
    response = resp.choices[0].message.content
    csv_data = io.StringIO(response)
    return pd.read_csv(csv_data)

if __name__ == "__main__":
    files_csv_sorted = sorted(files_csv, key=extract_number)
    df = load_dataframe(files_csv_sorted[0])
    dst = os.path.join("bronze", os.path.split( files_csv_sorted[0])[-1])
    df_classify = classify_sentiment(df)
    df_classify.columns = ['nickname', 'sentiment', 'personality', 'professional']
    try:
        merged_df = pd.merge(df, df_classify, on='nickname', how='inner')
        merged_df.to_csv(dst)
    except:
        df_classify.to_csv(dst)


