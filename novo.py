from copy import deepcopy

def signal(p0, p1, p2) -> float:
    '''Returns (p2p0) x (p2p1)'''
    return (p0[0]-p2[0]) * (p1[1]-p2[1]) - (p1[0]-p2[0]) * (p0[1]-p2[1])

def point_in_triangle(p0 : tuple[int,int], p1 : tuple[int,int], 
                      p2 : tuple[int,int], checked_point : tuple[int,int]) -> bool:
    '''Check if checked_point is inside triangle formed by p1,p2,p3'''
    
    d1 = signal(checked_point, p0, p1)
    d2 = signal(checked_point, p1, p2)
    d3 = signal(checked_point, p2, p0)

    has_neg = d1 < 0 or d2 < 0 or d3 < 0
    has_pos = d1 > 0 or d2 > 0 or d3 > 0

    return not(has_neg and has_pos)

def any_point_in_triangle(p0 : tuple[int,int], p1 : tuple[int,int], 
                          p2 : tuple[int,int], points : list[tuple[int,int]]) -> bool:
    '''Check if ANY point in points is inside triangle'''
    for p_check in points:
        if p_check != p0 and p_check != p1 and p_check != p2 and point_in_triangle(p0,p1,p2,p_check):
            return True
    return False

def check_ear(idx : int, points : list[tuple[int,int]]) -> bool:
    '''Check if index idx is an ear'''
    n = len(points)
    t = [points[(idx-1)%n], points[idx], points[(idx+1)%n]]
    return signal(t[1],t[2],t[0]) > 0 and not any_point_in_triangle(*t, points)

def earclip(points : list[tuple[int,int]]):
    '''Triangulate a polygon using ear clipping method, given a list of (x,y) points'''
    ears = {i for i in range(len(points)) if check_ear(i, points)}
    to_remove = list(range(len(points)))
    trimmed_polygon = deepcopy(points)
    trimmed_states = []
    trimmed_states.append(deepcopy(trimmed_polygon))
    triangles = []
    while len(to_remove) > 3:
        #Choose an ear to remove, remove
        curr_ear = ears.pop()
        idx = to_remove.index(curr_ear)

        #Add to triangles and remove from to_remove
        n = len(to_remove)
        triangles.append((to_remove[(idx-1) % n], to_remove[idx], to_remove[(idx+1) % n]))

        #Remove from structures
        to_remove.remove(curr_ear)
        del trimmed_polygon[idx]
        trimmed_states.append(deepcopy(trimmed_polygon))
        #Check if adjacent became ears, since idx was removed next is also idx
        for cand in [(idx - 1) % len(to_remove), idx % len(to_remove)]:
            if check_ear(cand, trimmed_polygon):
                ears.add(to_remove[cand])
            elif to_remove[cand] in ears:
                ears.remove(to_remove[cand])
    #Insert last triangle
    triangles.append(tuple(to_remove))
    return triangles, trimmed_states

def dfs_color(graph : list[list[int]], triangles : list[tuple[int,int,int]],
              vertice : int, visited : list[bool], colors : list[int]) -> None:
    '''Run DFS on triangulation graph, assigning colors to each vertice'''
    visited[vertice] = True
    
    #2 vertices of this triangle should already be colored, find that vertice and the remaining color
    curr_colors = [colors[v] for v in triangles[vertice]]
    remaining_color = ({0,1,2,-1} - set(curr_colors)).pop() #Find remaining color
    colors[triangles[vertice][curr_colors.index(-1)]] = remaining_color #Color remaining vertice

    #Continue DFS
    for neighbor in graph[vertice]:
        if not visited[neighbor]: dfs_color(graph, triangles, neighbor, visited, colors)

def tri_color_graph(graph : list[list[int]], triangles : list[tuple[int,int,int]], 
                    num_points : int) -> list[int]:
    '''3-colors a triangularization graph'''
    #Colors will be 0,1,2. -1 means no color
    colors = [-1] * num_points

    #Start by assigning colors for each vertice of first triangle
    v1, v2, v3 = triangles[0]
    colors[v1] = 0
    colors[v2] = 1

    #Run DFS on our graph
    visited = [False] * len(graph)
    dfs_color(graph, triangles, 0, visited, colors)

    return colors
