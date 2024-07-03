import util
import algo
import visual

if __name__ == "__main__":
    num_points, points = util.read_file("instances-simple/simple-20-1.pol")
    #visual.plot_polygon(points)
    triangles = algo.earclip(points)
    graph = util.build_graph_from_triangles(triangles)
    colors = algo.tri_color_graph(graph, triangles, len(points))
    visual.plot_triangulation(points, triangles, colors)