import numpy as np
import random
import sys

from nlmpy import nlmpy

np.random.seed(0) # So that the same NLMs are produced each time
nRow = 100 # Number of rows
nCol = 100 # Number of columns

# Randomly jitter the output rasters
random.seed(0)
raster_metadata = lambda cellSize: dict(
        xll=1743159.15 + 10*random.uniform(-1,1),
        yll=5469287.46 + 10*random.uniform(-1,1),
        cellSize=cellSize
    )

layers = 500

# Discrete
for layer in range(0,layers):
    # Midpoint displacement NLM
    nlm = nlmpy.mpd(nRow, nCol, 0.75)
    # Classified midpoint displacement NLM
    nlm = nlmpy.classifyArray(nlm, np.random.random_integers(1,10,(1,10))).astype(int)
    nlmpy.exportASCIIGrid(f'/home/lawr/dggs-benchmarks/discrete/raster-{layer}.asc', nlm, **raster_metadata(10))

# Continuous
for layer in range(0,layers):
    # Midpoint displacement NLM
    nlm = nlmpy.mpd(nRow, nCol, 0.75)
    nlmpy.exportASCIIGrid(f'/home/lawr/dggs-benchmarks/continuous/raster-{layer}.asc', nlm, **raster_metadata(10))

sys.exit(0)
