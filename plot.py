#!/usr/bin/env python3 
# -*- coding: utf-8 -*- 

""" 
Created on Sun Jun 28 20:30:43 2020 
Authors Deven Bowman, Julia Codere, Lincoln Doney
""" 
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.pyplot import cm
import re

def printf(format, *values):
    print(format % values )

class Experiment:
    def __init__(self, fileName, massNum, chrgNum, color, markerSize, markerSymbol, fillValue, computeBins):
        self.fileName = fileName
        self.massNum = massNum
        self.chargeNum = chrgNum 
        self.color = color
        self.markerSize = markerSize
        self.markerSymbol = markerSymbol
        self.fillValue = fillValue
        self.computeBins = computeBins
   

def flatten_list(_2d_list):
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list:
            # If the element is of type list, iterate through the sublist
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list

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

## Arrays that will hold info about each data set 

experiments=[] 

## Determines what power E is raised to 

POWER = 2.75 

##plotInput(name of the file, atomic mass number, charge number, color for plot, size of the marker, type of marker) 
## If the file containes energy data, enter None for MassNum and ChrgNum 
def plotInput(FileName, MassNum, ChrgNum, colr, mrkerSize, mrkerSymbol, fillValue, bins=True):
    ## adds information to each array 
    experiments.append(Experiment(
        FileName, MassNum, ChrgNum, colr, mrkerSize, mrkerSymbol, fillValue, bins
    ))

## data will plot in the order that plotInput is called 

element = "P"
if(element == "P"):
    plotInput('P_data/P_ACE-CRIS(1997-1998)_2013', None, None,'red', 4,'s', 'full') #point markers  
    plotInput('P_data/P_ALICE(1987)_1992', None, None,'black', 4,'D', 'full') #point markers  
    plotInput('P_data/P_ACE-CRIS(2001-2003)_2013', None, None,'blue', 4,'.', 'full') #point markers  
    plotInput('P_data/P_ACE-CRIS(2009-2010)_2013', None, None,'goldenrod', 4,'o', 'full') #point markers  
    plotInput('P_data/P_Balloon(1971-1972)_1974', None, None,'pink', 4,'v', 'full') #point markers  
    plotInput('P_data/P_Balloon(1968)_1979', None, None,'cadetblue', 4,'*', 'full') #point markers  
    plotInput('P_data/P_CRISIS(1977)_1981', None, None,'orange', 4,'^', 'full') #point markers  
    plotInput('P_data/P_HEAO3-C2(1979-1980)_1990', None, None,'green', 4,'P', 'full') #point markers  
#    plotInput('P_data/P_Voyager1-HET-Aend(2012-2015)_2016', None, None,'cadetblue', 4,'*', 'full') #point markers  
elif (element == "S"):
    plotInput('S_data/S_ACE-CRIS_2013', None, None,'red', 4,'s', 'full', bins=False) #point markers  
    plotInput('S_data/S_ALICE_1992', None, None,'black', 4,'.', 'full', bins=False) #point markers  
    plotInput('S_data/S_Balloon-EWAsym_1997', None, None,'blue', 4,'o', 'full', bins=False) #point markers  
    plotInput('S_data/S_Balloon-OpeningAngle_1997', None, None,'gray', 4,'v', 'full', bins=False) #point markers  
    plotInput('S_data/S_Balloon(1974)_1974', None, None,'pink', 4,'^', 'full', bins=False) #point markers  
    plotInput('S_data/S_Balloon(1978)_1978', None, None,'orange', 4,'1', 'full', bins=False) #point markers  

    # This one is messed up, ask Sasa
    plotInput('S_data/S_Balloon(1993)_1993', None, None,'green', 4,'d', 'full', bins=False) #point markers  

    plotInput('S_data/S_CRISIS_1981', None, None,'cadetblue', 4,'8', 'full', bins=False) #point markers  
    plotInput('S_data/S_HEAO3-C2_1990', None, None,'magenta', 4,'.', 'full', bins=False) #point markers  
    plotInput('S_data/S_TRACER03_2008', None, None,'brown', 4,'p', 'full', bins=False) #point markers  
    plotInput('S_data/S_Voyager1-HET-Aend_2016', None, None,'lightblue', 4,'P', 'full', bins=False) #point markers  
    plotInput('S_data/S_Voyager1-HET-Bend_2016', None, None,'lightgreen', 4,'*', 'full', bins=False) #point markers  
    plotInput('S_data/S_Voyager1-LET_2016', None, None,'goldenrod', 4,'D', 'full', bins=False) #point markers  
else:
    MATCHER = re.compile(r",(?=(?:[^\"']*[\"'][^\"']*[\"'])*[^\"']*$)")
    data = flatten_list([(MATCHER.split(line)) for line in open('e+_data/files')])
    data = map(lambda d: d.replace(".csv", "").replace("\n","").replace(" ", ""),data)
    data = list(filter(lambda d: d != '',data))
    if(len(data) > len(STYLES)):
        RAINBOW = iter(cm.rainbow(np.linspace(0, 1, len(data) - len(STYLES))))
    for i,f in enumerate(data):
        if(i < len(STYLES)):
            c = STYLES[i][0]
            marker = STYLES[i][1]
        else:
            c = next(RAINBOW)
            marker = "s" # we'll replace this later
        plotInput('e+_data/%s'%(f.replace(".csv", "").replace("\n","").replace(" ", "")), None, None, c, 4,marker, 'full', bins=False) #point markers  

''' 
### Plotting Loop ### 
-runs for each file, calculating flux and error bars 
-if rigidity data is entered, the energy conversion is calculated 
''' 

