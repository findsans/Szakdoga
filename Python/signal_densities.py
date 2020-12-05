from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import chart_studio.plotly as py
import plotly.graph_objects as go
import math
import random
import matplotlib as mpl

#setup
bin_num = 100
log_vals = False
sampling = 10
files = 120
startfile = 0
save = True    #save or show the densities
scatter = False  #show the 3D scatter or not
if files + startfile > 120:
    raise Exception("Can't check more than 120 files.")


x_vals = np.array([])
y_vals = np.array([])
z_vals = np.array([])

for i in range(files):
    fname = "C:\\Users\\Szászfai Vilmos\\Egyetem\\Szakdoga\\bad_signals_fast5_human_wgs_9.4\\divergences\\signal_{}_values.txt".format(i + startfile)
    x_vals_tmp = np.loadtxt(fname, delimiter="\t", usecols = 2)
    y_vals_tmp = np.loadtxt(fname, delimiter="\t", usecols = 3)
    z_vals_tmp = np.loadtxt(fname, delimiter="\t", usecols = 4)

    for j in range(np.size(x_vals_tmp)):
        if j % sampling == 0:
            x_vals = np.append(x_vals, x_vals_tmp[j])
            y_vals = np.append(y_vals, y_vals_tmp[j])
            z_vals = np.append(z_vals, z_vals_tmp[j])
print("sampling done")


clusters = np.zeros(np.size(x_vals), dtype=int)
center1 = -1
center0 = -1
avg1 = np.min(x_vals) + 0.1 * random.randint(1, 9)
avg0 = np.min(x_vals)
while abs(avg0 - center0) > 0.0001 or abs(avg1 - center1) > 0.0001:
    center1 = avg1
    center0 = avg0
    sum1 = 0
    sum0 = 0
    cnt1 = 0
    cnt0 = 0
    for i in range(np.size(x_vals)):
        if abs(x_vals[i] - center1) < abs(x_vals[i] - center0):
            sum1 += x_vals[i]
            cnt1 += 1
            clusters[i] = 1
        else:
            sum0 += x_vals[i]
            cnt0 += 1
            clusters[i] = 0
    avg1 = sum1 / cnt1
    avg0 = sum0 / cnt0
    print(abs(avg1 - center1), ", ", abs(avg0 - center0))

print(clusters)

#correlations
cors_xy = round(np.corrcoef(x_vals, y_vals)[0, 1], 3)
cors_xz = round(np.corrcoef(x_vals, z_vals)[0, 1], 3)
cors_yz = round(np.corrcoef(y_vals, z_vals)[0, 1], 3)
fig, axs = plt.subplots(3, 3)
fig.set_size_inches(16, 16)

axs[0, 1].text(0.5, 0.5, cors_xy, fontsize = 20, ha='center')
axs[0, 2].text(0.5, 0.5, cors_xz, fontsize = 20, ha='center')
axs[1, 2].text(0.5, 0.5, cors_yz, fontsize = 20, ha='center')

if log_vals == True:
    x_vals = np.log(np.maximum(np.nan_to_num(x_vals) + 1, 1))
    y_vals = np.log(np.maximum(np.nan_to_num(y_vals) + 1, 1))
    z_vals = np.log(np.maximum(np.nan_to_num(z_vals) + 1, 1))

#histograms
axs[0, 0].hist(x_vals, bins = bin_num)
axs[0, 0].title.set_text('KL divergence')
axs[1, 1].hist(y_vals, bins = bin_num)
axs[1, 1].title.set_text('Mean')
axs[2, 2].hist(z_vals, bins = bin_num)
axs[2, 2].title.set_text('Standard deviation')

#densities
axs[1, 0].hist2d(x_vals, y_vals, cmap = "plasma", bins = bin_num, norm=mpl.colors.LogNorm(), cmin=0)
axs[2, 0].hist2d(x_vals, z_vals, cmap = "plasma", bins = bin_num, norm=mpl.colors.LogNorm(), cmin=0)
axs[2, 1].hist2d(y_vals, z_vals, cmap = "plasma", bins = bin_num, norm=mpl.colors.LogNorm(), cmin=0)

if save == True:
    plt.savefig("C:\\Users\\Szászfai Vilmos\\Egyetem\\Szakdoga\\testplot", dpi = 600)
else:
    plt.show()

#3D plotting of values
if scatter == True:
    plt.clf()
    plt.close()
    fig = plt.figure(figsize=[8, 8])
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(x_vals, y_vals, z_vals, c=clusters, marker='o')

    ax.set_xlabel('KL divergence')
    ax.set_ylabel('Mean')
    ax.set_zlabel('Standard deviation')

    plt.show()