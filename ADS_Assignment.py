import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

st.set_page_config(page_title='Superb Dash', page_icon='random', layout='centered', initial_sidebar_state='auto')

path = "./Assignment/dataonline.csv"
st.sidebar.title('Superb Dash')
Assignment = st.sidebar.file_uploader('Upload Dataset', type=['csv'])



