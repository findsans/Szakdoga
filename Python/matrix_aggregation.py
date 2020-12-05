import numpy as np
import matplotlib.pyplot as plt
import math

def make_figure(name, arr):
    plt.figure(figsize=[8, 8])
    plt.suptitle(name)

    plt.subplot(211)
    plt.hist(arr, bins=64)

    plt.subplot(212)
    step = 64
    nsteps = 64
    imgarr = np.zeros((step,nsteps))
    for i in range(0,len(arr),step):
        y = arr[i:min(len(arr),i+step)]
        imgarr[0:len(y),i//step] = y
    imgarr = np.transpose(imgarr)
    signalimage = plt.imshow(imgarr,cmap='jet')
    plt.colorbar(signalimage)

    plt.savefig("C:\\Users\\Szászfai Vilmos\\Egyetem\\Szakdoga\\overlapsim_evaluation\\" + name + ".png", dpi=600)
    plt.clf()
    plt.close()

matrix = np.full([4096, 4096], -1, dtype=float)

fname = "C:\\Users\\Szászfai Vilmos\\Egyetem\\Szakdoga\\overlapsim_evaluation\\missrate_matrix.txt"
matrix = np.loadtxt(fname, delimiter="\t", dtype=float)

start_cnt_array = np.array([], float)
start_mn_array = np.array([], float)
start_std_array = np.array([], float)

f1 = open("C:\\Users\\Szászfai Vilmos\\Egyetem\\Szakdoga\\overlapsim_evaluation\\start_values.txt", "w")
for i in range(4096):
    m = matrix[:,i]
    mstart = np.array([], float)
    for j in range(4096):
        if m[j] > 0:
            mstart = np.append(mstart, m[j])
    cnt1 = len(mstart)
    mn1 = np.mean(mstart)
    std1 = np.std(mstart)
    f1.write(str(cnt1) + "\t" + str(mn1) + "\t" + str(std1) + "\n")
    start_cnt_array = np.append(start_cnt_array, cnt1)
    start_mn_array = np.append(start_mn_array, mn1)
    start_std_array = np.append(start_std_array, std1)

f1.close()
make_figure("Starting simulation counts", start_cnt_array)
make_figure("Starting simulation means", start_mn_array)
make_figure("Starting simulation standard deviations", start_std_array)
print("start kmers done.")


end_cnt_array = np.array([], float)
end_mn_array = np.array([], float)
end_std_array = np.array([], float)

f2 = open("C:\\Users\\Szászfai Vilmos\\Egyetem\\Szakdoga\\overlapsim_evaluation\\end_values.txt", "w")
for i in range(4096):
    m = matrix[i, :]
    mend = np.array([], float)
    for j in range(4096):
        if m[j] > 0:
            mend = np.append(mend, m[j])
    cnt2 = len(mend)
    mn2 = np.mean(mend)
    std2 = np.std(mend)
    f2.write(str(cnt2) + "\t" + str(mn2) + "\t" + str(std2) + "\n")
    end_cnt_array = np.append(end_cnt_array, cnt2)
    end_mn_array = np.append(end_mn_array, mn2)
    end_std_array = np.append(end_std_array, std2)

f2.close()
make_figure("Ending simulation counts", end_cnt_array)
make_figure("Ending simulation means", end_mn_array)
make_figure("Ending simulation standard deviations", end_std_array)
print("end kmers done.")