import pandas as pd
import networkx as nx
import streamlit as st
import scipy as sp

def load_vertices():
    # rename the movie title column
    df = pd.read_csv('Group9FinalProj_vertices_pd.csv')
    df.rename(columns={'name': 'Movie Title'}, inplace=True)
    return df

def load_edges():
    combined_df = pd.DataFrame()
    for i in range(3):  # Adjust number of splits as you need to
        part_df = pd.read_pickle(f'edges_split_part{i+1}.pkl')
        combined_df = pd.concat([combined_df, part_df], ignore_index=True)
    return combined_df


## load dataframes
vertices_df = load_vertices()
edges_df = load_edges()


# Build the graph
def build_graph(vertices_df, edges_df):
    G = nx.Graph()
    # nodes
    for index, row in vertices_df.iterrows():
        G.add_node(row['id'], title=row['Movie Title'])
    # edges
    for index, row in edges_df.iterrows():
        G.add_edge(row['src'], row['dst'], edge_type=row['edge_type'], weight=row['weight'])
    return G


G = build_graph(vertices_df, edges_df)

# mappings
id_to_title = dict(zip(vertices_df['id'], vertices_df['Movie Title']))
title_to_id = dict(zip(vertices_df['Movie Title'], vertices_df['id']))

# Streamlit UI
st.title("Movie Recommendation System")

# Movie selection
movie_titles = vertices_df['Movie Title'].tolist()
selected_movie = st.selectbox('Select a movie:', movie_titles)


# Function to compute recommendations
def get_recommendations(G, selected_movie_id, id_to_title, num_recommendations=10):
    # Use Personalized PageRank for recommendations
    personalized = {node: 0 for node in G.nodes()}
    personalized[selected_movie_id] = 1  # Personalize to the selected movie
    pr = nx.pagerank(G, personalization=personalized, weight='weight')

    # Sort nodes based on PageRank scores
    sorted_pr = sorted(pr.items(), key=lambda x: x[1], reverse=True)

    # Collect recommended movies, excluding the selected movie
    recommendations = []
    for node_id, score in sorted_pr:
        if node_id != selected_movie_id and node_id in id_to_title:
            recommendations.append((id_to_title[node_id], score))
            if len(recommendations) >= num_recommendations:
                break

    return recommendations


# Display recommendations when the button is clicked
if st.button('Get Recommendations'):
    selected_movie_id = title_to_id[selected_movie]
    recommendations = get_recommendations(G, selected_movie_id, id_to_title)
    st.write(f'Top 10 recommendations for *{selected_movie}*:')
    for idx, (rec_movie, score) in enumerate(recommendations, 1):
        st.write(f"{idx}. {rec_movie} (Score: {score:.4f})")