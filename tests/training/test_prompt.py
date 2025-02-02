from src.silver.main import SentimentClassifier


def test_prompt(version: str, prompt_name: str):
    path = "tests/data/training.csv"
    SentimentClassifier(path_file=path, prompt_version=version, prompt_name=prompt_name).run()


if __name__ == "__main__":
    test_prompt(version="v2", prompt_name="strengths_weaknesses")
