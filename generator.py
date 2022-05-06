#!/usr/bin/env python3 
# -*- coding: utf-8 -*- 

""" 
Created on Sun Jun 28 20:30:43 2020 
Authors Deven Bowman, Julia Codere 
""" 

import numpy as np 
import matplotlib.pyplot as plt 
import re
from matplotlib.pyplot import cm
import itertools

def printf(format, *values):
    print(format % values )

STYLES = [
    ('red', '.'),
    ('black', 's'),
    ('blue', 'o'),
    ('orange', '+'),
    ('pink', 'h'),
    ('cadetblue', '*'),
    ('green', 'D'),
    ('gray', '1'),
    ('darkgray', 'v')
]

plt.rcParams["font.weight"] = "bold" #makes the font on the plots bold 
plt.rcParams["axes.labelweight"] = "bold" #makes the fonts on the plots bold 

## Determines what power E is raised to 

POWER = 2.75 

plt.figure(figsize=(19, 8), dpi=80)

plt.rcParams["figure.figsize"] = plt.rcParamsDefault["figure.figsize"]

## plotInput(name of the file, atomic mass number, charge number, color for plot, size of the marker, type of marker) 
## If the file containes energy data, enter None for MassNum and ChrgNum 
# def plotInput(FileName, MassNum, ChrgNum, colr, mrkerSize, mrkerSymbol, fillValue, bins=True):

element_table = {}
## data will plot in the order that plotInput is called 
# data = np.genfromtxt('Compileflux_New_Set_data.csv', delimiter=',', skip_header=2,usecols=np.arange(0,35)) ## Opens the csv file of the form 'He_AMS_2017.csv' and skips the header 
MATCHER = re.compile(r",(?=(?:[^\"']*[\"'][^\"']*[\"'])*[^\"']*$)")

data = [MATCHER.split(line) for line in open('Compileflux_New_Set_data.csv')][2:]

for row in data:
    element = row[3]
    if(element_table.get(element) == None):
        element_table[element] = []
    row = [None if v == -9999 else v for v in row]
    element_table[element].append(row)
    
''' 
### Plotting Loop ### 
-runs for each file, calculating flux and error bars 
-if rigidity data is entered, the energy conversion is calculated 
''' 

#plt.figure(dpi=5000) 
ignore = []
to_plot = element_table["e+"]
experiments = {}

for row in to_plot:
    name = row[2]
    element = row[3]
    year = row[4]
    paper = row[5]
    A = None
    Z = None

    ## Assumes that None input for mass number and charge means the data is in terms of energy 
    Is_Energy = ( A == None or Z == None ) 
    ## ENERGY CSV ## 

    if Is_Energy: 
        E1 = float(row[15])
        E2 = float(row[16])
        if False:
            E = 10**((np.log10(E1)+np.log10(E2))/2) #computes center of energy bin 
        else: 
            E = float(row[17])
            
        error_pos = float(row[18])
        error_neg = float(row[19])
        F = float(row[20])

        if(experiments.get(name) == None):
            experiments[name] = []
        experiments[name].append((E, F, error_pos, error_neg, element, name.replace('/', u"\u2215"), year))
        
            

    ## Plots data with file specific formatting ##
for k in experiments.keys():
    v = experiments[k]
    new_rc = []
    for datapoint in v:
        E = datapoint[0]
        F = datapoint[1]
        error_pos = datapoint[2]
        error_neg = datapoint[3]
        new_rc.append([E, F, error_pos, error_neg])
    
    experiments[k] = (np.array(new_rc),datapoint[4],datapoint[5],datapoint[6])

if(len(experiments.keys()) > len(STYLES)):
    RAINBOW = iter(cm.rainbow(np.linspace(0, 1, len(experiments.keys()) - len(STYLES))))

MARKER_ITER = itertools.cycle(('.', 's', 'o', '+', 'h', '*', 'D', '1', 'v'))

i = 0
for k in experiments.keys():
    if(k in ignore):
        continue
    
    r = experiments[k]
    d = r[0]
    E = d[:,0:1].reshape(-1)
    F = d[:,1:2].reshape(-1)
    error_pos = d[:,2:3].reshape(-1)
    error_neg = d[:,3:4].reshape(-1)
    np.savetxt('e+_data/%s_%s_%s.csv'%(r[1],r[2],r[3]), d, delimiter=",", header="E,F,err_pos,err_neg",comments='')
    if(i < len(STYLES)):
        color = STYLES[i][0]
        marker = STYLES[i][1]
    else:
        color = next(RAINBOW)
        marker = next(MARKER_ITER)

    error_pos=(error_pos*E**POWER) #computes plotted error amounts 
    error_neg=(error_neg*E**POWER) 
    E_err = np.array(list(zip(error_pos, error_neg))).T

    halving = []
    for g,err in enumerate(error_neg):
        if(err/(F[g]*E[g]**POWER) > 0.9):
            error_neg = error_neg/4

    # This is sort of jank, let's see how it goes
    for g,err in enumerate(error_pos):
        if(err/(F[g]*E[g]**POWER) > 0.9):
            printf("Warning: Err on %s busted! %f > %f", r[2], err, F[g]*E[g]**POWER)
            ignore.append(k)
            break

    # if(not(k in ignore)):
    plt.plot(E, (F*E**POWER), marker, ms=4, c=color, label=k) ##plots the data 
    plt.errorbar(E, (F*E**POWER), yerr=E_err, fmt=' ', ecolor=color) ##plots error bars 
    
    i = i + 1

## Makes the plot log-log ##     
plt.xscale('log') 
plt.yscale('log') 

## Sets axes limits ## 
## plt.ylim(10**3, 10**5)
## plt.xlim(10**.75, 10**7.21)

## Adds Plots Labels/Title ## 
plt.title('Flux vs Energy: %s'%(element), fontweight='bold', fontsize=18) 
plt.xlabel('Energy/nucleon (GeV/n)', fontsize = 15) 

#Make sure the power in the label is correct 
plt.ylabel(r'Φ E$^{%s}$(m$^{-2}$s$^{-1}$sr$^{-1}$GeV/n$^{1.75}$)'%(POWER), fontsize =14) 

## Formats axis tick marks ## 
plt.tick_params(axis='both',which = 'both', direction = 'in', length= 3, width = 1.2 ) #adjust all axis ticks to point inward 
plt.tick_params(axis='both', direction = 'in', length = 5, labelsize=12 ) #further adjust size of only major tick marks 
 
# plt.legend(loc="right", bbox_to_anchor=(2.0, 0.5), borderaxespad=0) 

plt.legend(bbox_to_anchor=(1.02, 1.1), loc='upper left', borderaxespad=0)
plt.savefig("e+_plot.png")
plt.savefig("e+_plot.jpg")
plt.show()
