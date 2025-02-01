from src.bronze.main import SentimentClassifierGPT


def test_training_gpt(version: str):
    path = "tests/data/training.csv"
    SentimentClassifierGPT(path_file=path, version_prompt=version).run()


if __name__ == "__main__":
    test_training_gpt("v1")