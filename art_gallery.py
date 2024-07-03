import util
import algo
import visual

if __name__ == "__main__":
    num_points, points = util.read_file("instances-simple/simple-20-1.pol")
    visual.plot_polygon(points)
    sol = algo.earclip(points)
    visual.plot_triangulation(points, sol)