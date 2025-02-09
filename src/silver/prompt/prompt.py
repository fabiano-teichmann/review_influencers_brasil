import os

from src.utils.logger import logger


class Prompt:
    def __init__(self,
                 data_string: str,
                 prompt_name: str,
                 prompt_version: str, ):
        """

        :param data_string: data to send to llm
        :param prompt_name: name prompt used to create folder in silver
        :param prompt_version:  version name used create folder inside in name_prompt


        """
        self.data_string = data_string
        self.name_prompt = prompt_name
        self.prompt_version = prompt_version

    @property
    def user(self) -> str:
        return (f"Analyze the following CSV data and classify each entry as"
                f" instructed:\n```\n{self.data_string}\n```")

    @property
    def system(self) -> str:
        path_file = os.path.join("src/silver/prompt/prompts",
                                 self.name_prompt,
                                 f"{self.prompt_version}.txt")
        try:
            prompt = open(path_file).read()
            return prompt
        except FileNotFoundError:
            logger.error(f"Not found prompt {self.name_prompt} with version {self.prompt_version}")
            raise FileNotFoundError(path_file)
