from src import utils, diffusionSolver, plot



input = "input2"

n, xrange, yrange, sources, sT, sA, points, tolerance = utils.getInputs(input)
flux, iters, meshx, meshy = diffusionSolver.finite_volume(n, xrange, yrange, sources, sT, sA, points, tolerance)
plot.surfacePlot(flux, meshx, meshy, n, input)
plot.Side(flux, xrange, yrange, input)
plot.H_Map(flux, meshx, meshy, n, input)

with open("..\\exports\\" + input + "Fluxes.txt", "x") as file:
    for f in flux:
        print(f)
        file.write(" ".join(str(f)) + "\n")







