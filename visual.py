import matplotlib.pyplot as plt

def plot_polygon(points : list):
    '''Plots a polygon, given a list of (x,y) coordinates in some order'''
    x = [x[0] for x in points] + [points[0][0]]
    y = [x[1] for x in points] + [points[0][1]]

    plt.plot(x,y)
    for i, (x,y) in enumerate(points):
        plt.text(x,y,i)
    plt.show()

def plot_triangulation(points: list, triangles: list):
    '''Plots triangles'''
    plt.scatter([x[0] for x in points], [x[1] for x in points])
    for t in triangles:
        sides = [points[x] for x in t]
        x = [x[0] for x in sides] + [sides[0][0]]
        y = [x[1] for x in sides] + [sides[0][1]]
        plt.plot(x,y)
    
    plt.show()