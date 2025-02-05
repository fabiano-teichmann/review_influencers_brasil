import duckdb

from src.gold.personal_professional import PersistPersonalProfessional
from src.gold.recommendation import PersistRecommendation
from src.gold.strengths_weaknesses import PersistStrengthsWeaknesses
from src.utils.setup import SetupRecommendation, SetupStrengthsWeaknesses, SetupPersonalProfessional


def merge_data():
    conn = duckdb.connect(database='data/gold/influencer.duckdb', read_only=False)
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
    conn.close()


if __name__ == "__main__":
    PersistPersonalProfessional(setup=SetupPersonalProfessional()).run()
    PersistStrengthsWeaknesses(setup=SetupStrengthsWeaknesses()).run()
    PersistRecommendation(setup=SetupRecommendation()).run()
    merge_data()
