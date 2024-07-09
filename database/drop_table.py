import sqlite3

# Conecte-se ao banco de dados (ou crie um novo)
conn = sqlite3.connect('esports.db')
cursor = conn.cursor()

# Consulte os nomes de todas as tabelas no banco de dados
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Apague cada tabela
for table in tables:
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {table[0]};")
        print(f"Tabela {table[0]} apagada com sucesso.")
    except sqlite3.OperationalError as e:
        print(f"Erro ao apagar a tabela {table[0]}: {e}")
    except Exception as e:
        print(f"Erro inesperado ao apagar a tabela {table[0]}: {e}")

# Feche a conexão
conn.commit()
conn.close()
