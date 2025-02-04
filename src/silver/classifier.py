import os
from typing import  Callable

import pandas as pd

from src.silver.llm.gpt import call_gpt
from src.silver.prompt.prompt import Prompt
from src.utils.dto import ConfigModel
from src.utils.logger import logger


class SentimentClassifier:
    def __init__(self, path_file: str, prompt_version: str, prompt_name: str, llm: Callable = call_gpt):
        self.path_file = path_file
        self.version_prompt = prompt_version
        self.name_prompt = prompt_name
        self.model = ConfigModel()
        self.llm = llm

    def run(self):
        df = self.__load_data()
        csv_data_string = df.to_csv(index=False)
        prompt = Prompt(csv_data_string=csv_data_string, prompt_name=self.name_prompt,
                        prompt_version=self.version_prompt)
        messages = [
            {"role": "system",
             "content": prompt.system},
            {"role": "user",
             "content": prompt.user}
        ]
        df_response = self.llm(config=self.model, messages=messages)
        self.__save_data(df=df, df_response=df_response, prompt=prompt)

    def __load_data(self):
        logger.info(f"load file {self.path_file} ")
        df = pd.read_csv(self.path_file)
        df.columns = ["datetime", "name", "nickname", "evaluation_note",
                      "date_work", "review", "recommendation"]
        return df

    def __create_folder_if_not_exist(self, prompt: Prompt) -> str:
        path_base = os.path.join("data/silver/data/", prompt.name_prompt)
        if not os.path.isdir(path_base):
            os.mkdir(path_base)
        path_base = os.path.join(path_base, self.model.model)
        if not os.path.isdir(path_base):
            os.mkdir(path_base)
        dst_path = os.path.join(path_base, prompt.prompt_version)
        if not os.path.isdir(dst_path):
            os.mkdir(dst_path)
        return dst_path

    def __save_data(self, df: pd.DataFrame, df_response: pd.DataFrame, prompt: Prompt):
        dst_path = self.__create_folder_if_not_exist(prompt)
        dst_file = os.path.join(dst_path, os.path.split(self.path_file)[-1])
        df_final = pd.merge(df_response, df, on="nickname", how="inner")
        df_final.to_csv(dst_file, index=False, sep=";")
        logger.info(f"Salved with success file: {dst_file}")
