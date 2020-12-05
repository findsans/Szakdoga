import numpy as np
import matplotlib.pyplot as plt
import math
            
matrix = np.full([4096, 4096], -1, dtype=float)

fname = "C:\\Users\\Szászfai Vilmos\\Egyetem\\Szakdoga\\overlapsim_evaluation\\missrate_matrix.txt"
matrix = np.loadtxt(fname, delimiter="\t", dtype=float)

plt.figure(figsize=[10, 10])
plt.imshow(matrix, cmap = "hot", vmax=0.5)
plt.show()