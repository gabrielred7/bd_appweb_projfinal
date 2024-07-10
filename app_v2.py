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

consulta_4 = """
SELECT c.Continente_Nome AS Continente,
    SUM(j.Premio_Acumulado) AS Premiacao_Total_Por_Continente
FROM jogador j
JOIN pais p ON LOWER(j.fk_Pais_Sigla_Principal) = LOWER(p.Sigla_Principal)
JOIN pertence pe ON p.Sigla_Principal = pe.fk_Pais_Sigla_Principal
JOIN Continente c ON pe.fk_Continente_Continente_Nome = c.Continente_Nome
GROUP BY c.Continente_Nome
ORDER BY Premiacao_Total_Por_Continente DESC;
"""

consulta_5 = """
SELECT c.Continente_Nome, COUNT(DISTINCT jo.JogadorID) AS Total_Jogadores
FROM jogador jo
INNER JOIN pais p ON LOWER(jo.fk_Pais_Sigla_Principal) = LOWER(p.Sigla_Principal)
INNER JOIN pertence pe ON p.Sigla_Principal = pe.fk_Pais_Sigla_Principal
INNER JOIN continente c ON pe.fk_Continente_Continente_Nome = c.Continente_Nome
GROUP BY c.Continente_Nome
ORDER BY Total_Jogadores
DESC;
"""

# Executar a consulta SQL e obter os resultados em um DataFrame
df_1 = pd.read_sql_query(consulta_1, conn)
df_2 = pd.read_sql_query(consulta_2, conn)
df_3 = pd.read_sql_query(consulta_3, conn)
df_4 = pd.read_sql_query(consulta_4, conn)
df_5 = pd.read_sql_query(consulta_5, conn)

conn.close()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Análise de E-sports"),
    html.Div([
        html.H2("Jogo Menos Jogado"),
        html.Div(id='jogo-menos-jogado'),
    ]),
    html.Div([
        html.H2("Total Pago aos Jogadores"),
        html.Div(id='total-pago-jogadores')
    ]),
    html.Div([
        html.H2("Países Participantes da América do Sul"),
        html.Ul(id='lista-paises-am-sul')
    ]),
    html.Div([
        html.H2("Gráfico do Prêmio Total de cada Continente"),
        dcc.Graph(id='graph-total-premio-continente'),
    ]),
    html.Div([
        html.H2("Gráfico da Quantidade de Jogadores por Continente"),
        dcc.Graph(id='graph-total-jogadores-continente'),
    ]),
    dcc.Interval(
        id='dummy-interval',
        interval=86400000,  # 24 horas em milissegundos
        disabled=True  # desabilitar o intervalo
    ),
])


# Callback para atualizar o gráfico do jogo menos jogado
@app.callback(dash.dependencies.Output('jogo-menos-jogado', 'children'),
              [dash.dependencies.Input('dummy-interval', 'n_intervals')])
def update_graph_jogo_menos_jogado(n):
    jogo_menos_jogado = df_1.loc[df_1['total_aparicoes'].idxmin(), 'jogo']
    return jogo_menos_jogado


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


# Callback para atualizar o total de prêmio dos jogadores arrecadado por cada
# continente
@app.callback(
    dash.dependencies.Output('graph-total-premio-continente', 'figure'),
    [dash.dependencies.Input('dummy-interval', 'n_intervals')])
def update_graph_total_premio_continente(n):
    fig = px.bar(df_4,
                 x='Continente',
                 y='Premiacao_Total_Por_Continente',
                 title='Prêmio total arrecadado por continente')
    return fig


# Callback para atualizar o total de jogadores por continente
@app.callback(
    dash.dependencies.Output('graph-total-jogadores-continente', 'figure'),
    [dash.dependencies.Input('dummy-interval', 'n_intervals')])
def update_graph_total_jogadores_continente(n):
    fig = px.bar(df_5,
                 x='Continente_Nome',
                 y='Total_Jogadores',
                 title='Quantidade de jogadores por continente')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
