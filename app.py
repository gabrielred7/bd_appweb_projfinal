import sqlite3
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('database/esports.db')

# Consulta SQL para encontrar o jogo menos jogado
consulta_sql = """
SELECT jogo, COUNT(*) AS total_aparicoes
FROM (
    SELECT fk_Jogo_Titulo AS jogo FROM joga
    UNION ALL
    SELECT fk_Jogo_Titulo AS jogo FROM disputa
) AS combinadas
GROUP BY jogo
ORDER BY total_aparicoes
LIMIT 1;
"""

# Executar a consulta SQL e obter os resultados em um DataFrame
df = pd.read_sql_query(consulta_sql, conn)

# Fechar a conexão com o banco de dados
conn.close()

# Iniciar a aplicação Dash
app = dash.Dash(__name__)

# Layout da aplicação
app.layout = html.Div([
    html.H1("Gráfico do Jogo Menos Jogado em E-sports"),
    dcc.Graph(id='graph'),
    dcc.Interval(
        id='dummy-interval',
        interval=86400000,  # 24 horas em milissegundos
        disabled=True  # desabilitar o intervalo
    ),
])

# Callback para atualizar o gráfico com os dados
@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('dummy-interval', 'n_intervals')]
)
def update_graph(n):
    fig = px.bar(df, x='jogo', y='total_aparicoes', title='Jogo Menos Jogado em E-sports')
    return fig

# Executar a aplicação
if __name__ == '__main__':
    app.run_server(debug=True)
