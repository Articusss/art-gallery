// Inicialização de variáveis
let points = [];
let triangulos = [];
let estados_cortados = [];
let vertices_cor = [];
let visit_order = [];
let current_ears = [];

let vertice_atual = 0;
let triangulo_atual = 0;
let is_ear_clip = true;
let x_removidos = [];
let y_removidos = [];
let xs_triangulo = [];
let ys_triangulo = [];
let i_triangulo = [];

// Função que será executada quando o documento HTML for completamente carregado
document.addEventListener('DOMContentLoaded', function () {
    // Carrega dados de um arquivo JSON
    fetch('output.json')
        .then(response => response.json())
        .then(data => {
            // Inicializa as variáveis com os dados do JSON
            points = data.points;
            triangulos = data.triangles;
            estados_cortados = data.trimmed_states;
            vertices_cor = data.colors;
            visit_order = data.visit_order;
            current_ears = data.current_ears;
            // Inicializa o gráfico
            inicia_o_grafico();
        })
        .catch(error => console.error('Error loading JSON:', error));

    // Adiciona eventos de clique aos botões
    document.getElementById('play-button').addEventListener('click', updateGraph);
    document.getElementById('back-button').addEventListener('click', updateGraphBack);
});

// Função para inicializar o gráfico
function inicia_o_grafico() {
    const trace = {
        x: estados_cortados[0].map(p => p[0]).concat(estados_cortados[0][0][0]),
        y: estados_cortados[0].map(p => p[1]).concat(estados_cortados[0][0][1]),
        mode: 'lines+markers',
        name: 'Main Trace',
        line: { color: 'blue', width: 2 }
    };
    const layout = { 
        annotations: [
            {
                text: '',
                showarrow: false,
                xref: 'paper',
                yref: 'paper',
                x: 0.5,
                y: 0.1,
                align: 'center',
                bgcolor: 'rgba(255, 255, 255, 0.6)',
                bordercolor: 'rgba(255, 255, 255, 0.6)',
                borderwidth: 2
            }
        ]
    };
    Plotly.newPlot('graph', [trace], layout);
    highlight_current_ears();
}

// Atualiza o gráfico para a próxima etapa
function updateGraph() {
    if (vertice_atual < estados_cortados.length) {
        if (is_ear_clip) {
            animation_get_ear_clip();
            is_ear_clip = false;
        } else {
            vertice_atual++;
            animation_new_graph_after_ear_clip();
            is_ear_clip = true;
        }
    } 
    else if (triangulo_atual < xs_triangulo.length) {
        triangulo_atual++;
        animation_colors(triangulo_atual);
    }
}

// Atualiza o gráfico para a etapa anterior
function updateGraphBack() {
    if (triangulo_atual > 0) {
        triangulo_atual--;
        animation_colors();
    } else if (is_ear_clip && vertice_atual > 0 && xs_triangulo.length > 0) {
        xs_triangulo.pop();
        ys_triangulo.pop();
        i_triangulo.pop();
        vertice_atual--;
        is_ear_clip = false;
        show_main_trace();
        show_triangles();
        is_ear_clip = true;
    } else {
        animation_get_ear_clip();
        is_ear_clip = false;
    }
}

// Mostra os triângulos atuais no gráfico
function show_triangles() {
    const currentTraces = graph.data.length;
    if (currentTraces > 1) {
        Plotly.deleteTraces('graph', Array.from(Array(currentTraces).keys()).slice(1));
    }

    const traces = xs_triangulo.map((x, i) => ({
        x: x.concat(x[0]),
        y: ys_triangulo[i].concat(ys_triangulo[i][0]),
        mode: 'lines',
        line: { width: 3 },
        fill: 'toself',
    }));

    Plotly.addTraces('graph', traces);

    if(!is_ear_clip){
        if(vertice_atual < estados_cortados.length) highlight_current_ears();
    }
}

// Mostra o traço principal no gráfico
function show_main_trace() {
    const x = estados_cortados[vertice_atual].map(p => p[0]).concat(estados_cortados[vertice_atual][0][0]);
    const y = estados_cortados[vertice_atual].map(p => p[1]).concat(estados_cortados[vertice_atual][0][1]);
    const trace = {
        x: x,
        y: y,
        mode: 'lines+markers',
        name: 'Main Trace',
        line: { color: 'blue', width: 2 },
    };
    Plotly.addTraces('graph', [trace]);
}

// Realiza a animação de recorte da orelha
function animation_get_ear_clip() {
    const x_atual = estados_cortados[vertice_atual].map(p => p[0]).concat(estados_cortados[vertice_atual][0][0]);
    const y_atual = estados_cortados[vertice_atual].map(p => p[1]).concat(estados_cortados[vertice_atual][0][1]);
    const vertice_seguinte = vertice_atual + 1 < estados_cortados.length ? vertice_atual + 1 : 0;
    const x_proximo = estados_cortados[vertice_seguinte].map(p => p[0]).concat(estados_cortados[vertice_seguinte][0][0]);
    const y_proximo = estados_cortados[vertice_seguinte].map(p => p[1]).concat(estados_cortados[vertice_seguinte][0][1]);

    const x_removido = encontra_elemento_removido(x_atual, x_proximo);
    const y_removido = encontra_elemento_removido(y_atual, y_proximo);
    x_removidos.push(x_removido);
    y_removidos.push(y_removido);

    show_triangles();
    if(vertice_atual < estados_cortados.length - 1) show_current_ear_clip(x_atual, y_atual, x_removido, y_removido);
}

