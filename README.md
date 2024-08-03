# Project Name

This project called Gaming Scout. This is project team to fulfill final project at Hactiv8 and part of my personal portofolio in Data Science. My other personal project can be found at the [Nyoman Yudis Developer](https://github.com/nyomanyudisdeveloper)

#### -- Project Status: On-Hold

## Project Intro/Objective

The purpose of this project is to get data discussion product PC Gaming from website using method webscraping and then save it to database. And then we create pipeline to do ETL to load it with file csv and we used that file to Exploratory Data Analysis (EDA) and Model Tranining and Evaluation. The model goal is to extract information from question in duscssion by doing Named Entity Recognition (NER) by using concept Natural Language Program (NLP) and Neural Network. The metric we used for model evaluation is accuracy and it's score is 0.97.

### Partner

- Richard Edgina Virgo, [linkedin](https://www.linkedin.com/in/richard-edgina-virgo-a7435319b/) [github](https://github.com/REV04)
- Muhammad Haykal Qobus, [linkedin](https://www.linkedin.com/in/muhammad-haykal-qobus-4b8b391a9/)

### Methods Used

- Web Scraping
- ETL
- Batch Processing
- Natural Language Programming (NLP)
- Named Entity Recognition (NER)
- Neural Network
- Data Visualization

### Technologies

- Python
- Selenium
- PostgreSQL
- Airflow
- Pandas
- Sastrawi
- Streamlit
- Tensorflow
- Matploptlib

## Project Description

The dataset we used to create this model is from result webscrapping data discussion in [Tokopedia](https://www.tokopedia.com) with search product name "PC Gaming". With this dataset we do Exploratory Data Analysis(EDA) and found that most people discuss about Game, Device, Spek, and Activity. The conclusion in my EDA are :

- people make game GTA as benchmark before buy or not PC Gaming
- people prefer to buy PC that already include with monitor
- vga is the most important consideration in spek PC because this component is one of important part to play game.
- PC Gaming usually not only use for play game, but also for editing video and design grafis

And also we create model using this dataset to solve problem to get insight from discussion using NLP and neural network. The most challenging before do model training is manual labeling every word after pre processing text. But we try to simplify this process by create code standard manual labeling using pandas and batch processing ETL so in process Transform it's already labeling with previous exisitng word and tag.

## Getting Started

1. Clone this repo (for help see this [tutorial](https://help.github.com/articles/cloning-a-repository/)).
2. Raw Data is being kept in folder dataset/question.csv
3. Data processing/transformation scripts are being kept in folder data_scientist/text_preprocessing.ipynb
4. Model training and evaluation script is being kept in data_scientist/model_training_and_evaluation.ipynb
5. Model Inferential script is being kept in data_scientist/Model_inferential.ipynb
6. Deployment model inferential using streamlit are being kept in folder data_scientist/deployment_streamlit/
7. Exploratory Data Analysis (EDA) scripts is being kept in data_analust/index.ipynb
8. Webscrapping script is being kept in data_engineer/web_scrapping/index.py
9. Create pipeline for batch processing ETL script is being kept in data_engineer/docker_mer_pc_gaming/dags/pipeline_ETL_dataRaw_to_dataClean.py

## Featured Notebooks/Analysis/Deliverables

- [Hungging Face for model usage demonstration](https://huggingface.co/spaces/REV04/Gaming_Scout)
- [Slide PPT for this project](https://docs.google.com/presentation/d/1jv9aca-G_pSjwXRw7ebIYsGrZzh4yAFyUm6J0fLmgFI/edit#slide=id.p6)

## Contact

- If you have any question or want to contribute with this project, feel free to ask me in [linkedin](https://www.linkedin.com/in/yudit-a-9941ab318/) or my partners.
