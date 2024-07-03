import util
import algo
import visual

if __name__ == "__main__":
    num_points, points = util.readFile("instances-simple/simple-20-1.pol")
    visual.plotPolygon(points)
    sol = algo.earclip(points)
    visual.plotTriangulation(points, sol)