import streamlit as st
import pandas as pd

pd.options.display.max_columns = 999


#CONFICURAÇÕES INICIAIS
st.set_page_config(
    layout='wide',
    page_title='recomendador-papers',
    page_icon=':page_facing_up:'
)

#LOGO E TÍTULO DO APP
st.title('RECOMENDADOR DE PAPERS')

df = pd.read_parquet('./data/processed/df_concatenado.parquet')

print(df)