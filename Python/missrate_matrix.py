import numpy as np
import matplotlib.pyplot as plt
import math

def kmerpos(kmer):
    n = 0
    for i in range(6):
        if kmer[i] == 'A':
            n += 0 
        if kmer[i] == 'C':
            n += math.pow(4, 5-i)
        if kmer[i] == 'G':
            n += math.pow(4, 5-i) * 2
        if kmer[i] == 'T':
            n += math.pow(4, 5-i) * 3
    return int(n)
            
matrix = np.full([4096, 4096], -1, dtype=float)

for i in range(24):
    if i < 10:
        logp_filename = "C:\\Users\\Szászfai Vilmos\\Egyetem\\Szakdoga\\overlapsim_may15\\log_p_0{}.txt".format(i)
        startend_filename = "C:\\Users\\Szászfai Vilmos\\Egyetem\\Szakdoga\\overlapsim_may15\\started_0{}.txt".format(i)
    else:
        logp_filename = "C:\\Users\\Szászfai Vilmos\\Egyetem\\Szakdoga\\overlapsim_may15\\log_p_{}.txt".format(i)
        startend_filename = "C:\\Users\\Szászfai Vilmos\\Egyetem\\Szakdoga\\overlapsim_may15\\started_{}.txt".format(i)
    print("file ", i, " (may15)")
    missrates = np.loadtxt(logp_filename, delimiter="\t", usecols=np.arange(0, 2))
    kmers = np.loadtxt(startend_filename, delimiter="\t", dtype=str, max_rows=missrates.shape[0])

    for i in range(missrates.shape[0]):
        startkmer = list(kmers[i][0])
        endkmer = list(kmers[i][1])
        missrate = math.exp(missrates[i, 1] - missrates[i, 0]) / 2.0

        startpos = kmerpos(startkmer)
        endpos = kmerpos(endkmer)

        matrix[startpos][endpos] = missrate

f = open("C:\\Users\\Szászfai Vilmos\\Egyetem\\Szakdoga\\overlapsim_evaluation\\missrate_matrix.txt", "w")
for i in range(4096):
    for j in range(4096):
        if(j < 4095):
            f.write(str(matrix[i][j]) + "\t")
        else:
            f.write(str(matrix[i][j]) + "\n")
f.close()
print("matrix saved")