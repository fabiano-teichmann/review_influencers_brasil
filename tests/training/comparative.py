import os
from datetime import  datetime

import pandas as pd



def highlight_if_has_diff(row, cols: list):
    """
    merged['diff'] = merged.apply(lambda row: 'false' if celse 'true', axis=1)
    merged['diff_personality'] = merged.apply(lambda row: 'false' if row[cols[4]] == row[cols[5]] else 'true', axis=1)
    """
    if row[cols[2]] != row[cols[3]] and  row[cols[4]] != row[cols[5]]:
        return ['background-color: red; color: black;'] * len(row)
    elif row[cols[2]] != row[cols[3]]:
        return ['background-color: yellow; color: black;'] * len(row)

    elif row[cols[4]] != row[cols[5]]:
        return ['background-color: orange; color: black;'] * len(row)

    else:
        return ['background-color: green; color: black;'] * len(row)

def compare_diff(path1: str, path2: str):
    name = f"compare{version1}_with_{version2}.html"
    model1, v1, _ = path1.split("/")[-3 : ]
    model2, v2, _ = path2.split("/")[-3:]
    df1 = pd.read_csv(path1, delimiter=";")
    df2 = pd.read_csv(path2, delimiter=";")
    file_report = os.path.join("tests/data", name)
    merged = df1.merge(df2, on=["nickname", "review"], suffixes=(version1, version2))
    cols = [
            "nickname",
            "review",
            f"professional{version1}",
            f"professional{version2}",
            f"personality{version1}",
            f"personality{version2}"
    ]
    df = merged[cols]
    styled_df = df.style.apply(lambda row: highlight_if_has_diff(row, cols), axis=1)

    styled_df.to_html(file_report, escape=False)
    html_content_with_meta = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Tabela com Legenda</title>
    </head>
    <body>
    """

    legend_html = f"""
        <div>
            <h1> Análise comparativa de resultados </h1> </br>
            <h3> Comparando Modelo: {model1} Versão Prompt: {version1} com Comparando Modelo: {model2} Versão Prompt: {version2} </h3>
            </br>
            <b> Data: {datetime.now()} </b>
            <h3>Legendas</h3>
            <ul>
                <li><span style="display: inline-block; width: 60px; height: 20px; background-color: green; color: white;">&#9608;</span> Sem divergência (verde)</li>
                <li><span style="display: inline-block; width: 60px; height: 20px; background-color: orange; color: white;">&#9608;</span> Divergência de personalidade (amarelo)</li>
                <li><span style="display: inline-block; width: 60px; height: 20px; background-color: yellow; color: black;">&#9608;</span> Divergência de profissionalismo (laranja)</li>
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

if __name__ == "__main__":
    path_v1 = "src/silver/data/personal_professional/gpt-4o-mini/v1/training.csv"
    path_v2 = "src/silver/data/personal_professional/gpt-4o-mini/v2/training.csv"
    version1 = "_" + path_v1.split("/")[-2]
    version2 = "_" + path_v2.split("/")[-2]
    compare_diff(path_v1, path_v2)


cols = ["nickname", "review", f"professional{version1}", f"professional{version2}", f"personality{version1}",
            f"personality{version2}"]
