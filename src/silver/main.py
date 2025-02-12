import os
import glob
import re
from typing import List

from src.silver.classifier import SentimentClassifier
from src.services.llm import call_gpt
from src.utils.setup import Setup, SetupPersonalProfessional, SetupStrengthsWeaknesses, SetupRecommendation
from src.utils.util import timing_decorator
from src.utils.logger import logger


def sort_files(path_base: str):
    files = glob.glob(os.path.join(path_base, "*.csv"))
    default = re.compile(r"_(\d+)\.csv$")

    def sort_key(nome_arquivo):
        cor = default.search(nome_arquivo)
        if cor:
            return int(cor.group(1))
        return 0

    return sorted(files, key=sort_key)



@timing_decorator
def enrichment(files: List[str]):
    total_files = len(files)
    logger.info(f"Total files {total_files}")
    for file in files:
        try:
            SentimentClassifier(path_file=file, setup=SetupPersonalProfessional(), llm=call_gpt).run()
            SentimentClassifier(path_file=file, setup=SetupStrengthsWeaknesses(), llm=call_gpt).run()
            SentimentClassifier(path_file=file, setup=SetupRecommendation(), llm=call_gpt).run()
            total_files = total_files - 1
            logger.info(f"Still {total_files} files missing")
        except Exception as e:
            logger.error(f"Error file: {file}")
            raise e


if __name__ == "__main__":
    setup = Setup()
    files = sort_files(path_base=setup.path_bronze)
    enrichment(files=files)
