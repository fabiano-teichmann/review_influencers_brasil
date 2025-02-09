import os

import duckdb
from datetime import datetime

from src.gold.personal_professional import PersistPersonalProfessional
from src.gold.recommendation import PersistRecommendation
from src.gold.strengths_weaknesses import PersistStrengthsWeaknesses
from src.utils.setup import SetupRecommendation, SetupStrengthsWeaknesses, SetupPersonalProfessional


def save_versions_prompts(directory):
    """
    Recursively opens each file within the specified directory.

    Args:
        directory (str): The path to the root directory.
    """
    cmd = """
    CREATE TABLE IF NOT EXISTS versions_prompts (
        name VARCHAR,
        version VARCHAR,
        description VARCHAR,
        datetime_modified TIMESTAMP
    );
    """
    conn.execute(cmd)
    conn.execute("delete from versions_prompts")

    for root, subdirectories, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            try:
                with open(full_path, 'r') as f:  # Open the file for reading ('r')
                    contents = f.read()
                    name, version = full_path.split("/")[-2:]
                    insert = f"""INSERT INTO versions_prompts (name, version, description, datetime_modified)
                                VALUES ('{name}', '{version.replace('.txt', '')}', '{contents}', '{datetime.now()}');"""
                    conn.execute(insert)
            except Exception as e:
                print(f"Error opening file {full_path}: {e}")



def merge_data():

    query = """select 
                    pp.hash,
                    nickname,
                    name,
                    personality,
                    professional,
                    pp.version_personal_professional,
                    strengths,
                    weaknesses,
                    version_strengths_weaknesses,
                    recommends_influencer,
                    r.version_recommendation,
                    datetime,
                    evaluation_note,
                    date_work,
                    review,
                    recommendation, 
                    now() as data_processing
                from personal_professional pp
                left join strengths_weaknesses sw on pp.hash = sw.hash
                left join recommendation r on r.hash = pp.hash
    """
    temp_table = "temp_gold"
    table_name = "influencer_review"
    query = f"CREATE OR REPLACE TEMP TABLE {temp_table} AS ({query})"
    conn.execute(query)

    conn.execute(f"""
               CREATE TABLE IF NOT EXISTS {table_name} AS 
               SELECT * FROM {temp_table} WHERE false;
    """)

    conn.execute(f"""
                DELETE FROM {table_name}
                WHERE hash IN (SELECT hash FROM {temp_table});
            """)

    conn.execute(f"""
                INSERT INTO {table_name}
                SELECT * FROM {temp_table};
            """)



if __name__ == "__main__":
    PersistPersonalProfessional(setup=SetupPersonalProfessional()).run()
    PersistStrengthsWeaknesses(setup=SetupStrengthsWeaknesses()).run()
    PersistRecommendation(setup=SetupRecommendation()).run()
    conn = duckdb.connect(database='data/gold/influencer.duckdb', read_only=False)
    merge_data()
    save_versions_prompts("src/silver/prompt/prompts")
    conn.close()