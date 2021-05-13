import numpy as np
from numpy.linalg import inv, norm
from numpy import zeros, diag, insert


def generate_mesh(n, xrange, yrange, sources, sT, sA, points):

    meshx = np.linspace(xrange[0], xrange[1], n)
    meshy = np.linspace(yrange[0], yrange[1], n)
    source = np.zeros((n, n))
    if points[0] == 1:  # Checks to See if Source is a Point/(s)
        for i in range(0, len(sources)):
            source[points[i + 1][1]][points[i + 1][0]] = sources[i]  # Assigns Source(i,j) to MeshGrid
    elif points[0] == 0:  # Checks to See if Source is Uniform
        source = sources[0] * np.ones((n, n))

    D = 1 / (3 * sT) * np.ones((n + 1, n + 1))
    sA = sA * np.ones((n + 1, n + 1))
    dx = abs(meshx[1] - meshx[0]) * np.ones(n + 1)
    dy = abs(meshy[1] - meshy[0]) * np.ones(n + 1)
    return meshx, meshy, source, sA, D, dx, dy


def gauss_seidel(A, B, x, tolerance):
    iterations = 0
    Y = np.tril(A)
    Z = A-Y
    while True:
        iterations += 1
        x0 = x
        x = np.dot(np.linalg.inv(Y), B - np.dot(Z, x))
        error = norm(x - x0) / norm(x)
        if error < tolerance:
            return x, iterations

def finite_volume(n, xrange, yrange, sources, sT, sA, points, tol):
    meshx,meshy, source, sA, D, dx, dy = generate_mesh(n, xrange, yrange, sources, sT, sA, points)

    A, source = generate_A(n, dx, dy, D, sA, source)
    N = n ** 2
    source = np.reshape(source, (N, 1))
    guess = source
    flux, iters = gauss_seidel(A, source, guess, tol)
    print("Number of Iterations:" + str(iters))
    return flux, iters, meshx, meshy


def generate_A(n, dx, dy, D, sA, S):
    # defining Matrix Coefficients
    left, right, top, bottom, center = np.zeros((n, n)), np.zeros((n, n)), np.zeros((n, n)), np.zeros((n, n)), np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            left[i][j] = -(D[i][j] * dy[j] + D[i][j + 1] * dy[j + 1]) / (2 * dx[i])
            right[i][j] = -(D[i][j] * dy[j] + D[i + 1][j + 1] * dy[j + 1]) / (2 * dx[i + 1])
            bottom[i][j] = -(D[i][j] * dx[i] + D[i + 1][j] * dx[i + 1]) / (2 * dy[j])
            top[i][j] = -(D[i][j + 1] * dx[i] + D[i + 1][j + 1] * dx[i + 1]) / (2 * dy[j + 1])
            center[i][j] = sA[i][j] - (left[i][j] + right[i][j] + bottom[i][j] + top[i][j])


    for j in range(1, n):
        right[0][j] = 0
        bottom[0][j] = 0
        top[0][j] = 0
        center[0][j] = 1
        S[j][0] = 0

        left[n - 1][j] = -(D[n - 2][j] * dy[j] + D[n - 2][j - 1] * dy[j - 1]) / (2 * dx[n - 2])
        bottom[n - 1][j] = -D[n - 2][j] * dx[j] / (2 * dy[j])  # Reflecting on Right
        top[n - 1][j] = -D[n - 2][j - 1] * dx[j] / (2 * dy[j + 1])
        center[n - 1][j] = sA[n - 1][j] - (left[n - 1][j] + bottom[n - 1][j] + top[n - 1][j])

    for j in range(n - 1):
        left[j][0] = 0
        right[j][0] = 0
        top[j][0] = 0
        center[j][0] = 1
        S[0][j] = 0

        right[j][n - 1] = -D[i][n - 1] * dy[n - 1] / (2 * dx[j])
        bottom[j][n - 1] = -(D[j][n - 1] * dx[j] + D[i + 1][n - 1] * dx[i + 1]) / (2 * dy[n - 1])
        left[j][n - 1] = -D[j + 1][n - 1] * dy[n - 1] / (2 * dx[j + 1])
        center[j][n - 1] = sA[j][n - 1] - (right[j][n - 1] + bottom[j][n - 1] + left[j][n - 1])



    Center = []
    Top = []
    Bottom = []
    for i in range(n):
        Center.append(np.zeros((n, n)))
        Top.append(np.zeros((n,n)))
        Bottom.append(np.zeros((n,n)))

    for j in range(n):
        for i in range(1, n - 1):
            Center[j][i][i] = center[i][j]
            Center[j][i][i + 1] = right[i][j]
            Center[j][i][i - 1] = left[i][j]

        Center[j][0][0] = center[0][j]
        Center[j][0][1] = right[0][j]
        Center[j][n - 1][n - 1] = center[n - 1][j]
        Center[j][n - 1][n - 2] = left[n - 1][j]

        for i in range(n):
            Top[i][j][j] = top[j][i]
            Bottom[i][j][j] = bottom[j][i]


    # Pulling Coefficients to (n**2Xn**2) to Matrix
    A = np.zeros((n ** 2, n ** 2))
    x0, x1, x2, b, t = [], [], [], [], []

    for i in range(n):
        diagonal = np.diag(Center[i])
        for j in range(n):
            x1.append(diagonal[j])

        diagonal0 = np.diag(Center[i], -1)
        diagonal1 = np.diag(Center[i], -1)

        if i > 0:
            diagonal0, diagonal1 = np.insert(diagonal0, 0, 0), np.insert(diagonal1, 0, 0)
        for j in range(len(diagonal0)):
            x0.append(diagonal0[j])
            x2.append(diagonal1[j])

        if i >= 1:
            diagonal = np.diag(Bottom[i])
            for j in range(len(diagonal)):
                b.append(diagonal[j])

        if i < n-1:
            diagonal = np.diag(Top[i])
            for j in range(len(diagonal)):
                t.append((diagonal[j]))

    for i in range(len(x1)):
        A[i][i] = x1[i]
    for i in range(len(x0)):
        A[i + 1][i] = x0[i]
        A[i][i + 1] = x2[i]
    for i in range(len(b)):
        A[i + n][i] = b[i]
    for i in range(len(t)):
        A[i][i + n] = t[i]

    return A, S
