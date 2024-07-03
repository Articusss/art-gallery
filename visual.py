import matplotlib.pyplot as plt

def plot_polygon(points : list[tuple[int,int]]) -> None:
    '''Plots a polygon, given a list of (x,y) coordinates in some order'''
    x = [x[0] for x in points] + [points[0][0]]
    y = [x[1] for x in points] + [points[0][1]]

    plt.plot(x,y)
    for i, (x,y) in enumerate(points):
        plt.text(x,y,i)
    plt.show()

def plot_triangulation(points: list[tuple[int,int]], triangles: list[tuple[int,int,int]], 
                       colors = None) -> None:
    '''Plots triangles'''
    for t in triangles:
        sides = [points[x] for x in t]
        x = [x[0] for x in sides] + [sides[0][0]]
        y = [x[1] for x in sides] + [sides[0][1]]
        plt.plot(x,y)
    
    if colors == None:
        plt.scatter([x[0] for x in points], [x[1] for x in points], zorder=10)
    else:
        for color,label in [('b', 0), ('r', 1), ('g', 2)]:
            point_color = [points[i] for i, val in enumerate(points) if colors[i] == label]
            plt.scatter([x[0] for x in point_color], [x[1] for x in point_color], c=color, zorder=10)
    
    plt.show()