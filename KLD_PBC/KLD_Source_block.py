#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2020 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy as np
from gnuradio import gr
import pmt
class data_generate(gr.sync_block):
    """
    docstring for block data_generate
    """
    
    dataInc = 0 # using in plot data
    datasetNum = 0 # not availiable
    pkts = 0 # count packets
    amp = []
    data_set = []
    kl_set = []
    boundaryTag = []
    previous_Tag = 0
    tagIndex = 0
    tagged = 0

    sample_size = 100

    def loadConfig(self) :
        path = r'./config.txt'
        try:
            configfile = open(path,'r+')
        except FileNotFoundError:
            configfile = open(path,'w+')
            configfile.write(str(self.sample_size))
        else:
            config = configfile.read()
            self.sample_size = int(config)
        configfile.close()

    def cross_entropy(self,x, y) :
        return sum(x * np.log2(x / y))
    def kl_Divergence(self,x, y) :
        return self.cross_entropy(x,y) - self.cross_entropy(x,x)
    def packetsDetect(self,dataset,threshold) :

        sample_size = self.sample_size

        x = np.real(dataset)
        y = np.imag(dataset)
        self.amp = np.sqrt(x**2 + y**2)
        # generate data bins for KLD input 
        sample_size = sample_size # number of IQ or AMP values per sample
        set_size = int(len(dataset)/sample_size) # number of samples per bin
        seq_a = np.zeros((set_size,sample_size),dtype=np.float32)
        for i in range (0,set_size):
            j = i +1
            temp = self.amp[i * sample_size: j * sample_size]
            seq_a[i,:] = np.array(temp)
    
        # generate vector of relative entropy (KLD) values 
        self.kl_set = np.zeros((set_size-1,1))
        for i in range (0,set_size-1):
            self.kl_set[i] = self.kl_Divergence(seq_a[i],seq_a[i + 1])

        # determine KLD threshold for packet boundary
        # - must be done by visual analysis of graph 

        # implement packet counter for KLD output
        kl_set = np.zeros((set_size - 1,1))
        for i in range (0,set_size - 1):
            kl_set[i] = self.kl_Divergence(seq_a[i],seq_a[i + 1])
            if kl_set[i] < threshold and (i - self.previous_Tag) > 100 :
                self.pkts += 1
                self.boundaryTag.append(i)
                # using an extral param to aviod from index out of range
                #  at the beginning of array (before index 0 is -1)
                self.previous_Tag = i
        return self.amp,self.pkts
        
    def __init__(self):
        gr.sync_block.__init__(self,
            name="data_generate",
            in_sig=None,
            out_sig=[np.float32])
        self.loadConfig()
        fdata_set = r"/home/lu/EE559_datasets/set_12.txt"
        self.data_set = np.fromfile(fdata_set,dtype=np.complex64).tolist()
        self.data_set = self.data_set[:1000000]
        self.amp,self.pkts = self.packetsDetect(self.data_set,0.5)
        print(self.pkts,self.boundaryTag)

    def work(self, input_items, output_items):

        out = output_items[0]

        # <+signal processing here+>
       # print(self.dataInc,len(self.amp))
        outputLength = len(out)
        #maxrange = min((self.dataInc + 1)*outputLength,len(self.kl_set))
        maxrange = min((self.dataInc + 1)*outputLength,len(self.amp))
        print((self.dataInc)*outputLength,self.tagIndex,self.tagged)
        for i in range(outputLength):
            out[i] = self.amp[(self.dataInc)*outputLength + i]
            #self.add_item_tag(0, self.nitems_written(0) + i, pmt.intern('key'), pmt.intern('value'))
            if self.boundaryTag[self.tagIndex] * self.sample_size == ((self.dataInc)*outputLength + i):
                key = pmt.intern("boundary" + str(self.tagIndex + 1))
                value = pmt.intern(str(self.nitems_written(0) + i))
                self.add_item_tag(0, self.nitems_written(0) + i, key, value)
                print('tagged',self.tagIndex,self.nitems_written(0) + i)
                self.tagIndex += 1


            '''
            out[i] = self.kl_set[i]
            if i in self.boundaryTag :
                key = pmt.intern("boundary" + str(self.boundaryTag.index(i) + 1))
                value = pmt.intern(str(i))
                self.add_item_tag(0, self.nitems_written(0) + i, key, value)
        if self.dataInc*outputLength > len(self.kl_set):
            return -1
            
         
        self.dataInc += 1
        print(((self.dataInc)*outputLength + i),self.tagIndex,self.tagged)
        if self.tagIndex == 1 :
            self.tagged =1
            return len(output_items[0])
        elif self.tagged == 1 :
            return -1
        '''
        self.dataInc += 1

        return len(output_items[0])

