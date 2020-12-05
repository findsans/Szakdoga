from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import chart_studio.plotly as py
import plotly.graph_objects as go
import math
import random
import matplotlib as mpl


file_num = 47

fname = "C:\\Users\\Szászfai Vilmos\\Egyetem\\Szakdoga\\bad_signals_fast5_human_wgs_9.4\\divergences\\signal_{}_values.txt".format(file_num)
kl_divs = np.loadtxt(fname, delimiter="\t", usecols = 2)
means = np.loadtxt(fname, delimiter="\t", usecols = 3)
stds = np.loadtxt(fname, delimiter="\t", usecols = 4)

signal_size = np.size(kl_divs)
clusters = np.zeros(signal_size, dtype=int)

#1st round - too high/low values
for i in range(signal_size):
    if means[i] < 200 or means[i] > 800:
        clusters[i] = 1
    else:
        if stds[i] < 40 or stds[i] > 90:
            clusters[i] = 1
        else:
            if kl_divs[i] > 0.5:
                clusters[i] = 1


signals = np.array(range(signal_size)) * 100
#plotting signals with clusters
#plt.figure(figsize=[10, 8])

#plt.subplot(311)
#plt.plot(signals, kl_divs)

#plt.subplot(312)
#plt.plot(signals, means)

#plt.subplot(313)
#plt.plot(signals, stds)

kl_divs = np.log(kl_divs)
#means = np.log(means)
#stds = np.log(stds)

#plotting 3D values
plt.clf()
plt.close()
fig = plt.figure(figsize=[8, 8])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(kl_divs, means, stds, c=clusters, marker='o')

ax.set_xlabel('KL divergence')
ax.set_ylabel('Mean')
ax.set_zlabel('Standard deviation')

plt.show()