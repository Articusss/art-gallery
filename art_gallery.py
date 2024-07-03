import src.util
import src.algo
import src.visual

if __name__ == "__main__":
    num_points, points = util.readFile("instances-simple/simple-20-1.pol")
    sol = algo.earclip(points)
    visual.plotTriangulation(points, sol)
    visual.plotPolygon(points)