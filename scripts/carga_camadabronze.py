import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# 1. Carregar configurações do .env
load_dotenv()

def carregar_dados():
    # Configurações de conexão
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    db = os.getenv('DB_NAME')

    # Criar a conexão com o banco do Docker
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    
    path_raw = 'data_raw/'
    
    # 2. Listar todos os arquivos CSV na pasta
    arquivos = [f for f in os.listdir(path_raw) if f.endswith('.csv')]
    
    print(f"--- Iniciando carga de {len(arquivos)} arquivos ---")

    for arquivo in arquivos:
        # Criar nome da tabela baseado no nome do arquivo (removendo .csv e o prefixo 'olist_')
        nome_tabela = arquivo.replace('.csv', '').replace('olist_', '')
        
        print(f"Lendo arquivo: {arquivo}...")
        
        # 3. Leitura com Pandas
        df = pd.read_csv(os.path.join(path_raw, arquivo))
        
        # 4. Carga para o Postgres
        # if_exists='replace' garante que ele crie a tabela se não existir
        df.to_sql(nome_tabela, engine, if_exists='replace', index=False)
        
        print(f"Sucesso: Dados carregados na tabela '{nome_tabela}'.")

    print("--- Carga finalizada com sucesso! ---")

if __name__ == "__main__":
    carregar_dados()