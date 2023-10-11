import streamlit as st
from streamlit_tags import st_tags, st_tags_sidebar
import pandas as pd

pd.options.display.max_columns = 999

#FUNÇÕES


#CONFIGURAÇÕES INICIAIS
st.set_page_config(
    layout='wide',
    page_title='recomendador-papers',
    page_icon=':page_facing_up:'
)


#LOGO E TÍTULO DO APP
st.title('RECOMENDADOR DE PAPERS')


## BOTÕES DE SELEÇÃO APP

st.write('## Preferências Gerais')

areas = st.multiselect(
    'Áreas de interesse:',
    [
    'Political Science','Philosophy','Economics','Business','Psychology',
    'Mathematics','Medicine','Biology','Computer Science','Geology',
    'Chemistry','Art','Sociology','Engineering','Geography',
    'History','Materials Science','Physics','Environmental Science'
    ],
    placeholder='Escolha até 3 áreas',
    max_selections=3)
acesso_aberto = st.selectbox(
    'Você prefere receber apenas artigos de acesso aberto?',
    ('Sim', 'Não'))

st.write('## Termos Chave de Interesse')

termos = st_tags(
    label='Entre com até 3 termos chave de seu interesse:',
    text='Pressione "enter" para adicionar mais',
    value=['Ciência aberta', 'Physical activity', 'Artificial intelligence'],
    maxtags = 3,
    key='1')

st.markdown('<style>label{font-size: 16px;}</style>', unsafe_allow_html=True)


#IMPORTANDO DADOS

df = pd.read_parquet('./data/processed/df_concatenado.parquet')
