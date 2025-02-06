import os
import glob
import re
from typing import List

from src.silver.classifier import SentimentClassifier
from src.utils.setup import Setup
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
def enrichment(files: List[str], setup: Setup):
    total_files = len(files)
    logger.info(f"Total files {total_files}")
    for file in files:
        try:
            SentimentClassifier(path_file=file, prompt_version=setup.recommendation_version,
                                prompt_name="recommendation").run()
            SentimentClassifier(path_file=file, prompt_version=setup.personal_professional_version,
                                prompt_name="personal_professional").run()
            SentimentClassifier(path_file=file, prompt_version=setup.strengths_weaknesses_version,
                                prompt_name="strengths_weaknesses").run()
            total_files = total_files - 1
            logger.info(f"Still {total_files} files missing")
        except Exception as e:
            logger.error(f"Error file: {file}")
            raise e


if __name__ == "__main__":
    setup = Setup()
    files = sort_files(path_base=setup.path_bronze)
    enrichment(files=files, setup=setup)
