import os
import pandas as pd


#FUNÇÕES

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
    

#EXECUÇÃO

concatenar_arquivos_parquet('datasets_2023-10-02_to_2023-10-08_processados')