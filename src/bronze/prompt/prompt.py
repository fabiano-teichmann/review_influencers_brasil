import os

class Prompt:
    def __init__(self, csv_data_string : str, version_prompt: str):
        self.csv_data_string = csv_data_string
        self.version_prompt = version_prompt

    @property
    def user(self) -> str:
        return f"Analyze the following CSV data and classify each entry as instructed:\n```\n{self.csv_data_string}\n```"

    @property
    def system(self) -> str:
        path_base  = os.path.join("src/bronze/prompt/prompts", f"{self.version_prompt}.txt")
        prompt = open(path_base).read()
        return prompt
