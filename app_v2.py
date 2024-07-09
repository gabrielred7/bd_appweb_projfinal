import sqlite3
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('database/esports.db')

# Consultas SQL
consulta_1 = """
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

consulta_2 = """
SELECT SUM(Premio_Acumulado) AS PREMIACAO_TOTAL_JOGADORES
FROM jogador;
"""

consulta_3 = """
SELECT DISTINCT Nome FROM pais
JOIN pertence ON fk_Pais_Sigla_Principal=Sigla_Principal
AND fk_Continente_Continente_Nome='South America'
LIMIT 5;
"""

# Executar a consulta SQL e obter os resultados em um DataFrame
df_1 = pd.read_sql_query(consulta_1, conn)
df_2 = pd.read_sql_query(consulta_2, conn)
df_3 = pd.read_sql_query(consulta_3, conn)

conn.close()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Análise de E-sports"),
    html.Div([
        html.H2("Gráfico do Jogo Menos Jogado"),
        dcc.Graph(id='graph-jogo-menos-jogado'),
    ]),
    html.Div([
        html.H2("Total Pago aos Jogadores"),
        html.Div(id='total-pago-jogadores')
    ]),
    html.Div([
        html.H2("Países Participantes da América do Sul"),
        html.Ul(id='lista-paises-am-sul')
    ]),
    dcc.Interval(
        id='dummy-interval',
        interval=86400000,  # 24 horas em milissegundos
        disabled=True  # desabilitar o intervalo
    ),
])


# Callback para atualizar o gráfico do jogo menos jogado
@app.callback(dash.dependencies.Output('graph-jogo-menos-jogado', 'figure'),
              [dash.dependencies.Input('dummy-interval', 'n_intervals')])
def update_graph_jogo_menos_jogado(n):
    fig = px.bar(df_1,
                 x='jogo',
                 y='total_aparicoes',
                 title='Jogo Menos Jogado em E-sports')
    return fig


# Callback para atualizar o total pago aos jogadores
@app.callback(dash.dependencies.Output('total-pago-jogadores', 'children'),
              [dash.dependencies.Input('dummy-interval', 'n_intervals')])
def update_total_pago_jogadores(n):
    total_pago = df_2.iloc[0]['PREMIACAO_TOTAL_JOGADORES']
    return f"Total Pago aos Jogadores: R$ {total_pago:,}"


# Callback para atualizar a lista de países participantes da América do Sul
@app.callback(dash.dependencies.Output('lista-paises-am-sul', 'children'),
              [dash.dependencies.Input('dummy-interval', 'n_intervals')])
def update_lista_paises_am_sul(n):
    lista_paises = html.Ul([html.Li(pais) for pais in df_3['Nome']])
    return lista_paises


if __name__ == '__main__':
    app.run_server(debug=True)
