import matplotlib.pyplot as plt
import numpy as np


def surfacePlot(Flux, meshx, meshy, n, input):

    meshx, meshy = np.meshgrid(meshx, meshy)
    fig = plt.figure(figsize=(13, 13))
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(meshx, meshy,  np.reshape(Flux, (n, n)), rstride=1, cstride=1, cmap='coolwarm',
                           linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5, label="Flux[n/cm^2/s")
    ax.set_xlabel('X-Position: [cm]'), ax.set_ylabel('Y-Position: [cm]'), ax.set_zlabel('Flux: [n/cm^2/s')
    plt.title('Surface map of solutions to the flux', size=24)
    plt.savefig('..\\exports\\' + input + 'Surf.png')



def Side(Flux, xrange, yrange, input):

    fig = plt.figure(figsize=(16, 9))
    ax1, ax2 = plt.subplot(122), plt.subplot(121)
    ax1.plot(np.linspace(xrange[0], xrange[1], len(Flux)), Flux, 'b.', label="X-Z View"), ax2.plot(np.linspace(yrange[0], yrange[1], len(Flux)), Flux, 'r.', label="Y-Z View")
    ax1.legend(), ax2.legend()
    ax1.set_xlabel('X-Position: [cm]'), ax1.set_ylabel('Flux: [n/cm^2/s'), ax2.set_xlabel('Y-Position: [cm]'), ax2.set_ylabel('Flux: [n/cm^2/s')
    fig.suptitle("Side Views of Flux Solutions ", fontsize="large")
    plt.savefig('..\\exports\\' + input + 'Side.png')


def H_Map(Flux, meshx, meshy, n, input):
    meshx, meshy = np.meshgrid(meshx, meshy)
    fig = plt.figure(figsize=(16, 9))
    plt.pcolor(meshx, meshy, np.reshape(Flux, (n, n)), cmap='coolwarm', shading = 'auto')
    plt.xlabel('X-Position: [cm]'), plt.ylabel('Y-Position: [cm]')
    plt.title("Heat Map of Flux Solutions", fontsize="large"), plt.colorbar(label="Flux: [n/cm^2/s")
    plt.savefig('..\\exports\\' + input + 'HMap.png')