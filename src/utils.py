import os
import numpy as np

def getInputs(input):
    path = "..\\inputs\\"
    dir = os.listdir(path)
    if os.path.exists(path) and not os.path.isfile(path):
        if len(dir) != 0:
            for file in dir:
                if file == input:
                    f = open(os.path.join(path, file), "r")

    sources = []
    xrange = []
    yrange = []
    points = []


    lines = [line.rstrip() for line in f]
    for i in range(len(lines)):
        line = lines[i].split(': ')
        name = line[0]

        if name == 'Mesh_Size':
            n = int(line[1])

        elif name == 'Sources':
            if ', ' in line[1]:
                values = line[1].split(', ')
                for value in values:
                    sources.append(int(value))
            else:
                sources.append(int(line[1]))

        elif name == 'X_lower':
            xrange.append(int(line[1]))
        elif name == 'X_upper':
            xrange.append(int(line[1]))
        elif name == 'Y_lower':
            yrange.append(int(line[1]))
        elif name == 'Y_upper':
            yrange.append(int(line[1]))

        elif name == 'Location_mesh':
            if ', ' in line[1]:
                values = line[1].split(', ')
                for value in values:
                    points.append(int(value))
            else:
                points.append(0)
                points.append(int(line[1]))

        elif name == 'Sigma_transport':
            sT = float(line[1])
        elif name == 'Sigma_absorption':
            sA = float(line[1])

        elif name == 'Tolerance':
            tolerance = float(line[1])

        elif name == 'Uniform':
            Uniform = line[1]

    if len(points) != 2:
        points = np.reshape(points, (int(len(points) / 2), 2))


    if Uniform == 'False':  # Checks to See if Source is a Point/(s)
        Points = [0]
        Points[0] = 1
        for i in range(0, len(points)):
            Points.append([points[i][0], points[i][1]])
        return n, xrange, yrange, sources, sT, sA, Points, tolerance
    else:
        return n, xrange, yrange, sources, sT, sA, points, tolerance