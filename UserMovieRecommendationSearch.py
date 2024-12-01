import streamlit as st
import pandas as pd
import pickle

def combine_pickles(output_prefix):
    combined_df = pd.DataFrame()
    for i in range(4):
        # Load each .pkl file and append it to the combined DataFrame
        part_df = pd.read_pickle(f"{output_prefix}_part{i+1}.pkl")
        combined_df = pd.concat([combined_df, part_df], ignore_index=True)
    print("DataFrames combined back into one DataFrame.")
    return combined_df



try:
    df = combine_pickles('data_split')
        
    # check that it is a dataframe
    if isinstance(df, pd.DataFrame):
        #st.success(f"File '{FILE_NAME}' loaded successfully!")
        
        # selectbox that has autocomplete option 
        user_ids = sorted(df['userId'].unique())
        selected_user_id = st.selectbox(
            "Select or type a User ID:",
            user_ids
        )
        
        #shows results, and sorts values
        if selected_user_id:
            user_data = df[df['userId'] == selected_user_id]
            user_data_sorted = user_data.sort_values(by='predicted_rating', ascending=False)
            
            
            st.write("### Recommendations for User ID:", selected_user_id)
            st.dataframe(user_data_sorted[['Movie Title', 'Theme', 'Predicted Rating']])
    else:
        st.error("The file does not contain a valid DataFrame.")
except FileNotFoundError:
    st.error(f"File '{FILE_NAME}' not found. Please ensure it is in the same directory as this script.")
except Exception as e:
    st.error(f"An error occurred while loading the file: {e}")