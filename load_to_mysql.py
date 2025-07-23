import pandas as pd
from sqlalchemy import create_engine


# ✅ Load your CSV
df = pd.read_csv(r"C:\Users\Ravi\Desktop\Desktop\Sample program\Test\imdb_movies_2024.csv")


# ✅ Create SQLAlchemy engine
engine = create_engine("mysql+pymysql://root:root@localhost/imdb_data")


# ✅ Optional: Rename/clean columns if needed before insertion
# df.columns = [col.lower().replace(' ', '_') for col in df.columns]

# ✅ Write DataFrame to SQL table
df.to_sql("imdb_movies", con=engine, if_exists="replace", index=False)
print("✅ Data inserted into MySQL using SQLAlchemy!")
