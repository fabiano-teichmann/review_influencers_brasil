import glob
import os
import re


def get_list_files_csv(path_dir: str) -> list:
    files = glob.glob(os.path.join(path_dir, "*.csv"))
    default = re.compile(r"_(\d+)\.csv$")

    def sort_key(nome_arquivo):
        cor = default.search(nome_arquivo)
        if cor:
            return int(cor.group(1))
        return 0

    return sorted(files, key=sort_key)
