# # Import pacakges yang diperlukan untuk Web Scrapping 
from selenium import webdriver
import numpy as np 
import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import math

list_question_scrapping = []
last_page = 0
last_index_product = 0
last_total_product = 0

# Initiate driver for using selenium 
driver = webdriver.Chrome()
driver.implicitly_wait(10)

test_count = 11
list_url = []

# Initiate total page and prudct name for web scrapping
total_page = 1
search_product_query = "PC Gaming"


for page in range(total_page):
    last_page = page+1
    url= f"https://www.tokopedia.com/search?navsource=&page={page+1}&q={search_product_query}&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&st="
    driver.get(url)
    time.sleep(1.5)

    stopScrolling = 0
    while True:
        stopScrolling += 1
        driver.execute_script("window.scrollBy(0,140)")
        time.sleep(0.5)
        if stopScrolling > 40:
            break
    list_product_element = driver.find_elements(By.CLASS_NAME,"css-5wh65g")
    for product_element in list_product_element:
        try:
            url = product_element.find_element(By.TAG_NAME,"a").get_attribute('href')
            list_url.append(url)
        except:
            url = None
            list_url.append(url)
        
    for url in list_url:
        if url != None:
            driver.get(url)
            last_total_product += 1
            time.sleep(10)
            stopScrolling = 0
            while True:
                stopScrolling += 1
                driver.execute_script("window.scrollBy(0,140)")
                time.sleep(0.5)
                if stopScrolling > 10:
                    break
            try:
                btn_discuss_nav = driver.find_element(By.CSS_SELECTOR,"button[data-testid='discussion_faq']")
                btn_discuss_nav.click()
            except:
                pass
            try:
                time.sleep(10)
                stopScrolling = 0
                while True:
                    stopScrolling += 1
                    driver.execute_script("window.scrollBy(0,140)")
                    time.sleep(0.5)
                    if stopScrolling > 5:
                        break
                list_discussion = driver.find_elements(By.CLASS_NAME,'css-1huugyc')
                for discussion_container in list_discussion:
                    question_text = discussion_container.find_element(By.CLASS_NAME,'css-19lihx0-unf-heading').text
                    list_question_scrapping.append(question_text)
                button_next_discussion = driver.find_elements(By.CLASS_NAME,"css-16uzo3v-unf-pagination-item")[-1]
                while(button_next_discussion.is_enabled()):
                    button_next_discussion.click()
                    time.sleep(10)
                    list_discussion = driver.find_elements(By.CLASS_NAME,'css-1huugyc')
                    for discussion_container in list_discussion:
                        question_text = discussion_container.find_element(By.CLASS_NAME,'css-19lihx0-unf-heading').text
                        list_question_scrapping.append(question_text)
                    button_next_discussion = driver.find_elements(By.CLASS_NAME,"css-16uzo3v-unf-pagination-item")[-1]
            except:
                pass
    
    df_input = pd.DataFrame(list_question_scrapping,columns=['question'])
    df_total = pd.read_csv("../../dataset/question.csv")
    df_result = pd.concat([df_input,df_total],axis=0)
    df_result.to_csv("../../dataset/question.csv",index=False)