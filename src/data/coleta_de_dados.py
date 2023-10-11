import pandas as pd
import os
import requests

#FUNÇÕES

def coletar_dados_e_salvar(start_date, end_date):
    
    cursor = '*'
    
        
    contador = 1
    contador_erro = 0
    
    if not os.path.exists(f'datasets_{start_date}_to_{end_date}'):
        os.makedirs(f'datasets_{start_date}_to_{end_date}')
    
    while cursor != None:
        url = f'https://api.openalex.org/works?filter=from_publication_date:{start_date},to_publication_date:{end_date},type:article&per-page=200&cursor={cursor}'

        
        try:
            requisicao = requests.get(url)
            pagina_com_resultados = requisicao.json()
            
        except (requests.exceptions.RequestException, ValueError) as e:
            contador_erro += 1 
            print(f"Erro na página {contador} (Erro {contador_erro}): {e}")
            continue 
        
        resultados = pagina_com_resultados.get('results', [])
        
        df = pd.DataFrame(resultados)
        parquet_arquivo = os.path.join(f'datasets_{start_date}_to_{end_date}', f'registros_{contador}.parquet')
        df.to_parquet(parquet_arquivo, index=False)
        
        cursor = pagina_com_resultados['meta'].get('next_cursor')
        
        contador += 1
    
    print(f"Total de erros: {contador_erro}")

def criar_work_id(df):
    
    df['workd_id'] = df['id'].apply(lambda x: x.split('https://openalex.org/')[1])
    
    return df

def requisitar_abstract_inverted_index(id):
    
    url = f'https://api.openalex.org/works/{id}'

    abstract_inverted_index = requests.get(url).json()['abstract_inverted_index']
    
    return abstract_inverted_index

def formatar_abstract(abstract_desformatado):
    
    if abstract_desformatado is not None:
        todas_palavras = []
        for termo, posicoes in abstract_desformatado.items():
            for posicao in posicoes:
                todas_palavras.insert(posicao, termo)

        texto_corrido = ' '.join(todas_palavras)
        return texto_corrido
    else:
        return ""

def extrair_concepts_scores(df):
    concept_data = []

    for concepts in df['concepts']:
        concept_scores = {}
        for concept in concepts:
            if concept['level'] == 0:
                concept_scores[concept['display_name']] = concept['score']
        concept_data.append(concept_scores)

    df_concepts = pd.DataFrame(concept_data, index=df.index).fillna(0).round(4)

    df_final = pd.concat([df, df_concepts], axis=1)

    return df_final

'''
def extrair_concepts(df):
    concepts = []

    for coluna in df.iloc[:,6:].columns:
        if df[coluna].gt(0).any():
            concepts.append(coluna)

    df['concepts'] = df.apply(lambda row: ';'.join([col for col in concepts if row[col] > 0]), axis=1)

    return df
'''

def processar_dataframe(df):
    
    df = criar_work_id(df)
    
    df['abstract'] = df['workd_id'].apply(requisitar_abstract_inverted_index).apply(formatar_abstract)
    
    df = df.loc[:, ['doi', 'title','abstract', 'publication_date', 'open_access', 'concepts']]
    
    df['open_access'] = df['open_access'].apply(lambda x: x['is_oa'])

    df = extrair_concepts_scores(df)
    
    #df = extrair_concepts(df)
    

    return df

def processar_e_salvar_parquet(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    parquet_files = [file for file in os.listdir(input_folder) if file.endswith(".parquet")]
    
    try:
        for parquet_file in parquet_files:
            input_path = os.path.join(input_folder, parquet_file)
            df_original = pd.read_parquet(input_path)  
            df_processado = processar_dataframe(df_original) 
            
            output_file = os.path.splitext(parquet_file)[0] + ".parquet"
            output_path = os.path.join(output_folder, output_file)
            
            df_processado.to_parquet(output_path, index=False)

    except Exception as error:
        print(error)
        print(parquet_file)
        
def concatenar_arquivos_parquet(folder_path):
    dataframes = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.parquet'):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_parquet(file_path)
            dataframes.append(df)

    df_concatenado = pd.concat(dataframes, ignore_index=True)
    
    df_concatenado.iloc[:,4:] = df_concatenado.iloc[:,4:].fillna(0)
    
    df_concatenado.dropna(subset=['doi', 'title'],inplace=True)
    
    df_concatenado.to_parquet('df_concatenado.parquet', index=False)
    
    
    
coletar_dados_e_salvar('2023-10-02','2023-10-08')

processar_e_salvar_parquet('datasets_2023-10-02_to_2023-10-08', 'datasets_2023-10-02_to_2023-10-08_processados')

concatenar_arquivos_parquet('datasets_2023-10-02_to_2023-10-08_processados')