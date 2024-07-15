import dash
from dash import html, dcc, Input, Output
import plotly.graph_objects as go
import util
import algo
import sys
class GraphAnimator:
    def __init__(self, file_path):
        self.vertice_atual = 0
        self.triangulo_atual = 0
        self.is_ear_clip = True
        self.x_removidos = []
        self.y_removidos = []
        self.xs_triangulo = []
        self.ys_triangulo = []
        self.num_points, self.points = util.read_file(file_path)
        self.triangulos, self.estados_cortados = algo.earclip(self.points)
        self.graph = util.build_graph_from_triangles(self.triangulos)
        self.vertices_cor = algo.tri_color_graph(self.graph, self.triangulos, len(self.points))
        self.x_original = self.get_x_vertex(0, self.estados_cortados)
        self.y_original = self.get_y_vertex(0, self.estados_cortados)

    def inicia_o_grafico(self):
        fig = go.Figure()
        fig.update_layout(width=2400, height=1200)
        self.show_main_trace(fig, self.x_original, self.y_original)
        return fig

    def get_x_vertex(self, state, list_states):
        return [x[0] for x in list_states[state]] + [list_states[state][0][0]]

    def get_y_vertex(self, state, list_states):
        return [y[1] for y in list_states[state]] + [list_states[state][0][1]]

    def show_main_trace(self, fig, x, y):
        main_trace = go.Scatter(x=x, y=y, mode="lines+markers", name="Main Trace", line=dict(color='blue', width=2))
        fig.add_trace(main_trace)

    def animation_get_ear_clip(self, fig):
        x_atual = self.get_x_vertex(self.vertice_atual, self.estados_cortados)
        y_atual = self.get_y_vertex(self.vertice_atual, self.estados_cortados)
        vertice_seguinte = self.vertice_atual + 1 if self.vertice_atual < len(self.estados_cortados) - 1 else 0
        x_proximo = self.get_x_vertex(vertice_seguinte, self.estados_cortados)
        y_proximo = self.get_y_vertex(vertice_seguinte, self.estados_cortados)

        self.show_main_trace(fig, x_atual, y_atual)

        x_removido = self.find_deleted_element(x_atual, x_proximo) if vertice_seguinte > 0 else x_atual[0]
        y_removido = self.find_deleted_element(y_atual, y_proximo) if vertice_seguinte > 0 else y_atual[0]
        self.x_removidos.append(x_removido)
        self.y_removidos.append(y_removido)

        self.show_triangles(fig)
        if self.is_ear_clip:
            self.show_current_ear_clip(fig, x_atual, y_atual, x_removido, y_removido)

    def find_deleted_element(self, lista_atual, lista_atualizada):
        for element in lista_atual:
            if element not in lista_atualizada:
                return element

    def show_triangles(self, fig):
        for x, y in zip(self.xs_triangulo, self.ys_triangulo):
            fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(width=3)))

    def show_current_ear_clip(self, fig, x_atual, y_atual, x_removido, y_removido):
        if x_removido is None or y_removido is None:
            return 
        pontos_atuais = list(zip(x_atual, y_atual))
        indice_anterior, indice_proximo = self.find_adjacent_indices(pontos_atuais,(x_removido, y_removido))
        x_traces = [x_atual[indice_anterior], x_removido, x_atual[indice_proximo]]
        y_traces = [y_atual[indice_anterior], y_removido, y_atual[indice_proximo]]
        traces = go.Scatter(x=x_traces, y=y_traces, mode="lines", line=dict(color='red', width=6))
        fig.add_trace(traces)

    def find_adjacent_indices(self,pontos, ponto):
        indice = pontos.index(ponto)
        indice_anterior = (indice - 1) % len(pontos)
        indice_proximo = (indice + 1) % len(pontos)
        return indice_anterior, indice_proximo
    
    def update_triangles(self, state):
        triangle = self.triangulos[state -1]
        sides = [self.points[x] for x in triangle ]
        x_triangle = [x[0] for x in sides] + [sides[0][0]]
        y_triangle = [x[1] for x in sides] + [sides[0][1]]

        self.xs_triangulo.append(x_triangle)
        self.ys_triangulo.append(y_triangle)
    
    def animation_new_graph_after_ear_clip(self, fig):
        x_atual = [x[0] for x in self.estados_cortados[self.vertice_atual]] + [self.estados_cortados[self.vertice_atual][0][0]]
        y_atual = [x[1] for x in self.estados_cortados[self.vertice_atual]] + [self.estados_cortados[self.vertice_atual][0][1]]

        self.update_triangles(self.vertice_atual)
        self.show_main_trace(fig, x_atual, y_atual)
        self.show_triangles(fig)

    def cor_vertice(self, indice_cor):
        if indice_cor == 0:
            return 'blue'
        elif indice_cor == 1:
            return 'red'
        elif indice_cor == 2:
            return 'green'
        return 'black'

    def get_index(self, x,y):
        return self.points.index((x,y))

    def show_removed_vertex(self, fig, x_removed, y_removed):
        for x,y in zip(x_removed, y_removed):
            color_indice = self.vertices_cor[self.get_index(x,y)]
            fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers", marker=dict(color=self.cor_vertice(color_indice), size=20))) 
    
    def show_colors(self, fig, x_triangles, y_triangles):
        for xs_triangle, ys_triangle in zip(x_triangles, y_triangles):
            self.show_removed_vertex(fig, xs_triangle, ys_triangle)

    def animation_colors(self, fig):
        xs_triangulo_atual = self.xs_triangulo[:self.triangulo_atual]
        ys_triangulo_atual = self.ys_triangulo[:self.triangulo_atual]
        self.show_triangles(fig)
        self.show_colors(fig, xs_triangulo_atual, ys_triangulo_atual)

    def update_graph(self, n_clicks):
        if n_clicks > 0 and self.vertice_atual < len(self.estados_cortados) - 1:
            fig = go.Figure()
            fig.update_layout(width=2400, height=1200)
            if self.is_ear_clip:
                self.animation_get_ear_clip(fig)
                self.is_ear_clip = False
            else:
                self.vertice_atual += 1
                self.animation_new_graph_after_ear_clip(fig)
                self.is_ear_clip = True
            return fig
        elif self.triangulo_atual < len(self.xs_triangulo) - 1:
            fig = go.Figure()
            fig.update_layout(width=2400, height=1200)
            self.triangulo_atual += 1
            self.animation_colors(fig)
            return fig
        return self.inicia_o_grafico()
        

    def update_graph_back(self, n_clicks):
        fig = go.Figure()
        fig.update_layout(width=2400, height=1200)
        if n_clicks > 0:
            if self.triangulo_atual > 0:
                self.triangulo_atual-=1
                self.animation_colors(fig)
                return fig
            elif not self.is_ear_clip:
                x_atual = [x[0] for x in self.estados_cortados[self.vertice_atual]] + [self.estados_cortados[self.vertice_atual][0][0]]
                y_atual = [x[1] for x in self.estados_cortados[self.vertice_atual]] + [self.estados_cortados[self.vertice_atual][0][1]]
                self.show_main_trace(fig, x_atual, y_atual)
                self.show_triangles(fig)
                self.is_ear_clip = True
                return fig  
            elif self.vertice_atual > 0 and len(self.xs_triangulo) > 0:
                self.xs_triangulo.pop()
                self.ys_triangulo.pop()
                self.vertice_atual-=1
                x_atual = [x[0] for x in self.estados_cortados[self.vertice_atual]] + [self.estados_cortados[self.vertice_atual][0][0]]
                y_atual = [x[1] for x in self.estados_cortados[self.vertice_atual]] + [self.estados_cortados[self.vertice_atual][0][1]]
                self.animation_get_ear_clip(fig)
                self.is_ear_clip = False
                return fig
        return self.inicia_o_grafico()
            

