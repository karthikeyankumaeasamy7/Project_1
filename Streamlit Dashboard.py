import streamlit as st
import pandas as pd
import mysql.connector
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt

# Set page layout
st.set_page_config(page_title="IMDb Dashboard", layout="wide")

st.title("🎬 Simple IMDb 2024 Dashboard")

# Connect to MySQL and fetch data
try:
    #conn = mysql.connector.connect(
    #    host="localhost",
    #    user="root",
    #    password="root",
    #    database="imdb_data"
    #)
    df = pd.read_csv("imdb_movies_2024.csv")
    df.columns = df.columns.str.strip().str.lower()
    st.success("✅ IMDb data loaded successfully")
except Exception as e:
    st.error(f"❌ Failed to load data: {e}")
    st.stop()

# Print column names for confirmation
#st.write("Raw Columns:", df.columns.tolist())
# Preview data
st.dataframe(df)

def assign_genre(title):
    title = title.lower()
    if "zombie" in title or "terror" in title:
        return "Horror"
    elif "love" in title or "romance" in title:
        return "Romance"
    elif "war" in title or "battle" in title:
        return "Action"
    else:
        return "Adventure"

df["genre"] = df["title"].apply(assign_genre)

selected_genre = st.sidebar.multiselect("Select Genre(s):", options=df["genre"].unique())
filtered_df = df[df["genre"].isin(selected_genre)]


# Filter 2024 and specific genres
#filtered_df = df[(df['year'] == 2024) & (df['Genre'].isin(['Action', 'Adventure', 'Comedy', 'Horror', 'Romance']))]

# Pie Chart Data
#genre_counts = filtered_df['genre'].value_counts().sort_values(ascending=False)

# --- Genre Parsing ---
#genre_list_flat = []

#for gstr in df['Genre'].dropna():
#    for g in str(gstr).split(','):
#        genre = g.strip().capitalize()
#        if genre:
#            genre_list_flat.append(genre)

# Count genres
#genre_counts = pd.Series(genre_list_flat).value_counts().sort_values(ascending=False)
#genre_percentages = (genre_counts / genre_counts.sum()) * 100

# Filter 2024 and specific genres
#filtered_df = df[(df['year'] == 2024) & (df['Genre'].isin(['Action', 'Adventure', 'Comedy', 'Horror', 'Romance']))]

# Pie Chart Data
#genre_counts = filtered_df['genre'].value_counts().sort_values(ascending=False)
#movie_data['genre'] = ", ".join([tag.text.strip() for tag in genre_tags])

# Streamlit app
#st.header("🎯 Genre Distribution for 2024")

#st.write("Filtered Movies:", filtered_df)

# Rename columns to match display names
df.rename(columns={
    "title": "Movie Name",
    "rating": "Ratings",
    "votes": "Voting Counts",
    "duration": "Duration",
    "storyline": "Storyline"
}, inplace=True)

# Filter section
st.sidebar.header("📌 Filters")
min_rating = st.sidebar.slider("Minimum Rating", 0.0, 10.0, 5.0)
min_votes = st.sidebar.slider("Minimum Votes", 0, 5000, 0)
duration_range = st.sidebar.slider("Duration (minutes)", 0, 200, (0, 200))

# Filter data
filtered_df = df[
    (df["Ratings"] >= min_rating) &
    (df["Voting Counts"].str.replace(r'[^\d]', '', regex=True).astype(int) >= min_votes) &
    (df["Duration"].str.extract(r'(\d+)').astype(float)[0].between(duration_range[0], duration_range[1]))
]

# Display filtered results
st.subheader("🎯 Filtered IMDb Movies")
st.dataframe(filtered_df)

# Ratings distribution
st.subheader("⭐ Ratings Distribution")
fig = px.histogram(filtered_df, x="Ratings", nbins=20, title="Rating Histogram")
st.plotly_chart(fig)

# Voting count chart
st.subheader("🔥 Voting Counts")
try:
    filtered_df["Votes (int)"] = filtered_df["Voting Counts"].str.replace(r'[^\d]', '', regex=True).astype(int)
    top_votes = filtered_df.sort_values(by="Votes (int)", ascending=False).head(10)
    fig = px.bar(top_votes, x="Movie Name", y="Votes (int)", title="Top 10 Movies by Votes")
    st.plotly_chart(fig)
except Exception as e:
    st.warning(f"Skipping vote chart due to error: {e}")

    # Pie Chart Data
selected_genre= filtered_df['genre'].value_counts().sort_values(ascending=False)

# --- Matplotlib Bar Chart ---
st.subheader("📈 Bar Chart (Matplotlib)")
fig_bar, ax_bar = plt.subplots()
selected_genre.plot(kind='bar', ax=ax_bar, color='skyblue')
ax_bar.set_title("Number of Movies by Genre (2024)")
ax_bar.set_xlabel("Genre")
ax_bar.set_ylabel("Number of Movies")
st.pyplot(fig_bar)

# --- Plotly Bar Chart ---
st.subheader("📊 Bar Chart (Interactive - Plotly)")
fig_bar_plotly = px.bar(
    x=selected_genre.index,
    y=selected_genre.values,
    labels={'x': 'Genre', 'y': 'Number of Movies'},
    title="Number of Movies by Genre (2024)",
    color=selected_genre.index,
    color_discrete_sequence=px.colors.qualitative.Pastel
)
st.plotly_chart(fig_bar_plotly, use_container_width=True)


# --- Download Filtered Data ---
st.subheader("⬇️ Download Filtered Data")

if not filtered_df.empty:
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download filtered data as CSV",
        data=csv,
        file_name="imdb_filtered_2024.csv",
        mime="text/csv"
    )
else:
    st.info("No filtered data available to download.")

st.success("✅ Dashboard loaded successfully.")