plt.figure(figsize=(10, 5), dpi=100)
i=0 
ignore = []

while i < len(experiments): 
    ### accesses the file specific info ### 
    experiment = experiments[i]
    fileName= experiment.fileName
    name = fileName.split('/')[-1].split('_')
    element =name[0] 
    paper =name[1] 
    year = name[2] 
    A = experiment.massNum 
    Z = experiment.chargeNum 
    fill = experiment.fillValue 

    data = np.genfromtxt(fileName + '.csv', delimiter=',', skip_header=1) ## Opens the csv file of the form 'He_AMS_2017.csv' and skips the header 

    # Fixes error with single row
    if(data.ndim != 2):
        data = data.reshape((1,data.shape[0]))

    ## Assumes that None input for mass number and charge means the data is in terms of energy 
    Is_Energy = ( A == None or Z == None ) 
    ## ENERGY CSV ## 

    lolims = False
    uplims = False
    if Is_Energy: 
        # y = input('Do you need to calculate the mean values of the energy bins for ' + fileName + ', Y or N: ') 
        y = "y"
        if experiment.computeBins == True:
            E1 = data[:,0:1].reshape(-1) ## COLUMN 0 
            E2 = data[:,1:2].reshape(-1) ## COLUMN 1 
            F = data[:,2:3].reshape(-1) ## COLUMN 2 
            error_pos = data[:,3:4].reshape(-1) ## column 3 
            error_neg = data[:,4:5].reshape(-1) ## column 4 
            E = 10**((np.log10(E1)+np.log10(E2))/2) #computes center of energy bin 
        else: 
            E = data[:,0:1].reshape(-1)
            F = data[:,1:2].reshape(-1)
            error_pos = data[:,2:3].reshape(-1)
            error_neg = data[:,3:4].reshape(-1)
        
        error_pos=(error_pos*E**POWER) #computes plotted error amounts 
        error_neg=(error_neg*E**POWER) 

        uplims = [True if (v - e < 0.0000000001) else False for e,v in zip(error_pos, F*E**POWER)] 
        error_pos = [abs(9.9*v/10) if v - e < 0.0000000001 else e for e,v in zip(error_pos, F*E**POWER)]
        
        E_err = np.array(list(zip(error_pos, error_neg))).T #creates a 2D array of error that can be plotted 
            
    ## RIGIDITY CSV ## 
    ## if a mass number and charge number were enterd, it treats the data as rigidity 
    else: 
            ## Calculation Information ## 
            ratio = 931.5 ##ratio of MeV/c^2 per 1 u 
            M = A*ratio/10**3 ##mass [GeV/c^2] 

            ## Rigidity ## 
            R1 = data[:,0:1] 
            R2 = data[:,1:2] 
            F_R = data[:,2:3] 
            sys_err = data[:,3:4] 
            stat_err = data[:,4:5] 
            R_err = np.sqrt(stat_err**2 + sys_err**2) ## AMS Paper Error Calculation Method 
            R = 10**((np.log10(R1)+np.log10(R2))/2) ##calculates center of rigidity bin(not used when plotting energy) 

             ## Energy ## 
            E1 = (np.sqrt(Z**2*R1**2+M**2)-M)/A # calculates energy from rigidity 
            E2 = (np.sqrt(Z**2*R2**2+M**2)-M)/A 
            E = 10**((np.log10(E1)+np.log10(E2))/2) ##calculates center of energy bin 
            ##Calculates energy flux F 
            dRdE = (R2-R1)/(E2-E1) 
            F = F_R*dRdE 
            E_err = ((R_err*dRdE)*E**POWER) ##calculates plotted Energy flux error 


    if(not (paper in ignore)):
        ## Plots data with file specific formatting ## 
        plt.plot(E, (F*E**POWER), experiment.markerSymbol, ms=experiment.markerSize, c=experiment.color, label = paper, fillstyle=fill) ##plots the data 
        plt.errorbar(E, (F*E**POWER), yerr=E_err, fmt=' ', ecolor=experiment.color, uplims=uplims) ##plots error bars 
        plt.errorbar(E, (F*E**POWER), yerr=E_err, fmt=' ', ecolor=experiment.color, lolims=lolims) ##plots error bars 

    i+=1 ##moves on to next file     

## Makes the plot log-log ##     
plt.xscale('log') 
plt.yscale('log')

## Sets axes limits ## 
#plt.ylim(10**(-3), 10**2)

## Adds Plots Labels/Title ## 
plt.title('Flux vs Energy: %s'%(element), fontweight='bold', fontsize=18) 
plt.xlabel('Energy/nucleon (GeV/n)', fontsize = 15) 

#Make sure the power in the label is correct 
plt.ylabel(r'Φ E$^{%s}$(m$^{-2}$s$^{-1}$sr$^{-1}$GeV/n$^{1.75}$)'%(POWER), fontsize =14) 

## Formats axis tick marks ## 
plt.tick_params(axis='both',which = 'both', direction = 'in', length= 3, width = 1.2 ) #adjust all axis ticks to point inward 
plt.tick_params(axis='both', direction = 'in', length = 5, labelsize=12 ) #further adjust size of only major tick marks 
 
plt.legend(bbox_to_anchor=(1.02, 1.1), loc='upper left', borderaxespad=0)
#plt.legend(loc=0) 
#plt.legend(bbox_to_anchor=(1.02, 1.1), loc='upper left', borderaxespad=0)
plt.savefig("%s_Plot.png"%(element),bbox_inches='tight')
plt.savefig("%s_Plot.jpg"%(element),bbox_inches='tight')
plt.show()
