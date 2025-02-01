import os

import pandas as pd

from src.bronze.llm.gpt import call_gpt
from src.bronze.prompt.prompt import Prompt
from src.utils.dto import ConfigModel


class SentimentClassifierGPT:
    def __init__(self, path_file: str, version_prompt: str):
        self.path_file = path_file
        self.version_prompt = version_prompt

    def run(self):
        df = self.__load_data()
        csv_data_string = df.to_csv(index=False)
        prompt = Prompt(csv_data_string, self.version_prompt)
        messages = [
            {"role": "system",
             "content": prompt.system},
            {"role": "user",
             "content": prompt.user}
        ]
        df_response = call_gpt(config=ConfigModel(), messages=messages)
        self.__save_data(df=df, df_response=df_response)

    def __load_data(self):
        df = pd.read_csv(self.path_file)
        df.columns = ["datetime", "name", "nickname", "evaluation_note", "date_work", "review", "recommendation"]
        return df

    def __save_data(self, df: pd.DataFrame, df_response: pd.DataFrame):
        dst_path = "src/bronze/data/v1"
        if not os.path.isdir(dst_path):
            os.mkdir(dst_path)
        dst_file = os.path.join(dst_path, os.path.split(self.path_file)[-1])
        df_final = pd.merge(df, df_response, on="nickname", how="left")
        df_final.to_csv(dst_file, index=False, sep=";")
