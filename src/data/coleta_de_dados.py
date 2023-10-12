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
    
#EXECUÇÃO


coletar_dados_e_salvar('2023-10-02','2023-10-08')

