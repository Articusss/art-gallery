def readFile(filepath : str) -> tuple[int, list]:
    '''Reads a polygon file and returns points on an (x,y) format'''
    with open(filepath, "r") as f:
        data = f.readlines()[0].rstrip().split(" ")
        num_points = int(data[0])
        divided = [int(x)/int(y) for x,y in [st.split("/") for st in data[1:]]]
        points = [(divided[i], divided[i+1]) for i in range(0, len(divided), 2)]

        return num_points, points
