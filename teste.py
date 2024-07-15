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

def cor_vertice(indice_cor):
    if indice_cor == 0:
        return 'blue'
    elif indice_cor == 1:
        return 'red'
    return 'green'

def show_triangles(fig):
    global xs_triangulo
    global ys_triangulo
    for x,y in zip(xs_triangulo, ys_triangulo):
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(width=3)))

def show_main_trace(fig, x, y):
    main_trace = go.Scatter(x=x, y=y, mode="lines+markers", name="Main Trace", line=dict(color='blue', width=2))
    fig.add_trace(main_trace)

def show_current_ear_clip(fig, x_atual, y_atual, x_removido, y_removido):
    indice_anterior, indice_proximo = encontra_indices_adjacentes(x_atual, x_removido)
    x_traces = [x_atual[indice_anterior], x_removido, x_atual[indice_proximo]]
    y_traces = [y_atual[indice_anterior], y_removido, y_atual[indice_proximo]]
    traces = go.Scatter(x=x_traces, y=y_traces, mode="lines", line=dict(color='red', width=6))
    fig.add_trace(traces)

def show_removed_vertex(fig, x_removed, y_removed):
    for x,y in zip(x_removed, y_removed):
        fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers", marker=dict(color=cor_vertice(vertices_cor[x_original.index(x)]), size=20))) 

def get_x_vertex(state, list_states):
    return [x[0] for x in list_states[state]] + [list_states[state][0][0]]

def get_y_vertex(state, list_states):
    return [y[1] for y in list_states[state]] + [list_states[state][0][1]]

def update_triangles(triangulos, state):
    triangle = triangulos[state -1]
    sides = [points[x] for x in triangle ]
    x_triangle = [x[0] for x in sides] + [sides[0][0]]
    y_triangle = [x[1] for x in sides] + [sides[0][1]]

    xs_triangulo.append(x_triangle)
    ys_triangulo.append(y_triangle)

def animation_get_ear_clip(fig, vertice_atual, estados_cortados):
    x_atual = get_x_vertex(vertice_atual, estados_cortados)
    y_atual = get_y_vertex(vertice_atual, estados_cortados)
    vertice_seguinte = vertice_atual + 1 if vertice_atual < len(estados_cortados) -1  else 0
    x_proximo = get_x_vertex(vertice_seguinte, estados_cortados)
    y_proximo = get_y_vertex(vertice_seguinte, estados_cortados)
            
    show_main_trace(fig, x_atual, y_atual)

    x_removido = encontra_elemento_removido(x_atual, x_proximo) if vertice_seguinte > 0 else x_atual[0]
    y_removido = encontra_elemento_removido(y_atual, y_proximo) if vertice_seguinte > 0 else y_atual[0]
    x_removidos.append(x_removido)
    y_removidos.append(y_removido)
    
    show_triangles(fig)
    show_current_ear_clip(fig, x_atual, y_atual, x_removido, y_removido)

def animation_new_graph_after_ear_clip(fig, vertice_atual, estados_cortados):
    x_atual = [x[0] for x in estados_cortados[vertice_atual]] + [estados_cortados[vertice_atual][0][0]]
    y_atual = [x[1] for x in estados_cortados[vertice_atual]] + [estados_cortados[vertice_atual][0][1]]
            
    update_triangles(triangulos, vertice_atual)

    show_main_trace(fig, x_atual, y_atual)
    show_triangles(fig)

def show_colors(fig, x_triangles, y_triangles):
    for xs_triangle, ys_triangle in zip(x_triangles, y_triangles):
        show_removed_vertex(fig, xs_triangle, ys_triangle)

def animation_colors(fig, xs_triangulo, ys_triangulo, triangulo_atual):
    xs_triangulo_atual = xs_triangulo[:triangulo_atual + 1]
    ys_triangulo_atual = ys_triangulo[:triangulo_atual + 1]
    show_triangles(fig)
    show_colors(fig, xs_triangulo_atual, ys_triangulo_atual)

num_points, points = util.read_file("instances-simple/simple-20-1.pol")

vertice_atual = 0
triangulo_atual = 0
is_ear_clip = True

triangulos, estados_cortados = novo.earclip(points)
graph = util.build_graph_from_triangles(triangulos)
vertices_cor = novo.tri_color_graph(graph, triangulos, len(points))





x_original = [x[0] for x in estados_cortados[0]] + [estados_cortados[0][0][0]]
y_original = [x[1] for x in estados_cortados[0]] + [estados_cortados[0][0][1]]

x_removidos = []
y_removidos = []

xs_triangulo = []
ys_triangulo = []

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='live-graph', figure=inicia_o_grafico()),
      html.Button('Play', id='play-button', n_clicks=0, 
                style={'fontSize': '20px', 'padding': '10px 24px', 'minWidth': '100px'}),
    html.Button('Voltar', id='back-button', n_clicks=0, 
                style={'fontSize': '20px', 'padding': '10px 24px', 'minWidth': '100px'}),
])


# Callback para atualizar o gráfico
@app.callback(
    Output('live-graph', 'figure',allow_duplicate=True),
    [Input('play-button', 'n_clicks')],
    prevent_initial_call=True
)
def update_graph(n_clicks):
    global vertice_atual
    global vertices_cor
    global x_original
    global y_original
    global x_removidos
    global y_removidos
    global xs_triangulo
    global ys_triangulo
    global triangulo_atual
    global is_ear_clip
    fig = go.Figure()
    fig.update_layout(width=2400, height=1200)
    if n_clicks > 0 and vertice_atual < len(estados_cortados) - 1:
        if is_ear_clip:
            animation_get_ear_clip(fig, vertice_atual, estados_cortados)
            is_ear_clip = False
        else:
            vertice_atual+=1
            animation_new_graph_after_ear_clip(fig, vertice_atual, estados_cortados)
            is_ear_clip = True

        return fig
    elif n_clicks == 0:
        return inicia_o_grafico()
    elif triangulo_atual < len(xs_triangulo) -1:
        animation_colors(fig, xs_triangulo, ys_triangulo, triangulo_atual)
        triangulo_atual+=1
        return fig
    


@app.callback(
    Output('live-graph', 'figure'),
    [Input('back-button', 'n_clicks')]
)
def update_graph_back(n_clicks):
    global vertice_atual
    global vertices_cor
    global x_original
    global y_original
    global x_removidos
    global y_removidos
    global xs_triangulo
    global ys_triangulo
    global triangulo_atual
    global is_ear_clip
    fig = go.Figure()
    fig.update_layout(width=2400, height=1200)
    if n_clicks > 0:
        if triangulo_atual > 0:
            triangulo_atual-=1
            animation_colors(fig, xs_triangulo, ys_triangulo, triangulo_atual)
            return fig
        elif  is_ear_clip and vertice_atual > 0 and len(xs_triangulo) > 0:
            xs_triangulo.pop()
            ys_triangulo.pop()
            vertice_atual-=1
            x_atual = [x[0] for x in estados_cortados[vertice_atual]] + [estados_cortados[vertice_atual][0][0]]
            y_atual = [x[1] for x in estados_cortados[vertice_atual]] + [estados_cortados[vertice_atual][0][1]]
            show_main_trace(fig, x_atual, y_atual)
            show_triangles(fig)
            is_ear_clip = True
            return fig  
        else:
            animation_get_ear_clip(fig, vertice_atual, estados_cortados)
            is_ear_clip = False
            return fig
    else:
        return inicia_o_grafico()


# Executa o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)