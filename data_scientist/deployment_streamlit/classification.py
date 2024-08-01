# Import Libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pickle
import json
import tensorflow as tf
import math
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from collections import defaultdict

# Initialize stopword remover and stemmer
stopword_factory = StopWordRemoverFactory()
stopword = stopword_factory.create_stop_word_remover()
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# Load the model and dictionaries
with open("model_NER.pkl", "rb") as file_1:
    model = pickle.load(file_1)

with open("wordDict.json", "r") as file_2:
    word2idx = json.load(file_2)

with open("tagDict.json", "r") as file_3:
    tag2idx = json.load(file_3)

# Load slang data
slang = pd.read_csv('Slang2.csv')
slang_dict = dict(zip(slang['slang'], slang['formal']))

def clean_special_character(text):
    result = ""
    for char in text:
        if char == " " or char.isalnum():
            result += char
    return result

def replace_slang(tokens):
    list_result = []
    for token in tokens:
        stemming_slang = slang_dict.get(token)
        if stemming_slang is None:
            list_result.append(token)
        else:
            try:
                if math.isnan(stemming_slang):
                    list_result.append(token)
                else:
                    list_result.append(stemming_slang)
            except:
                list_result.append(stemming_slang)
    return list_result

def convert_word_to_nominal_category(list_word):
    list_result = []
    for word in list_word:
        if word in word2idx:
            index = word2idx[word]
            list_result.append(index)
    return list_result

def remove_stopwords(tokens):
    text = ' '.join(tokens)
    filtered_text = stopword.remove(text)
    return filtered_text.split()

def map_original_to_stemmed(tokens_list, stemmer):
    """
    Maps original tokens to their stemmed versions using the provided stemmer.

    Parameters:
        tokens_list (list of list of str): A list of lists, where each inner list contains tokens (words).
        stemmer (object): A stemmer object with a .stem() method, used to stem tokens.

    Returns:
        defaultdict: A dictionary mapping each stemmed token to a list of its original forms.
    """
    original_tokens = defaultdict(list)

    for tokens in tokens_list:
        for token in tokens:
            stemmed_token = stemmer.stem(token)
            original_tokens[stemmed_token].append(token)
    
    return original_tokens

def stem_tokens(tokens):
    return [stemmer.stem(token) for token in tokens]

def run():
    st.title("Hey, Let's Classify Your :blue[Text] :sunglasses:")
    with st.form("prediction_form"):
        text = st.text_input("Question About PC Gaming", "Input Your Question")
        submitted = st.form_submit_button("Submit")
        
        if submitted and text:
            text = clean_special_character(text)
            text_clean = text.lower().strip()
            text_split = text_clean.split(" ")
            text = replace_slang(text_split)
            text = remove_stopwords(text)
            text = stem_tokens(text)
            text_id = convert_word_to_nominal_category(text)
            text_array = np.array([text_id])
            
            y_pred = model.predict(text_array)
            y_pred = np.argmax(y_pred, axis=-1)
            
            st.write(f'### This question has tags:')
            for tag in y_pred[0]:
                key = next((key for key, value in tag2idx.items() if value == tag), None)
                if key:
                    st.write(f'- {key}')

if __name__ == '__main__':
    run()
