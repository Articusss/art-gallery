import util
import algo
import visual
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='Input file')
    args = parser.parse_args()

    num_points, points = util.read_file(args.input_file)
    #visual.plot_polygon(points)
    triangles = algo.earclip(points)
    graph = util.build_graph_from_triangles(triangles)
    colors = algo.tri_color_graph(graph, triangles, len(points))
    visual.plot_triangulation(points, triangles, colors)