// Atualiza o gráfico após o recorte da orelha
function animation_new_graph_after_ear_clip() {
    if(vertice_atual < estados_cortados.length - 1){
        const x_atual = estados_cortados[vertice_atual].map(p => p[0]).concat(estados_cortados[vertice_atual][0][0]);
        const y_atual = estados_cortados[vertice_atual].map(p => p[1]).concat(estados_cortados[vertice_atual][0][1]);
    }
    
    update_triangles();

    show_triangles();
}

// Atualiza as cores dos vértices
function animation_colors() {
    show_triangles();
    show_colors();
}

// Encontra o elemento removido entre duas listas
function encontra_elemento_removido(lista_atual, lista_atualizada) {
    return lista_atual.find(element => !lista_atualizada.includes(element));
}

// Atualiza a lista de triângulos
function update_triangles() {
    const triangle = triangulos[vertice_atual - 1];
    const sides = triangle.map(i => points[i]);
    const x_triangle = sides.map(p => p[0]).concat(sides[0][0]);
    const y_triangle = sides.map(p => p[1]).concat(sides[0][1]);
    const indices = triangle.map(i => i); // Copia os índices do triângulo atual
    i_triangulo.push(indices); 

    xs_triangulo.push(x_triangle);
    ys_triangulo.push(y_triangle);
}

// Mostra o recorte da orelha atual
function show_current_ear_clip(x_atual, y_atual, x_removido, y_removido) {
    const indices = encontra_indices_adjacentes(x_atual, x_removido);
    const x_traces = [x_atual[indices[0]], x_removido, x_atual[indices[1]]];
    const y_traces = [y_atual[indices[0]], y_removido, y_atual[indices[1]]];
    const trace = {
        x: x_traces,
        y: y_traces,
        mode: 'lines',
        line: { color: 'red', width: 6 }
    };
    Plotly.addTraces('graph', [trace]);

}

// Marca as orelhas atuais no gráfico
function highlight_current_ears() {
    const current_ears_traces = current_ears[vertice_atual].map(idx => ({
        x: [points[idx][0]],
        y: [points[idx][1]],
        mode: 'markers',
        marker: { color: 'red', size: 10 }
    }));
    Plotly.addTraces('graph', current_ears_traces);
}

// Encontra os índices dos vértices adjacentes
function encontra_indices_adjacentes(lista, elemento) {
    const indice = lista.indexOf(elemento);
    const indice_anterior = (indice - 1 + lista.length) % lista.length;
    const indice_proximo = (indice + 1) % lista.length;
    return [indice_anterior, indice_proximo];
}

// Mostra a coloração atual dos vértices
function show_colors() {
    const currentTraces = graph.data.length;
    if (currentTraces > 1) {
        Plotly.deleteTraces('graph', Array.from(Array(currentTraces).keys()).slice(1));
    }
    
    show_triangles();

    if(triangulo_atual == xs_triangulo.length){
        atualizarAnotacao(calcularMenorConjunto());
    }
    const vertices_colored = new Set();
    for (let i = 0; i <= triangulo_atual && i < xs_triangulo.length; i++) {
        const tri_index = visit_order[i];
        for (let j = 0; j < 3; j++) {
            const vertice = i_triangulo[tri_index][j];
            if (!vertices_colored.has(vertice)) { 
                const trace = {
                    x: [xs_triangulo[tri_index][j]],
                    y: [ys_triangulo[tri_index][j]],
                    mode: 'markers',
                    marker: { color: cor_vertice(vertices_cor[vertice]), size: 20 },
                };
                Plotly.addTraces('graph', trace);
                vertices_colored.add(vertice); 
            }
        }
    }

    // Destaca o triângulo atual com uma cor diferente
    if(triangulo_atual < xs_triangulo.length){
        const currentTriangle = visit_order[triangulo_atual];
        const traceHighlight = {
            x: xs_triangulo[currentTriangle].concat(xs_triangulo[currentTriangle][0]),
            y: ys_triangulo[currentTriangle].concat(ys_triangulo[currentTriangle][0]),
            mode: 'lines',
            line: { color: 'yellow', width: 6 }
        };
        Plotly.addTraces('graph', [traceHighlight]);
    }
}

// Calcula o menor conjunto de câmeras necessárias
function calcularMenorConjunto() {
    const freq = {};
    vertices_cor.forEach(cor => {
        if (freq[cor] === undefined) {
            freq[cor] = 1;
        } else {
            freq[cor]++;
        }
    });
    const menorConjunto = Math.min(...Object.values(freq));
    return menorConjunto;
}

// Retorna a cor do vértice com base no índice da cor
function cor_vertice(indice_cor) {
    if (indice_cor === 0) return 'blue';
    if (indice_cor === 1) return 'red';
    return 'green';
}

// Atualiza a anotação no gráfico
function atualizarAnotacao(menorConjunto) {
    Plotly.relayout('graph', {
        'annotations[0].text': `Mínimo de câmeras: ${menorConjunto}`,
    });
}
