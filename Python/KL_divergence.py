import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import h5py
import math
import warnings
import gc

def kl_div(p, q):
	return np.sum(np.where(p != 0, p * np.log(p / q), 0))

def normalize(array):
	return (array - array.mean(axis=0)) / array.std(axis=0)

def get_signal_from_fast5(filename):
	fast5file = h5py.File(filename, 'r+')  # open in read and write!
	#print("Loading", filename)
	raw_signal = None
	for key in fast5file['Raw/Reads'].keys():
		if 'Read_' in key:
			raw_signal = np.copy(fast5file['Raw/Reads'][key]['Signal'])
	fast5file.close()
	return raw_signal

warnings.filterwarnings("ignore")

ideal_dist = pd.DataFrame(pd.read_excel("C:\\Users\\Szászfai Vilmos\\Egyetem\\Szakdoga\\official6merModel.xlsx"))
ideal_means = np.array(ideal_dist["mean"])
ideal_stds = np.array(ideal_dist["std"])

window = 1000
bin_num = int(math.sqrt(window))

minval = np.min(ideal_means)
maxval = np.max(ideal_means)
bins = np.linspace(minval, maxval, bin_num + 1)
discretized = np.digitize(ideal_means, bins=bins)
q = np.zeros(len(bins))
for i in range(len(bins)):
	n = 0
	for j in discretized:
		if j == i+1:
			n += 1
	q[i] = n / len(discretized)


for n in range(121):
	print("Working on file number {}\n".format(n))
	name = "signal_{}".format(n)
	fname = "C:\\Users\\Szászfai Vilmos\\Egyetem\\Szakdoga\\bad_signals_fast5_human_wgs_9.4\\divergences\\{}.fast5".format(name)
	f = open("C:\\Users\\Szászfai Vilmos\\Egyetem\\Szakdoga\\bad_signals_fast5_human_wgs_9.4\\divergences\\signal_{}_values.txt".format(n), "w")
	raw_signal = get_signal_from_fast5(fname)

	KL_list = np.zeros(int((len(raw_signal) - window) / 100) + 1)
	signal_means = np.zeros(int((len(raw_signal) - window) / 100) + 1)
	signal_stds = np.zeros(int((len(raw_signal) - window) / 100) + 1)
	signal_list = np.arange(0, len(raw_signal)-window + 1, 100)

	for x in range(int((len(raw_signal) - window) / 100) + 1):
		signal_shard = normalize(raw_signal[x*100 : (x*100)+window])

		minval = np.min(signal_shard)
		maxval = np.max(signal_shard)
		bins = np.linspace(minval, maxval, bin_num + 1)
		discretized = np.digitize(signal_shard, bins=bins)
		p = np.zeros(len(bins))
		for i in range(len(bins)):
			n = 0
			for j in discretized:
				if j == i+1:
					n += 1
			p[i] = n / len(discretized)

		div = kl_div(p, q)
		m = np.mean(raw_signal[x*100 : (x*100)+window])
		s = np.std(raw_signal[x*100 : (x*100)+window])
		f.write("{}\t{}\t{}\t{}\t{}\n".format(x*100, (x*100)+window, div, m, s))
		KL_list[x] = div
		signal_means[x] = m
		signal_stds[x] = s

	f.close()
	#Drawing figures

	plt.figure(figsize=[14, 12])
	G = gridspec.GridSpec(12, 10)
	plt.suptitle(name)

	plt.subplot(G[0:3, :5])
	plt.title("KL divergences (window size: {})".format(window))
	plt.ylabel("KL divergence")
	plt.xlabel("starting k-mer")
	plt.plot(signal_list, KL_list, '.-')
	x1,x2,y1,y2 = plt.axis()
	plt.axis((0,x2,0,y2))

	plt.subplot(G[4:7, :5])
	plt.title("Raw signal means (window size: {})".format(window))
	plt.ylabel("mean")
	plt.xlabel("starting k-mer")
	plt.plot(signal_list, signal_means, '.-')
	x1,x2,y1,y2 = plt.axis()
	plt.axis((0,x2,y1,y2))

	plt.subplot(G[8:11, :5])
	plt.title("Raw signal stds (window size: {})".format(window))
	plt.ylabel("standard deviation")
	plt.xlabel("starting k-mer")
	plt.plot(signal_list, signal_stds, '.-')
	x1,x2,y1,y2 = plt.axis()
	plt.axis((0,x2,y1,y2))

	plt.subplot(G[:5, 6:])
	plt.title("Histogram of the raw signal")
	plt.hist(raw_signal,bins= 100)

	plt.subplot(G[6:, 6:])
	plt.title("Raw signal")
	step = int(math.ceil(math.sqrt(len(raw_signal))))
	nsteps = len(raw_signal)//step + 1
	imgarr = np.zeros((step,nsteps))
	for i in range(0,len(raw_signal),step):
	    y = raw_signal[i:min(len(raw_signal),i+step)]
	    imgarr[0:len(y),i//step] = y
	imgarr = np.transpose(imgarr)
	signalimage = plt.imshow(imgarr,cmap='jet')
	plt.colorbar(signalimage)

	#plt.tight_layout()
	#plt.show()
	plt.savefig("C:\\Users\\Szászfai Vilmos\\Egyetem\\Szakdoga\\bad_signals_fast5_human_wgs_9.4\\divergences\\" + name + "_divergence.png", dpi=600)
	plt.clf()
	plt.close()
	gc.collect()