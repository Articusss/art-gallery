def read_file(filepath : str) -> tuple[int, list[tuple[int,int]]]:
    '''Reads a polygon file and returns points on an (x,y) format'''
    with open(filepath, "r") as f:
        data = f.readlines()[0].rstrip().split(" ")
        num_points = int(data[0])
        divided = [int(x)/int(y) for x,y in [st.split("/") for st in data[1:]]]
        points = [(divided[i], divided[i+1]) for i in range(0, len(divided), 2)]

        return num_points, points
    
def build_graph_from_triangles(triangles : list[int]) -> list[list[int]]:
    '''Build a graph for triangles. Vertices are the triangles, and the edges are if they share an edge'''
    g = [[] for _ in range(len(triangles))]

    for idx, (v1, v2, v3) in enumerate(triangles):
        #Edge if two triangles share and edge -> Have two points in common
        edges = [(v1, v2), (v1,v3), (v2,v3)]
        for t_idx, t in enumerate(triangles):
            for e1, e2 in edges:
                if e1 in t and e2 in t:
                    g[idx].append(t_idx)
    return g