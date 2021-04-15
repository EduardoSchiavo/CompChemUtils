#!/usr/bin/env python
# coding: utf-8

# ## Crest Utilities
# 
# Module containing functions and utilities for crest analysis


import matplotlib.pyplot as plt
import pandas as pd


# ## crest to dataframe
# 
# takes the crest.out input and returns a pandas DataFrane object


def crest_to_dataframe(crest_out):


    with open(crest_out, 'r') as ifile:
        #initialize DataFrame
        conformers=pd.DataFrame(columns=['Energy','Weight','Number'])

        for line in ifile:
            if "total number unique points" in line:
                unique_points=int(line.split()[7]) # get total number of structures 
                rows=ifile.readlines()[1:unique_points]    #rows f the table

                for i,row in  enumerate(rows):  
                    if len(row.split())>6:     #isolate rows containing 'real conformers'
                        #read number, energy and weight
                        conf_num=int(row.split()[5])
                        conf_energy=float(row.split()[2])
                        conf_weight=float(row.split()[3])
                        #assign to DataFrame
                        conformers=conformers.append({'Energy':conf_energy, 'Weight':conf_weight, 'Number':conf_num}, ignore_index=True)

    return conformers





