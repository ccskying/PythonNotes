# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 16:00:15 2020

@author: lcc
"""

# libraries needed 
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats

# define KLD function (or use existing)
def cross_entropy(x, y):
    return scipy.stats.entropy(x,y)
#    return sum(x * np.log2(x / y))
def findsamplsize(amp,sample_size,threshold):
    # number of IQ or AMP values per sample
    set_size = int(len(subset)/sample_size) # number of samples per bin
    seq_a = np.zeros((set_size,sample_size),dtype=np.float32)
    for i in range (0,set_size):
        j = i +1
        temp = amp[i * sample_size: j * sample_size]
        seq_a[i,:] = np.array(temp)
    
    # generate vector of relative entropy (KLD) values 
    pkts = 0
    pkts2 = 0
    previous_bd = 0
    kl_set = np.zeros((set_size - 1,1))
    for i in range (0,set_size - 1):
        kl_set[i] = cross_entropy(seq_a[i],seq_a[i + 1]) - cross_entropy(seq_a[i],seq_a[i])
        if kl_set[i] < threshold and i - previous_bd > 100:
            pkts += 1
            previous_bd = i
        if kl_set[i] > 1.2 and i - previous_bd > 100:
            pkts2 += 1
            previous_bd = i
    plt.plot(kl_set)
    plt.title('KL Divirgence' + str(stepsize))
    plt.show()

    return pkts,pkts2
    

# import data set
#fdata_set = r"C:\\Users\\lcc\\Documents\\559PNdata\\EE559_datasets\\set_1.txt"
#fdata_set = r"C:\\Users\\lcc\\Documents\data\set2_4.txt"
fdata_set = r"C:\\Users\\lcc\\Documents\\MobaXterm\\slash\\home\\16qam_1500.txt"
data_set = np.fromfile(fdata_set,dtype=np.complex64)

# generate subset of data for heurstic analysis (1M samples) 
subset = data_set[0:1000000]
subset = data_set

#%%

# plot amplitude to find packet boundary
# - manually increase "inc" by 1 to scan all values 
# - may have to try "inc" in range (0,40)
x = np.real(subset)
y = np.imag(subset)
amp = np.sqrt(x**2 + y**2)
ran = list(range(0,len(amp))) # preserve x-axis indices
inc = 8               # index of plotted window
frame = 2000 # number of samples to plot per window 
plt.figure(0)
plt.plot(ran[inc*frame:(inc+1)*frame],amp[inc*frame:(inc+1)*frame])
plt.title('Capture sequence, amplitude')

#%%
pktsarray = np.zeros(30)
pktsarray2 = np.zeros(30)
for i in range(28):
    stepsize = (i + 1) *10
    threshold = 0.1
    pktsarray[i],pktsarray2[i] = findsamplsize(amp, stepsize, threshold)


#%%

# generate data bins for KLD input 
sample_size = 20 # number of IQ or AMP values per sample
set_size = int(len(subset)/sample_size) # number of samples per bin
seq_a = np.zeros((set_size,sample_size),dtype=np.float32)
for i in range (0,set_size):
    j = i +1
    temp = amp[i * sample_size: j * sample_size]
    seq_a[i,:] = np.array(temp)
    
# generate vector of relative entropy (KLD) values 
kl_set = np.zeros((set_size-1,1))
for i in range (0,set_size-1):
    kl_set[i] = cross_entropy(seq_a[i],seq_a[i + 1]) - cross_entropy(seq_a[i],seq_a[i])
    


# plot KLD and analyze graph 
plt.figure(1)
plt.plot(kl_set)
plt.title('KL Divirgence')

# determine KLD threshold for packet boundary
# - must be done by visual analysis of graph 

# implement packet counter for KLD output
pkts = 0
previous_bd = 0
kl_set = np.zeros((set_size - 1,1))
for i in range (0,set_size - 1):
    kl_set[i] = cross_entropy(seq_a[i],seq_a[i + 1]) - cross_entropy(seq_a[i],seq_a[i])
    if kl_set[i] <0.001 and i - previous_bd > 70:
        plt.scatter(i,kl_set[i])
        pkts += 1
        previous_bd = i
plt.show()
pktlength = len(amp) / pkts
# repeat process on full data set (16M samples) 
# - make sure you are confident in each step before this
