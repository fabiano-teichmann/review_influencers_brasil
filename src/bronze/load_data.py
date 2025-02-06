import glob

from tabula import read_pdf
import pandas as pd

def generate_csv():
    pdf_path = "../../data/bronze/data/Planilha_de_influenciadores_respostas_Google_Drive_xlsx_Planilha.pdf"
    csv_path = "../../data/bronze/data/influencers_reviews.csv"

    # df = read_pdf(pdf_path, pages=1, pandas_options={"header": 1})
    tables = read_pdf(pdf_path, pages="all", lattice=True, multiple_tables=True)

    col = []
    for i, table in enumerate(tables):
        if i  == 0:
            col =  table.iloc[1]
            table = table[2:]
        try:
            table.columns = col
        except Exception as e:
            print(e)
            table = table.iloc[:, 0:7]
            table.columns = col
        table.to_csv(f"{csv_path}_table_{i+1}.csv", index=False)
        print(f"table {i+1} saved CSV.")


if __name__ == "__main__":
    generate_csv()