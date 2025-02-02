from src.silver.main import SentimentClassifier
from src.utils.logger import logger


def test_training_gpt_personality_professional(version: str):
    path = "tests/data/training.csv"
    SentimentClassifier(path_file=path, prompt_version=version, prompt_name="personal_professional").run()


if __name__ == "__main__":
    test_training_gpt_personality_professional("v2")