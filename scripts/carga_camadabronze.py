import os
import logging
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateSchema 
from sqlalchemy import text
from dotenv import load_dotenv

# Busca os dados no arquivo .env
load_dotenv()

def carregar_dados():
    # Configurações de conexão utilizando os dados do arquivo .env
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    db = os.getenv('DB_NAME')

    # Criar a conexão com o banco do Docker
    banco_login = (f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine = create_engine(banco_login)

    print("Verificando/Criando schema bronze...")
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS bronze;"))
        conn.commit()

    path_raw = 'data_raw'
    
    # 2. Listar todos os arquivos CSV na pasta
    arquivos = [f for f in os.listdir(path_raw) if f.endswith('.csv')]
    
    print(f"--- Iniciando carga de {len(arquivos)} arquivos ---")

    for arquivo in arquivos:
        # Criar nome da tabela baseado no nome do arquivo (removendo .csv, _dataset e o prefixo 'olist_')
        nome_tabela = arquivo.replace('.csv', '').replace('olist_', '').replace('_dataset', '')
        
        print(f"Lendo arquivo: {arquivo}...")
        
        # 3. Leitura com Pandas
        df = pd.read_csv(os.path.join(path_raw, arquivo))
        
        # 4. Carga para o Postgres
        # if_exists='replace' garante que ele crie a tabela se não existir
        df.to_sql(nome_tabela, engine, schema='bronze', if_exists='replace', index=True)
        
        print(f"Sucesso: Dados carregados na tabela '{nome_tabela}'.")

    print("--- Carga finalizada com sucesso! ---")

if __name__ == "__main__":
    carregar_dados()