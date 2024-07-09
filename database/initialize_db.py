import sqlite3

# Conecte-se ao banco de dados (ou crie um novo)
conn = sqlite3.connect('esports.db')
cursor = conn.cursor()

# Lista de arquivos SQL
arquivos_sql = [
    "modelo_fisico/banco_dados_parte2_continente.sql",
    "modelo_fisico/banco_dados_parte2_disputa.sql",
    "modelo_fisico/banco_dados_parte2_joga.sql",
    "modelo_fisico/banco_dados_parte2_jogador.sql",
    "modelo_fisico/banco_dados_parte2_jogo.sql",
    "modelo_fisico/banco_dados_parte2_pais.sql",
    "modelo_fisico/banco_dados_parte2_pertence.sql",
    "modelo_fisico/banco_dados_parte2_time.sql"
]

# Carregue e execute cada arquivo SQL
for arquivo in arquivos_sql:
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        cursor.executescript(sql_script)
        print(f"Arquivo {arquivo} carregado com sucesso.")
    except sqlite3.OperationalError as e:
        print(f"Erro ao carregar {arquivo}: {e}")
    except Exception as e:
        print(f"Erro inesperado ao carregar {arquivo}: {e}")

# Feche a conexão
conn.commit()
conn.close()