graph_animator = None

app = dash.Dash(__name__)

def create_layout():
    figure = graph_animator.inicia_o_grafico() if graph_animator is not None else {}
    return html.Div([
        dcc.Graph(id='live-graph', figure=figure),
         html.Button('Avancar', id='play-button', n_clicks=0, 
                style={'fontSize': '20px', 'padding': '10px 24px', 'minWidth': '100px'}),
    html.Button('Voltar', id='back-button', n_clicks=0, 
                style={'fontSize': '20px', 'padding': '10px 24px', 'minWidth': '100px'}),
    ])

@app.callback(
    Output('live-graph', 'figure', allow_duplicate=True),
    [Input('play-button', 'n_clicks')],
    prevent_initial_call=True
)
def update_graph(n_clicks):
    return graph_animator.update_graph(n_clicks)

@app.callback(
    Output('live-graph', 'figure'),
    [Input('back-button', 'n_clicks')]
)
def update_graph_back(n_clicks):
    return graph_animator.update_graph_back(n_clicks)

if __name__ == '__main__':

    if len(sys.argv) != 2:
        file_path = "instances-other\StSerninH.pol"
        print("Necessário caminho do arquivo. Comando correto: python animation.py <caminho_do_arquivo>")
        #ssys.exit(1)
    else:
        file_path = sys.argv[1]

    graph_animator = GraphAnimator(file_path)
    app.layout = create_layout()
    app.run_server(debug=True)