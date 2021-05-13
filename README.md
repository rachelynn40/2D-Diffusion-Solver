# 2D-Diffusion-Solver

Instructions for use:
1. Download all files on GitHub repo
2. Use sample input files OR create your own based exactly on the sample input files
    -- spacing must be exact or the file will not be read in correctly
3. Navigate to main.py & state the name of the input file you want solved
4. Run main.py in command prompt, terminal, or IDE
5. View outputs in output directory

Note: Program can only be ran ONCE before either moving, deleting, or renaming the output txt file.

Generic Input File:
Mesh_Size: __
Sources: ____, ____
X_lower: -1
X_upper: 1
Y_lower: -1
Y_upper: 1
Location_mesh: __, __, __, __
Sigma_transport: 0.__
Sigma_absorption: 0.__
Tolerance: 1e-7
Uniform: False/True
