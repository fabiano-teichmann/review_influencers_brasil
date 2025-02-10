import os
from typing import Callable, Union
import hashlib

import pandas as pd

from src.silver.llm.gpt import call_gpt
from src.silver.prompt.prompt import Prompt
from src.utils.dto import ConfigModel
from src.utils.logger import logger
from src.utils.setup import SetupPersonalProfessional, SetupStrengthsWeaknesses, SetupRecommendation
from src.utils.util import timing_decorator


def generate_hash(row):
    combined_string = str(row['datetime']) + str(row['nickname'])
    return hashlib.sha256(combined_string.encode()).hexdigest()


class SentimentClassifier:
    def __init__(self, path_file: str,
                 setup: Union[SetupPersonalProfessional, SetupStrengthsWeaknesses, SetupRecommendation],
                 llm: Callable = call_gpt):
        self.path_file = path_file
        self.version_prompt = setup.version
        self.name_prompt = setup.name
        self.model = ConfigModel()
        self.llm = llm

    def run(self):
        df = self.__load_data()
        csv_data_string = df.to_csv(index=False)
        prompt = Prompt(data_string=csv_data_string, prompt_name=self.name_prompt,
                        prompt_version=self.version_prompt)
        messages = [
            {"role": "system",
             "content": prompt.system},
            {"role": "user",
             "content": prompt.user}
        ]
        df_response = self.llm(config=self.model, messages=messages)
        self.__save_data(df=df, df_response=df_response, prompt=prompt)

    @timing_decorator
    def __load_data(self):
        logger.info(f"load file {self.path_file} ")
        df = pd.read_csv(self.path_file)
        df.columns = ["datetime", "name", "nickname", "evaluation_note",
                      "date_work", "review", "recommendation"]
        df['hash'] = df.apply(generate_hash, axis=1)
        return df

    def __create_folder_if_not_exist(self, prompt: Prompt) -> str:
        path_base = os.path.join("data/silver/data/", prompt.prompt_name)
        if not os.path.isdir(path_base):
            os.mkdir(path_base)
        path_base = os.path.join(path_base, self.model.model)
        if not os.path.isdir(path_base):
            os.mkdir(path_base)
        dst_path = os.path.join(path_base, prompt.prompt_version)
        if not os.path.isdir(dst_path):
            os.mkdir(dst_path)
        return dst_path

    @timing_decorator
    def __save_data(self, df: pd.DataFrame, df_response: pd.DataFrame, prompt: Prompt):
        dst_path = self.__create_folder_if_not_exist(prompt)
        dst_file = os.path.join(dst_path, os.path.split(self.path_file)[-1])
        total_input = df.count()["hash"]
        total_output = df_response.count()["hash"]
        df_final = pd.merge(df_response, df, on="hash", how="left")
        total_final = df_final.count()["hash"]
        try:
            assert total_input == total_output
        except AssertionError:
            logger.warning(
                f'DIFF total records input {total_input} records output {total_output}')
        try:
            assert total_final == total_output
        except AssertionError as e:
            logger.error(
                f'DIFF total records input {total_input} records output {total_output}, records final {total_final}')
            raise e
        df_final.to_csv(dst_file, index=False, sep=";")
        logger.info(f"Salved with success file: {dst_file}")
