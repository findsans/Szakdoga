import numpy as np
import matplotlib.pyplot as plt
import math

def number_to_kmer(n):
    tmp = -1
    kmer = ""
    for i in range(6):
        x = math.pow(4, 5-i)
        if n < x:
            tmp = 0
            kmer = kmer + "A"
        else:
            if (n < 2 * x):
                tmp = 1
                kmer = kmer + "C"
            else:
                if (n < 3 * x):
                    tmp = 2
                    kmer = kmer + "G"
                else:
                    tmp = 3
                    kmer = kmer + "T"
        n = n - tmp * x
    return kmer
    


matrix = np.full([4096, 4096], -1, dtype=float)

start_fname = "C:\\Users\\Szászfai Vilmos\\Egyetem\\Szakdoga\\overlapsim_evaluation\\start_values.txt"
end_fname = "C:\\Users\\Szászfai Vilmos\\Egyetem\\Szakdoga\\overlapsim_evaluation\\end_values.txt"
start_mn_array = np.loadtxt(start_fname, delimiter="\t", dtype=float, usecols=1)
end_mn_array = np.loadtxt(end_fname, delimiter="\t", dtype=float, usecols=1)

corrs = np.corrcoef(start_mn_array, end_mn_array)

print(corrs)

plt.scatter(start_mn_array, end_mn_array)
plt.title('Correlation between start and end kmers')
plt.xlabel('start kmers')
plt.ylabel('end kmers')
plt.plot(np.unique(start_mn_array), np.poly1d(np.polyfit(start_mn_array, end_mn_array, 1))(np.unique(start_mn_array)), color='yellow')
plt.show()


kmer_dict = {}
for i in range(len(start_mn_array)):
    kmer_dict[number_to_kmer(i)] = start_mn_array[i]
top_start = sorted(kmer_dict.items(), key=lambda x: x[1], reverse=True)[:40]

f1 = open("C:\\Users\\Szászfai Vilmos\\Egyetem\\Szakdoga\\overlapsim_evaluation\\worst_starting_kmers.txt", "w")
for i in top_start:
    a, b = i
    f1.write(a + "\t" + str(b) + "\n")
f1.close()

print("\n\n")
for i in range(len(end_mn_array)):
    kmer_dict[number_to_kmer(i)] = end_mn_array[i]
top_end = sorted(kmer_dict.items(), key=lambda x: x[1], reverse=True)[:40]

f2 = open("C:\\Users\\Szászfai Vilmos\\Egyetem\\Szakdoga\\overlapsim_evaluation\\worst_ending_kmers.txt", "w")
for i in top_end:
    a, b = i
    f2.write(a + "\t" + str(b) + "\n")
f2.close()