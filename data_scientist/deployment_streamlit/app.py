import streamlit as st
import eda
import classification
import FAQ

navigation = st.sidebar.selectbox('Pilih Halaman:',('EDA','Classification','FAQ'))

if navigation == 'EDA':
    eda.run()
elif navigation == 'FAQ':
    FAQ.run()
else:
   classification.run()