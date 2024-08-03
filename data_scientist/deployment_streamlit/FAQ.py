import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pickle
import json

df = pd.read_csv('DatasetWithTagFinal.csv')
df.dropna(inplace=True)

def filter_and_combine_words(df, tag_contains_list):
    # Check if all tags in the list are contained within the 'tag' column for each 'Kalimat'
    def check_all_tags(tags):
        return all(tags.str.contains(tag).any() for tag in tag_contains_list)
    
    # Apply the check to each group of sentences
    df['has_all_tags'] = df.groupby('sentence')['tag'].transform(lambda x: check_all_tags(x))

    # Select all sentences containing words with all specified tags
    result_df = df[df['has_all_tags']]

    # Drop the helper column
    result_df = result_df.drop(columns=['has_all_tags'])

    # Combine words based on 'Kalimat'
    combined_words = result_df.groupby('sentence')['kata'].apply(' '.join).reset_index()

    return combined_words

def run():
    df_value = pd.DataFrame(df['tag'].value_counts())
    st.dataframe(df_value)
    with st.form("prediction_form"):
        text = st.multiselect('**4 Top Topic**',['Game','Spek','Device','Request'])
        submitted = st.form_submit_button("Submit")
    # st.write("Outside the form")
    if submitted:
      if text:
        combined_words = filter_and_combine_words(df, text)
        combined_words = combined_words['kata']
        st.write("Combined words for sentences containing all selected tags:")
        st.dataframe(combined_words)
      else:
        st.write("Please select at least one tag.")

if __name__ == '__main__':
  run()
