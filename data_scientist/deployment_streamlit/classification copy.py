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
from tensorflow.keras.preprocessing.sequence import pad_sequences
from collections import defaultdict

# Initialize stopword remover and stemmer
stopword_factory = StopWordRemoverFactory()
stopword = stopword_factory.create_stop_word_remover()
factory = StemmerFactory()
stemmer = factory.create_stemmer()

list_skip_steming_word = ['kinemaster','setingan','bekasi','seandainya','seting','rohan','lemot','kesing','diseting']

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

del slang_dict['main']
del slang_dict['banget']
del slang_dict['uhh']
del slang_dict['takut']
del slang_dict['da']
del slang_dict['uhhh']

# edit specific key in slang_dict 
slang_dict['dahhhh'] = 'sudah'
slang_dict['kalo'] = 'kalau'

def clean_special_character(text):
    result = ""
    for char in text:
        if (char == " " or char.isalpha()) and char != "²":
            result+= char
        else:
            result += " "

    text = result
    return text

def replace_slang(tokens):
    # del specific key because it is not neccessary for PC GAMING NER scenario 
    list_result = []
    for word in tokens:
        steming_slang = slang_dict.get(word)
        if steming_slang == None:
            list_result.append(word)
        else:
            try:
                if(math.isnan(steming_slang)):
                    list_result.append(word)
                else:
                    list_result.append(steming_slang)
            except:
                list_result.append(steming_slang)

    tokens = list_result
    return tokens


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
    list_result = []
    for word in tokens:
        stemmed_word = word
        if word not in list_skip_steming_word:
            stemmed_word = stemmer.stem(word)
        list_result.append(stemmed_word)
    tokens = list_result
    return tokens
    # return [stemmer.stem(token) for token in tokens]

def stem_tokens_manual(tokens):
    # Steming using manual word
    list_kata_dasar = ['setting','packing','offline','pc','seting','memory','software','ssd','halo','render','ongkir','ganti','upgrade','vga','mobo','case','casing','install','keyboard','ddr','processor','hdd','storage']
    list_result = []
    for token in tokens:
        word_result = token
        for kata_dasar in list_kata_dasar:
            if token.find(kata_dasar) != -1:
                word_result = kata_dasar
                break
        list_result.append(word_result)

    tokens = list_result 
    return tokens

max_len = 40
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
            text = stem_tokens(text)
            text = stem_tokens_manual(text)
            text = remove_stopwords(text)
            text_id = convert_word_to_nominal_category(text)
            list_result = []
            for index in text_id:
                if index != 0:
                    list_result.append(index)
            text_id = list_result
            total_word = len(text_id)

            text_array = np.array([text_id])
            text_arrays = pad_sequences(maxlen=40, sequences=text_array, padding="post")
            
            pred = model.predict(text_arrays)
            pred = np.argmax(pred, axis=-1)
            pred = pred[0][0:total_word]
            pred = np.array([pred])
            

            
            st.write(f'### This question has tags:')
            idx2tag = {v: k for k, v in tag2idx.items()}
            idx2word = {v: k for k, v in word2idx.items()}

            # Decode data_inferential_token_id
            decoded_words = np.vectorize(lambda x: idx2word.get(x, 'Unknown'))(text_arrays)
            # Decode y_pred
            decoded_tags = np.vectorize(lambda x: idx2tag.get(x, 'None'))(pred)

            # Check for 'None' values in decoded_tags and handle them
            for row in decoded_tags:
                for i, tag in enumerate(row):
                    if tag == 'None':
                        # Handle the 'None' value appropriately, e.g., replace with a default tag or remove
                        row[i] = 'ENPAD'  # Replace 'None' with 'Unknown'
            
            st.write("{:15}\t{}".format("Word", "Pred"))
            st.write("-" * 30)

            for word, tag in zip(decoded_words[0], decoded_tags[0]):
                st.write("{:15}\t{}".format(word, tag))

            # for tag in y_pred[0]:
            #     key = next((key for key, value in tag2idx.items() if value == tag), None)
            #     if key:
            #         st.write(f'- {key}')

if __name__ == '__main__':
    run()
