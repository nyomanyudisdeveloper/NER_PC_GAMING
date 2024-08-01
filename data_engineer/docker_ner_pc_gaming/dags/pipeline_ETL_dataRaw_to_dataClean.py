import datetime as dt
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

import pandas as pd
import psycopg2 as db
from elasticsearch import Elasticsearch

import pandas as pd
# import tensorflow_hub as tf_hub

import math

from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


def clean_special_character(text):
    '''
    This function is used to transofrm text so there are no special character ( alphabetic and numeric only)

    parameter description
    ===========================
    text = question or regular sentence 

    usage example 
    ===================
    data_inferential = "untuk record MLBB dan PUBG kuat kah gan??"
    data_inferential = clean_special_character(data_inferential)
    '''
    result = "";
    for char in text:
        if (char == " " or char.isalpha()) and char != "²":
            result+= char
        else:
            result += " "
    return result



def extract_from_postgresql():
    # create connection to postgresql
    conn_string="dbname='nerpcgaming' host='postgres' user='airflow' password='airflow'"
    conn=db.connect(conn_string)

    # read table from postgre and save it to dataframe
    df_discussion= pd.read_sql("select * from discussion",conn)
    # export file from df to csv
    df_discussion.to_csv('/opt/airflow/dags/data_raw_question.csv',index=False)

    df_kata_tag = pd.read_sql("select * from kata_tag_dict",conn)
    df_kata_tag.to_csv('/opt/airflow/dags/data_kata_tag.csv',index=False)





def transform_preProcessing_text():
    df_question = pd.read_csv('/opt/airflow/dags/data_raw_question.csv')
    df_kata_tag = pd.read_csv('/opt/airflow/dags/data_kata_tag.csv')

    # Remove data duplicate
    df_question = df_question.drop_duplicates(ignore_index=True)
    
    # Handling missing value by delete it
    df_question.dropna(inplace=True)

    # Replace newline into space
    df_question['question'] = df_question['question'].str.replace('\n',' ')

    # Replace special character ( only alphabetic remaining)
    df_question['question_after_preprocessing'] = df_question['question'].apply(clean_special_character)

    # Change question text to lower case
    df_question['question_after_preprocessing'] = df_question['question_after_preprocessing'].apply(lambda x: " ".join(x.lower() for x in x.split()))

    # Remove white space in df question text 
    df_question['question_after_preprocessing'] = df_question['question_after_preprocessing'].str.strip()

    # This code is used to convert data to tokenization
    list_result = []
    for index in df_question.index:
        list_word = df_question.iloc[index]['question_after_preprocessing'].split(" ")
        for word in list_word:
            list_result.append({
                'sentence':f'Kalimat {index+1}',
                'kata': word,
                'tag':''
            })
    df_token = pd.DataFrame(list_result)
    df_token

    # df_token.to_csv("/opt/airflow/dags/DatasetWithTag.csv",index=False)

    # # This code is used to remove slang word
    
    def replace_slang(word):
        slang = pd.read_csv("/opt/airflow/dags/Slang2.csv")
        slang_dict = dict(zip(slang['slang'], slang['formal']))
        # del specific key because it is not neccessary for PC GAMING NER scenario 
        del slang_dict['main']
        del slang_dict['banget']
        del slang_dict['uhh']
        del slang_dict['takut']
        del slang_dict['da']
        del slang_dict['uhhh']

        # edit specific key in slang_dict 
        slang_dict['dahhhh'] = 'sudah'
        slang_dict['kalo'] = 'kalau'
        # Replace each token if it matches a slang term
        steming_slang = slang_dict.get(word)
        if steming_slang == None:
            return word
        else:
            try:
                if(math.isnan(steming_slang)):
                    return word
                else:
                    return steming_slang
            except:
                return steming_slang
    df_token['kata'] = df_token['kata'].apply(replace_slang)

    # Create object that use to stemming word in indonesia using Sastrawati
    # Stemming word using sastrawi
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    def steming_word_sastrawi(word):
        list_skip_steming_word = ['kinemaster','setingan','bekasi','seandainya','seting','rohan','lemot','kesing','diseting']

        stemmed_word = word
        if word not in list_skip_steming_word:
            stemmed_word = stemmer.stem(word)
        return stemmed_word
    df_token['kata_steming'] = df_token['kata'].apply(steming_word_sastrawi)

    # # Steming using manual word
    list_kata_dasar = ['setting','packing','offline','pc','seting','memory','software','ssd','halo','render','ongkir','ganti','upgrade','vga','mobo','case','casing','install','keyboard','ddr','processor','hdd','storage']
    for kata_dasar in list_kata_dasar:
        df_token.loc[df_token['kata'].str.contains(kata_dasar),'kata'] = kata_dasar

    # # Remove stopword in df_token saraswati 
    stopword_factory = StopWordRemoverFactory()
    stopword_remover = stopword_factory.create_stop_word_remover()
    def remove_stopword(word):
        # initiate object that use to remove stopword using sastrawi
        stopword_word = stopword_remover.remove(word)
        return stopword_word  
    df_token['kata_steming'] = df_token['kata_steming'].apply(remove_stopword)
    df_token = df_token[df_token['kata_steming'] != '']

    df_token['kata'] = df_token['kata_steming']
    df_token = df_token[['sentence','kata','tag']]

    def fill_tag(sentence,kata):
        tag = df_kata_tag[(df_kata_tag['sentence'] == sentence) & (df_kata_tag['kata'] == kata)][['tag']].values
        try:
            return tag[0][0]
        except:
            return ''

    df_token['tag'] = df_token.apply(lambda row_data: fill_tag(row_data['sentence'],row_data['kata']),axis=1)

    df_token.to_csv("/opt/airflow/dags/DatasetWithTag.csv",index=False)


def load_to_elasticsearch():
    # create connection to elasticsearch
    es = Elasticsearch('http://elasticsearch:9200') 

    # read file from file csv data clean
    df= pd.read_csv('/opt/airflow/dags/DatasetWithTag.csv')

    # looping for every row data in df
    for i,r in df.iterrows():
        # convert row data to format json
        doc=r.to_json()

        # insert data json to index data_warehouse_school_student
        res=es.index(index="data_index_ner_pc_gaming",doc_type="doc",body=doc)


default_args = {
    'owner': 'yudis_aditya1',
    'start_date': dt.datetime(2024, 7, 21),
    'retries': 6,
    'retry_delay': dt.timedelta(seconds=20),
}


with DAG('Pipeline_ETL_dataRaw_to_dataClean',
         default_args=default_args,
         schedule_interval='30 6 * * *',
         ) as dag:

    extractData = PythonOperator(task_id='extract',
                                 python_callable=extract_from_postgresql)
    transformData = PythonOperator(task_id = 'transform',
                                 python_callable=transform_preProcessing_text)
    loadData = PythonOperator(task_id='load',
                                 python_callable=load_to_elasticsearch)



# getData >> cleandata >> insertData
extractData >> transformData >> loadData
