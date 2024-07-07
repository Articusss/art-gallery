import dash
from dash import html, dcc, Input, Output
import plotly.graph_objects as go
import util
import novo



def inicia_o_grafico():
    fig = go.Figure()
    fig.update_layout(width=2400, height=1200)
    x = [x[0] for x in estados_cortados[0]] + [estados_cortados[0][0][0]]
    y = [x[1] for x in estados_cortados[0]] + [estados_cortados[0][0][1]]
    main_trace = go.Scatter(x=x, y=y, mode="lines+markers", name="Main Trace", line=dict(color='blue', width=2))
    fig.add_trace(main_trace)
    return fig

def encontra_elemento_removido(lista_atual, lista_atualizada):
    for element in lista_atual:
        if element not in lista_atualizada:
            return element
        
def encontra_indices_adjacentes(lista, elemento):
    indice = lista.index(elemento)
    indice_anterior = (indice - 1) % len(lista)
    indice_proximo = (indice + 1) % len(lista)
    return indice_anterior, indice_proximo

num_points, points = util.read_file("instances-simple/simple-20-1.pol")
# Dados de exemplo



vertice_atual = 0


triangulos, estados_cortados = novo.earclip(points)

# Inicializa o aplicativo Dash
app = dash.Dash(__name__)

# Layout do aplicativo
app.layout = html.Div([
    dcc.Graph(id='live-graph', figure=inicia_o_grafico()),
    html.Button('Play', id='play-button', n_clicks=0),
    
])


# Callback para atualizar o gráfico
@app.callback(
    Output('live-graph', 'figure'),
    [Input('play-button', 'n_clicks')]
)
def update_graph(n_clicks):
    global vertice_atual
    if(n_clicks > 0):
        fig = go.Figure()
        fig.update_layout(width=2400, height=1200)
        

        if n_clicks % 2 == 1:
            x_atual = [x[0] for x in estados_cortados[vertice_atual]] + [estados_cortados[vertice_atual][0][0]]
            y_atual = [x[1] for x in estados_cortados[vertice_atual]] + [estados_cortados[vertice_atual][0][1]]

            x_proximo = [x[0] for x in estados_cortados[vertice_atual + 1]] + [estados_cortados[vertice_atual + 1][0][0]]
            y_proximo = [x[1] for x in estados_cortados[vertice_atual + 1]] + [estados_cortados[vertice_atual + 1][0][1]]

            
            main_trace = go.Scatter(x=x_atual, y=y_atual, mode="lines+markers", name="Main Trace", line=dict(color='blue', width=2))
            fig.add_trace(main_trace)
            x_removido = encontra_elemento_removido(x_atual, x_proximo)
            y_removido = encontra_elemento_removido(y_atual, y_proximo)
    
            indice_anterior, indice_proximo = encontra_indices_adjacentes(x_atual, x_removido)
            x_traces = [x_atual[indice_anterior], x_removido, x_atual[indice_proximo]]
            y_traces = [y_atual[indice_anterior], y_removido, y_atual[indice_proximo]]
            
            traces = go.Scatter(x=x_traces, y=y_traces, mode="lines", line=dict(color='red', width=3))
            fig.add_trace(traces)
        else:
            vertice_atual+=1
            x_atual = [x[0] for x in estados_cortados[vertice_atual]] + [estados_cortados[vertice_atual][0][0]]
            y_atual = [x[1] for x in estados_cortados[vertice_atual]] + [estados_cortados[vertice_atual][0][1]]

            x_proximo = [x[0] for x in estados_cortados[vertice_atual + 1]] + [estados_cortados[vertice_atual + 1][0][0]]
            y_proximo = [x[1] for x in estados_cortados[vertice_atual + 1]] + [estados_cortados[vertice_atual + 1][0][1]]

            
            main_trace = go.Scatter(x=x_atual, y=y_atual, mode="lines+markers", name="Main Trace", line=dict(color='blue', width=2))
            fig.add_trace(main_trace)

        # Configura transições suaves para o gráfico
        fig.update_layout(transition={'duration': 500, 'easing': 'cubic-in-out'})

        
        return fig
    else:
        if n_clicks % 2 ==0:
            vertice_atual+=1
        return inicia_o_grafico()

# Executa o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)