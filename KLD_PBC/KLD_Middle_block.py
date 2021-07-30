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

class data_generate_one(gr.basic_block):
    """
    docstring for block data_generate_one
    """

    dataInc = 0 # using in plot data
    datasetNum = 0 # not availiable
    pkts = 0 # count packets
    amp = []
    data_set = []
    kl_set = []
    boundaryTag = []
    previous_Tag = -101
    tagIndex = 0

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
    # threshold is given in 'work', sample_size is predefine in class
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
        kl_set = np.zeros((set_size-1,1))
        for i in range (0,set_size-1):
            kl_set[i] = self.kl_Divergence(seq_a[i],seq_a[i + 1])

        # determine KLD threshold for packet boundary
        # - must be done by visual analysis of graph 

        # implement packet counter for KLD output
        kl_set = np.zeros((set_size - 1,1))
        for i in range (0,set_size - 1):
            kl_set[i] = self.kl_Divergence(seq_a[i],seq_a[i + 1])
            
            # using an extral param to aviod too close kld in threshold

            if kl_set[i] < threshold and (i - self.previous_Tag) > 100 :
                print(kl_set[i])
                self.pkts += 1
                self.boundaryTag.append(i)
                self.previous_Tag = i

                self.tagIndex += 1
                key = pmt.intern("boundary" + str(self.tagIndex ))
                value = pmt.intern(str(self.nitems_written(0) + i))
                self.add_item_tag(0, self.nitems_written(0) + i * sample_size, key, value)
                print('tagged',self.tagIndex,self.nitems_written(0) + i)
        self.previous_Tag = -101
        
        return self.amp,self.pkts

    def __init__(self):
        gr.basic_block.__init__(self,
            name="data_generate_one",
            in_sig=[np.complex64],
            out_sig=[np.float32])
        #self.loadConfig()

    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items

    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        amp,pkts = self.packetsDetect(in0,0.5)
        for i in range(len(out)) :
            out[i] = amp[i]
        
        self.consume_each(len(input_items[0]))
        return len(output_items[0])
