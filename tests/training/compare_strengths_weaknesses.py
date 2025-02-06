import os
from datetime import  datetime

import pandas as pd



def highlight_if_has_diff(row, cols: list):

    if row[cols[2]] != row[cols[3]] and row[cols[4]] != row[cols[5]] and row[cols[6]] != row[cols[7]]:
        return ['background-color: red; color: black;'] * len(row)
    elif row[cols[2]] != row[cols[3]] or row[cols[4]] != row[cols[5]] or row[cols[6]] != row[cols[7]]:
        return ['background-color: orange; color: black;'] * len(row)

    else:
        return ['background-color: green; color: black;'] * len(row)

def compare_diff(path1: str,
                 path2: str,
                 version1: str,
                 version2: str,
                 file_report: str,
                 dt: str,
                 cols: list):

    model1, v1, _ = path1.split("/")[-3 : ]
    model2, v2, _ = path2.split("/")[-3:]
    df1 = pd.read_csv(path1, delimiter=";")
    df2 = pd.read_csv(path2, delimiter=";")
    merged = df1.merge(df2, on=["nickname", "review"], suffixes=(version1, version2))
    df = merged[cols]
    styled_df = df.style.apply(lambda row: highlight_if_has_diff(row, cols), axis=1)

    styled_df.to_html(file_report, escape=False)
    html_content_with_meta = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Comparativo de prompts</title>
    </head>
    <body>
    """

    legend_html = f"""
        <div>
            <h1> Análise comparativa de resultados: strengths_weaknesses  </h1> </br>
            <h3> Comparando Modelo: {model1} Versão Prompt: {v1} com Comparando Modelo: {model2} Versão Prompt: {v2} </h3>
            </br>
            <b> Data: {dt} </b>
            <h3>Legendas</h3>
            <ul>
                <li><span style="display: inline-block; width: 60px; height: 20px; background-color: green; color: white;">&#9608;</span> Sem divergência (verde)</li>
                <li><span style="display: inline-block; width: 60px; height: 20px; background-color: orange; color: white;">&#9608;</span> Divergência em 1 ou 2 campos (laranja)</li>
                <li><span style="display: inline-block; width: 60px; height: 20px; background-color: red; color: white;">&#9608;</span> Divergência total (vermelho)</li>
            </ul>
        </div>
    """
    with open(file_report, 'r') as file:
        html_content = file.read()

    # Inserir a legenda antes da tabela
    html_content_with_legend = html_content_with_meta + legend_html + html_content
    with open(file_report, 'w') as file:
        file.write(html_content_with_legend)
    print(f"Diferenças salvas em {file_report}")


def strengths_weaknesses():
    path_v1 = "data/silver/data/strengths_weaknesses/gpt-4o-mini/v1/training.csv"
    path_v2 = "data/silver/data/strengths_weaknesses/gpt-4o-mini/v2/training.csv"
    version1 = "_" + path_v1.split("/")[-2]
    version2 = "_" + path_v2.split("/")[-2]
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    name = f"compare_strengths_weaknesses{version1}_with{version2}_{dt}.html"
    file_report = os.path.join("tests/data/diff/strengths_weaknesses", name)
    cols = [
        "nickname",
        "review",
        f"strengths{version1}",
        f"strengths{version2}",
        f"weaknesses{version1}",
        f"weaknesses{version2}",
        f"complaint{version1}",
        f"complaint{version2}",
    ]
    compare_diff(path1=path_v1,
                 path2=path_v2,
                 version1=version1,
                 version2=version2,
                 file_report=file_report,
                 dt=dt,
                 cols=cols)



if __name__ == "__main__":
    strengths_weaknesses()

