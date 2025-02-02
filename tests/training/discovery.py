import pandas as pd


def discovery(path_file: str, field_name: str, value: str, cols):
    df = pd.read_csv(path_file, delimiter=";")
    df = df[df[field_name] == value]
    prompt = path_file.split("/")
    print(f"##### Discovery {prompt[3]} - {prompt[4]} #######")
    if cols:
        print(df[cols].to_markdown())
    else:
        print(df.to_markdown())
    print("#" * 200)


if __name__ == "__main__":
    cols = ["nickname", "review", "strengths", "weaknesses", "complaint", "evaluation_note"]
    path = "data/silver/data/strengths_weaknesses/gpt-4o-mini/v1/training.csv"
    discovery(path_file=path, field_name="nickname", value="@caiocastro", cols=cols)
