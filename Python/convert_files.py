import os

dirpath = "C:\\Users\\Szászfai Vilmos\\Egyetem\\Szakdoga\\bad_signals_fast5_human_wgs_9.4\\divergences"
files = os.listdir(dirpath)
i = 0

f = open("C:\\Users\\Szászfai Vilmos\\Egyetem\\Szakdoga\\bad_signals_fast5_human_wgs_9.4\\conversion.txt", "a")
for name in files:
    os.rename(dirpath+"\\"+name, dirpath+"\\signal_"+str(i)+".fast5")
    f.write("signal_" + str(i) + ".fast5\t" + name + "\n")
    i+=1
f.close()
print("Done")