import os

import duckdb

from src.utils.list_files import get_list_files_csv
from src.utils.logger import logger
from src.utils.setup import SetupPersonalProfessional

class PersistPersonalProfessional:
    def __init__(self, setup: SetupPersonalProfessional):
        if not isinstance(setup, SetupPersonalProfessional):
            raise TypeError(f"Expected setup to be an instance of SetupPersonalProfessional, but got {type(setup).__name__}")
        self.setup = setup
        self.conn = duckdb.connect(database='data/gold/influencer.duckdb', read_only=False)
        self.files = self._get_files()

    def run(self):
        for file in self.files:
            self._save_results(file)
            logger.info(f"Ingested {file}")
        self.conn.close()


    def _get_files(self) -> list:
        path_files = os.path.join(self.setup.path_silver, self.setup.name, self.setup.model, self.setup.version)
        return get_list_files_csv(path_files)

    def _save_results(self, file: str):
        table_name = self.setup.name
        version = f"{self.setup.model}/{self.setup.version}"
        temp_table = 'temp_data'
        # self.conn.execute(f"drop table {table_name}")
        self.conn.execute(
            f"""
            CREATE OR REPLACE TEMP TABLE {temp_table} AS
            SELECT 
                    hash::VARCHAR AS hash, 
                    personality::VARCHAR AS personality,  
                    professional::VARCHAR AS professional, 
                    datetime::VARCHAR AS datetime,  
                    name::VARCHAR AS name,  
                    nickname::VARCHAR AS nickname,  
                    evaluation_note::INTEGER AS evaluation_note,  
                    date_work::VARCHAR AS date_work,  
                    review::VARCHAR AS review,
                    recommendation::VARCHAR AS recommendation, 
                   '{version}' AS version_{self.setup.name}
            FROM read_csv_auto('{file}', HEADER=TRUE, SEP=';')
        """)

        # Cria a tabela se não existir
        self.conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} AS 
            SELECT * FROM {temp_table} WHERE false;
        """)

        # Delete registros que já existem
        self.conn.execute(f"""
            DELETE FROM {table_name}
            WHERE hash IN (SELECT hash FROM {temp_table});
        """)

        # Insere os novos registros
        self.conn.execute(f"""
            INSERT INTO {table_name}
            SELECT * FROM {temp_table};
        """)
