import streamlit as st
import pandas as pd


st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")
# Add custom CSS for light red background
st.markdown(
    """
    <style>
    body {
        background-color: #ffe5e5;
    }
    .stApp {
        background-color: #ffe5e5;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ...existing code...

# Load dataset
df = pd.read_csv("movies.csv", encoding="latin1")


st.title("🎥 Movie Recommendation System")

# Sidebar Filters
st.sidebar.header("🎯 Filter Options")
selected_genres = st.sidebar.multiselect("Select Genre(s):", df['genre'].unique())
selected_language = st.sidebar.selectbox("Select Language:", ["All"] + sorted(df['language'].unique().tolist()))
selected_director = st.sidebar.selectbox("Select Director:", ["All"] + sorted(df['director'].unique().tolist()))

# Apply filters
filtered_df = df.copy()
if selected_genres:
    filtered_df = filtered_df[filtered_df['genre'].isin(selected_genres)]
if selected_language != "All":
    filtered_df = filtered_df[filtered_df['language'] == selected_language]
if selected_director != "All":
    filtered_df = filtered_df[filtered_df['director'] == selected_director]

# Tabs
tab1, tab2, tab3 = st.tabs(["🎬 All Movies", "🔍 Filtered Results", "🔁 Similar Movies"])

# Tab 1 - All Movies
with tab1:
    st.subheader("🔥 All Movies in Database")
    for i, row in df.iterrows():
        st.markdown(f"### {row['title']}")
        st.markdown(f"**Genre:** {row['genre']} | **Director:** {row['director']} | **Language:** {row['language']}")
        st.markdown(f"_{row['description']}_")
        st.markdown("---")

# Tab 2 - Filtered Movies
with tab2:
    st.subheader("🎯 Movies Matching Your Preferences")
    if not filtered_df.empty:
        for i, row in filtered_df.iterrows():
            st.markdown(f"#### {row['title']}")
            st.markdown(f"**Genre:** {row['genre']} | **Director:** {row['director']} | **Language:** {row['language']}")
            st.markdown(f"_{row['description']}_")
            st.markdown("---")
    else:
        st.warning("No movies match the selected filters.")

# Tab 3 - Similar Movies
with tab3:
    selected_movie = st.selectbox("Select a movie to find similar ones:", df['title'].unique())
    if selected_movie:
        base = df[df['title'] == selected_movie].iloc[0]
        similar_df = df[
            (df['genre'] == base['genre']) &
            (df['language'] == base['language']) &
            (df['title'] != selected_movie)
        ]
        st.subheader(f"Movies similar to **{selected_movie}**")
        if not similar_df.empty:
            for i, row in similar_df.iterrows():
                st.markdown(f"#### {row['title']}")
                st.markdown(f"**Genre:** {row['genre']} | **Director:** {row['director']} | **Language:** {row['language']}")
                st.markdown(f"_{row['description']}_")
                st.markdown("---")
        else:
            st.info("No similar movies found.")
