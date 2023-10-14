import streamlit as st
from streamlit_tags import st_tags, st_tags_sidebar
import pandas as pd

pd.options.display.max_columns = 999

#FUNÇÕES
def filtrar_dataframe_por_termos(df, termos):
    
    termos_formatados = [f"`{termo}`" if ' ' in termo else termo for termo in termos]
    
    filtro = " or ".join(f"{termo} > 0" for termo in termos_formatados)
    
    df_filtrado = df.query(filtro).loc[:, ['doi', 'title','abstract', 'publication_date', 'open_access'] + termos]
    
    return df_filtrado

def filtrar_dataframe_por_acesso_aberto(df,resposta):
    
    if resposta == 'Sim':
        df = df.query('open_access == True')
    
    return df

def criar_coluna_score(df):
    
    df['score'] = df.iloc[:,4:].sum(axis=1)
    
    return df

def atribuir_fator_termo_score(df, termos):
    df_copy = df.copy()
    
    df_copy['title'] = df_copy['title'].fillna('')
    
    for term in termos:
        mask = df_copy['title'].str.upper().str.contains(term.upper())
        df_copy.loc[mask, 'score'] *= 2
        
        mask = df_copy['abstract'].str.upper().str.contains(term.upper())
        df_copy.loc[mask, 'score'] *= 1.5
    
    df_copy = df_copy.sort_values(by='score', ascending=False)
    
    return df_copy

def atribuir_fator_termo_similar_score(df, termos_similares):
    df_copy = df.copy()
    
    df_copy['title'] = df_copy['title'].fillna('')
    
    for term in termos_similares:
        mask = df_copy['title'].str.upper().str.contains(term.upper())
        df_copy.loc[mask, 'score'] *= 1.5
        
        mask = df_copy['abstract'].str.upper().str.contains(term.upper())
        df_copy.loc[mask, 'score'] *= 1.25
    
    df_copy = df_copy.sort_values(by='score', ascending=False)
    
    return df_copy


def normalizar_score(df):
    min_score = df['score'].min()
    max_score = df['score'].max()


    df['score_normalizado'] = ((df['score'] - min_score) / (max_score - min_score))

    return df

def filtrar_escolha(areas,acesso_aberto,termo,termo_similar):
    
    df_filtrado = filtrar_dataframe_por_termos(df,areas)

    df_filtrado = filtrar_dataframe_por_acesso_aberto(df_filtrado,acesso_aberto)

    df_filtrado = criar_coluna_score(df_filtrado)

    df_filtrado = atribuir_fator_termo_score(df_filtrado,termo)

    df_filtrado = atribuir_fator_termo_similar_score(df_filtrado,termo_similar)

    df_filtrado = normalizar_score(df_filtrado)
    
    
    df_filtrado_top = df_filtrado.head(5).reset_index(drop=True).loc[:,['doi','title','abstract','publication_date']]

    return df_filtrado_top


def criar_html_com_artigos(df):
    with open('./newsletter_template.html', 'r', encoding='utf-8') as file:
        html_template = file.read()

    html_artigos = ""

    for i in range(5):
        article_html = f"""
            <div class="article">
                <h2>{df['title'].iloc[i]}</h2>
                <p>{df['abstract'].iloc[i]}</p>
                <p class="date">Data de Publicação: {df['publication_date'].iloc[i]}</p>
                <p class="doi">DOI: <a href="{df['doi'].iloc[i]}">{df['doi'].iloc[i]}</a></p>
            </div>
        """
        html_artigos += article_html

    html_template = html_template.replace("<!-- ARTICLES_GO_HERE -->", html_artigos)

    with open('./newsletter_final.html', 'w', encoding='utf-8') as file:
        file.write(html_template)

#--------------------------------------------------------------------------------------------------------------------

#IMPORTANDO DADOS

df = pd.read_parquet('./data/processed/df_concatenado.parquet')


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
     'Art', 'Biology', 'Business', 'Chemistry', 
     'Computer Science', 'Economics', 'Engineering', 
     'Environmental Science', 'Geography', 'Geology', 
     'History', 'Materials Science', 'Mathematics', 
     'Medicine', 'Philosophy', 'Physics', 
     'Political Science', 'Psychology', 'Sociology'
     ],
    placeholder='Escolha até 3 áreas',
    max_selections=3)
acesso_aberto = st.selectbox(
    'Você prefere receber apenas artigos de acesso aberto?',
    ('Sim', 'Não'))

st.write('## Termos Chave de Interesse')

termos = st_tags(
    label='Entre com até 3 termo-chave de seu interesse:',
    text='Pressione "enter" para adicionar mais',
    value=['Inteligência Artificial', 'Physical activity'],
    maxtags = 3,
    key='1')


if st.button("Recomende"):
    df = filtrar_escolha(areas,acesso_aberto,termos,['Nature','Oral'])
    print(df)
    criar_html_com_artigos(df)
    


