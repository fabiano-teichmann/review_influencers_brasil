import duckdb

conn = duckdb.connect(database='data/gold/influencer.duckdb', read_only=False)