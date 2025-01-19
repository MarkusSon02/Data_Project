import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(page_title="Spotify Data Dashboard", layout="wide")

# PostgreSQL connection
db_url = "postgresql://son:son@localhost:5432/spotify"
engine = create_engine(db_url)

# Load data from PostgreSQL
@st.cache
def load_data(table_name):
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql(query, engine)

# Streamlit app layout
# st.title("Spotify Data Dashboard")
# st.write("Explore Spotify data from Kaggle with interactive visualizations.")


# Sidebar options
data_source = st.sidebar.selectbox("Choose Dataset", ["Tracks", "Genres", "Years"])
if data_source == "Tracks":
    df = load_data("data")
elif data_source == "Genres":
    df = load_data("genre_data")
else:
    df = load_data("year_data")

# Display dataset
st.write(f"Showing data from: **{data_source}**")
st.dataframe(df)

# Example visualization
if data_source == "Years":
    st.line_chart(df[['year', 'popularity']].set_index('year'))
elif data_source == "Genres":
    top_genres = df.sort_values(by='popularity', ascending=False).head(10)
    st.bar_chart(top_genres[['genre', 'popularity']].set_index('genre'))
else:
    st.write("Explore tracks data here!")
