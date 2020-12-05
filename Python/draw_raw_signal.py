import matplotlib.pyplot as plt
import os
import h5py
import numpy as np
import math

def plot_raw_signal(fname, raw_signal):
    print ('Making figure for ',fname)
    plt.clf()
    fig, axs = plt.subplots(2, 1)
    fig.set_size_inches(6, 10)
    axs[0].hist(raw_signal,bins= 100)
    #plt.hist(raw_signal,bins=100)
    raw_signal = np.clip(raw_signal,0,np.amax(raw_signal))


    #plt.figure(figsize = (10,8),dpi = 300)
    axs[1].set_title(fname)
    step = int(math.ceil(math.sqrt(len(raw_signal))))
    nsteps = len(raw_signal)//step + 1
    imgarr = np.zeros((step,nsteps))
    for i in range(0,len(raw_signal),step):
        y = raw_signal[i:min(len(raw_signal),i+step)]
        imgarr[0:len(y),i//step] = y
        #plt.plot(range(0,len(y)), y, linestyle = '-' , linewidth=0.2,color = (1.0-((i/step)/nsteps),(i/step)/nsteps,0))
    imgarr = np.transpose(imgarr)
    signalimage = axs[1].imshow(imgarr,cmap='jet')
    fig.colorbar(signalimage, ax = axs[1])
    fig.savefig(fname +'.png' ,dpi = 300)
    plt.close()


def get_signal_from_fast5(filename):
	fast5file = h5py.File(filename, 'r+')  # open in read and write!
	print("Loading", filename)
	raw_signal = None
	for key in fast5file['Raw/Reads'].keys():
		if 'Read_' in key:
			raw_signal = np.copy(fast5file['Raw/Reads'][key]['Signal'])
	fast5file.close()
	return raw_signal

if __name__ == "__main__":
	fname = 'good_signal_5.fast5'
	raw_signal = get_signal_from_fast5(fname)
	plot_raw_signal(fname,raw_signal)

