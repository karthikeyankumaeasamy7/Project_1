import pandas as pd
import mysql.connector
import re

# ✅ Load CSV
csv_file = r"C:\Users\Ravi\Desktop\Desktop\Sample program\Test\imdb_movies_2024.csv"
df = pd.read_csv(csv_file)
print(f"✅ Loaded rows: {len(df)}")

# ✅ Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",   # change if needed
    database="imdb_data"
)
cursor = conn.cursor()

# ✅ Create table if not exists
cursor.execute("DROP TABLE IF EXISTS imdb_movies")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS imdb_movies (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        rating FLOAT,
        vote INT,
        duration INT,
        storyline TEXT
    )
""")

# ✅ Clean + Insert data row-by-row
for index, row in df.iterrows():
    try:
        # --- Clean Votes ---
        vote_str = str(row['Votes']).strip().replace('(', '').replace(')', '').replace(',', '')
        if 'K' in vote_str:
            vote = int(float(vote_str.replace('K', '')) * 1000)
        else:
            vote = int(vote_str)

        # --- Clean Duration: "1h 30m" -> total minutes
        duration_str = str(row['Duration'])
        h, m = 0, 0
        if 'h' in duration_str:
            h_match = re.search(r'(\d+)h', duration_str)
            if h_match:
                h = int(h_match.group(1))
        if 'm' in duration_str:
            m_match = re.search(r'(\d+)m', duration_str)
            if m_match:
                m = int(m_match.group(1))
        duration = h * 60 + m

        # --- Insert into MySQL ---
        cursor.execute("""
            INSERT INTO imdb_movies (title, rating, vote, duration, storyline)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            row['Title'],
            float(row['Rating']),
            vote,
            duration,
            row['Storyline']
        ))

    except Exception as e:
        print(f"❌ Error at row {index}: {e}")

# ✅ Finalize
conn.commit()
cursor.close()
conn.close()
print("✅ All rows inserted into MySQL!")