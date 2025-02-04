from src.silver.classifier import SentimentClassifier


def run_sample_prompt(version: str, prompt_name: str):
    path = "tests/data/training.csv"
    SentimentClassifier(path_file=path, prompt_version=version, prompt_name=prompt_name).run()


if __name__ == "__main__":
    # personal_professional
    #run_sample_prompt(version="v1", prompt_name="personal_professional")
    #run_sample_prompt(version="v2", prompt_name="personal_professional")
    # strengths_weaknesses
    #run_sample_prompt(version="v1", prompt_name="strengths_weaknesses")
    #run_sample_prompt(version="v2", prompt_name="strengths_weaknesses")
    # recommendation
    run_sample_prompt(version="v1", prompt_name="recommendation")
