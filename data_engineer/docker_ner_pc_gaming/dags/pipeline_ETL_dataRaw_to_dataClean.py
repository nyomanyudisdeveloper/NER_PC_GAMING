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





def post_to_elasticsearch():
    # create connection to elasticsearch
    es = Elasticsearch('http://elasticsearch:9200') 

    # read file from file csv data clean
    df= pd.read_csv('/opt/airflow/dags/P2M3_yudis_aditya_data_clean.csv')

    # create new column alias for visualization purpose 
    df['grade_class_alias'] = df['grade_class'].apply(convert_grade_class_alias)

    df['volunteering_alias'] = df['volunteering'].apply(convert_yes_no)
    df['music_alias'] = df['music'].apply(convert_yes_no)
    df['sports_alias'] = df['sports'].apply(convert_yes_no)
    df['extracurricular_alias'] = df['extracurricular'].apply(convert_yes_no)
    df['tutoring_alias'] = df['tutoring'].apply(convert_yes_no)

    df['parental_education_alias'] = df['parental_education'].apply(convert_parental_education_alias)
    df['parental_support_alias'] = df['parental_support'].apply(convert_parental_support_alias)

    df['gender_alias'] = df['gender'].apply(convert_gender_alias)
    df['ethnicity_alias'] = df['ethnicity'].apply(convert_ethnicity_alias)

    # looping for every row data in df
    for i,r in df.iterrows():
        # convert row data to format json
        doc=r.to_json()

        # insert data json to index data_warehouse_school_student
        res=es.index(index="data_warehouse_school_student",doc_type="doc",body=doc)


default_args = {
    'owner': 'yudis_aditya4',
    'start_date': dt.datetime(2024, 7, 21),
    'retries': 6,
    'retry_delay': dt.timedelta(seconds=20),
}


with DAG('Pipeline_ETL_dataRaw_to_dataClean',
         default_args=default_args,
         schedule_interval='30 6 * * *',
         ) as dag:

    getData = PythonOperator(task_id='extract',
                                 python_callable=extract_from_postgresql)
    cleandata = PythonOperator(task_id = 'transform',
                                 python_callable=transform_preProcessing_text)
    # insertData = PythonOperator(task_id='PostToElasticsearch',
                                #  python_callable=post_to_elasticsearch)



# getData >> cleandata >> insertData
getData
