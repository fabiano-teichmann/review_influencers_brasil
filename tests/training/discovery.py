import os
import pandas as pd


def discovery(path_file: str, field_name: str, value: str, cols=None):
    if cols is None:
        cols = ["nickname", "review", "personality", "professional", "evaluation_note"]
    df = pd.read_csv(path_file, delimiter=";")
    df = df[df[field_name] == value]
    prompt = path_file.split("/")
    # print(f"##### Discovery {prompt[3]} - {prompt[4]} #######")
    print(df[cols].to_markdown())
    print("#" * 200)


if __name__ == "__main__":
    path_v1 = "src/silver/data/personal_professional/gpt-4o-mini/v1/training.csv"
    path_v2 = "src/silver/data/personal_professional/gpt-4o-mini/v2/training.csv"
    discovery(path_v1, "nickname", "@caiocastro")
    discovery(path_v2, "nickname", "@caiocastro")
