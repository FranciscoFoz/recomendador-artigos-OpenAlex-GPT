import streamlit as st
from streamlit_tags import st_tags
import pandas as pd
#import markdown
#from bs4 import BeautifulSoup
import json
import openai

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


    #Não foi implementada inicialmente
    '''
    def markdown_to_html(input_file):

        with open(input_file, 'r', encoding='utf-8') as md_file:
            markdown_text = md_file.read()
            
        html = markdown.markdown(markdown_text)
        # Incluir a ligação para o arquivo CSS
        html = f"""
        <html>
        <head>
            <link rel="stylesheet" type="text/css" href="style.css">
        </head>
        <body>
        <div class="container">
        {html}
        </div>
        </body>
        </html>
        """
        
        soup = BeautifulSoup(html, 'html5lib')

        html_formatado = soup.prettify()
        
        with open('newsletter_final.html', 'w', encoding='utf-8') as html_file:
            html_file.write(html_formatado)
    '''

def criar_markdown_com_artigos(df):
    artigos = ''

    for i in range(5):
        article_markdown = f"### [{df['title'].iloc[i]}]({df['doi'].iloc[i]})\n\n"
        article_markdown += f"**Data de Publicação**: {df['publication_date'].iloc[i]}\n\n"
        article_markdown += f"**Resumo**: {df['abstract'].iloc[i]}\n\n"

        artigos += article_markdown

    return artigos

def criar_markdown_com_artigos(artigos,paragrafo_inicial):
    
    markdown_content = f'## Recomendações\n\n Olá,\n{paragrafo_inicial}\n\n{artigos}'

    return markdown_content


def chave_open_ai():
    
    with open('../../credentials_open_ai.json','r') as json_file:
        dados = json.load(json_file)
        api_key = dados.get('OPEN_AI_API_KEY')
        
        
    return api_key    


def chama_api_gera_termos(termo):
    
    resposta = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                {
                    "role": "system",
                    "content": "Você é uma bibliotecária, especialista em linguagem documentária (tesauros)."
                },
                {
                    "role": "user",
                    "content": f'''
                        A partir dessa lista de termos {termo}.
                        Gere pelo menos 5 termos relacionados (como um tesauro) para cada um, em inglês e em português, mas retorne todos em conjunto.
                        
                        Responda com uma única lista Python todos os termos.
                        
                        Como nesse exemplo:
                        ['Artificial Intelligence,'Inteligência Artificial']
                        
                        Não responda mais nada além da lista.
                        '''

                },
                ],
                temperature=1.05,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=1,
                stop=["30"]
            )
    return resposta

def gera_termos_relacionados(termo):
    tentativas = 0

    while tentativas < 3:
        tentativas += 1

        try:
            resposta = chama_api_gera_termos(termo)
            
            termos_relacionados = resposta.get('choices')[0].get('message').get('content')
            lista_termos_relacionados = eval(termos_relacionados)
            
            return lista_termos_relacionados
       
        except SyntaxError:
            print("Erro de sintaxe. Tentando novamente...")
            continue 
        
        except openai.error.APIError as error:
            print(f'Erro de API. {error}')

    print("Número máximo de tentativas alcançado. Não foi possível obter uma resposta.")
    return None


        
#--------------------------------------------------------------------------------------------------------------------


#VALIDA CHAVE OPEN AI
openai.api_key = chave_open_ai()


#IMPORTANDO DADOS

df = pd.read_parquet('./data/processed/df_concatenado.parquet')

colunas_pt_br = {
    'Computer science': 'Ciência da Computação',
    'Mathematics': 'Matemática',
    'Physics':'Física',
    'Biology':'Biologia',
    'Chemistry':'Química',
    'Political science':'Ciências Políticas',
    'Engineering':'Engenharia',
    'Materials science':'Ciência dos Materiais',
    'Philosophy':'Filosofia',
    'Business':'Administração e Negócios',
    'Psychology':'Psicologia',
    'Art':'Artes',
    'Medicine':'Medicina',
    'Geography':'Geografia',
    'Geology':'Geologia',
    'Economics':'Economia',
    'Sociology':'Sociologia',
    'Environmental science':'Ciências Ambientais',
    'History':'História'
    }
df.rename(columns=colunas_pt_br, inplace=True) 

#CONFIGURAÇÕES INICIAIS
st.set_page_config(
    layout='wide',
    page_title='recomendador-artigos-cientificos',
    page_icon=':page_facing_up:'
)


#LOGO E TÍTULO DO APP
st.title('RECOMENDADOR DE ARTIGOS CIENTÍFICOS')
st.image('reports/figures/open-alex.png')



## BOTÕES DE SELEÇÃO APP

st.write('## Preferências Gerais')

areas = st.multiselect(
    'Áreas de interesse:',
    [
        'Administração e Negócios', 'Artes', 'Biologia', 'Ciência da Computação', 'Ciência dos Materiais',
        'Ciências Ambientais', 'Ciências Políticas', 'Economia', 'Engenharia', 'Filosofia', 'Física', 
        'Geografia', 'Geologia', 'História', 'Matemática', 'Medicina', 'Psicologia', 'Química', 'Sociologia'
        ],
    placeholder='Escolha até 3 áreas',
    max_selections=3)

acesso_aberto = st.selectbox(
    'Você prefere receber apenas artigos de acesso aberto?',
    ('Sim', 'Não'))

st.write('## Termos Chave de Interesse')

termos = st_tags(
    label='Entre com até 3 termo-chave de seu interesse (em português ou inglês):',
    text='Pressione "enter" para adicionar mais',
    value=['Inteligência artificial', 'Physical activity'],
    maxtags = 3,
    key='1')
print(termos)

if st.button("Recomende"):
    if areas and len(termos) != 0:
        lista_termos_relacionados = gera_termos_relacionados(termos)
        print(lista_termos_relacionados)
        df = filtrar_escolha(areas,acesso_aberto,termos,lista_termos_relacionados)
        st.markdown(criar_markdown_com_artigos(df))
        print(criar_markdown_com_artigos(df))
    else:
        st.write('Escolha uma área e, pelo menos, um termo-chave de interesse :confused:')

