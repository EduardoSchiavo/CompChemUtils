#!/usr/bin/env python
# coding: utf-8

# ## HFLD Map from ORCA output 
# 
# Eduardo Schiavo v. 1.1
#
#call as hfld_heatmap.py orca_output.out

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import seaborn as sns

ifile=sys.argv[-1]

with open(ifile, "r") as f:
    input_list = f.read().splitlines()

l = [x for x in input_list if 'Dispersion' in x]


def parse_list(inpList):
    outList=[]
    for line in inpList[1:]:  #skip line 0
        outList.append(line.split()[1:]) #split and drop 'Dispersion'
    return outList


# [['2,1', '-0.003523775'],
#  ['3,1', '-0.001001638'],
#  ['3,2', '-0.003803736'],
#  ['4,1', '-0.003817664'],
#  ['4,2', '-0.001196230'],
#  ['4,3', '0.000000000'],
#  ['5,1', '-0.003755028'],
#  . . . ]

def get_max_num(inpList):
    return max([max(num) for num in inpList])

def create_heatmap(inpList):
    #parse list from orca
    parsedList=parse_list(inpList)
    #parse coordinates
    coord=[]
    vals=[]
    for line in parsedList:
        coord.append(tuple(map(int, line[0].split(','))))
        vals.append(float(line[1]))
    # get size for array
    arrSize=get_max_num(coord)

    #initialize empty matrix
    corrMatrix=np.zeros((arrSize+1,arrSize+1))

    #fill in values
    for i, j in zip(coord, vals):
        corrMatrix[i]=j

    corrMatrix

    f, ax = plt.subplots(figsize=(15, 15))
    ax = sns.heatmap(corrMatrix,cmap="OrRd")
    
    return f

fig=create_heatmap(l)

fig.savefig('heatmap.png', dpi=600)
