# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   15/02/2021 -- 13/04/2022
# version:      0.9
# status:       prototype
# =============================================================================
"""
Description:
This module is used to evaluate the results.

DATA STRUCTURE:
    each list entry is one experiment
    one entry has the following comma separated values:
    0  number of agents
    1  timestep
    2  simulation time
    3  timesteps until no tokens are left in source
    4  timsteps until all tokens are in sink
    5  total number of collisions for all agents
    6  total number of broadcasts for all agents
    7  total number of received messages for all agents
    
"""

# =============================================================================
# Imports
# =============================================================================
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import os

# =============================================================================
# Class
# =============================================================================
class Evaluation():
    """
    This object is responsible for evaluation of measurement files.
    """
    def __init__(self):
        super(Evaluation, self).__init__()

    def evaluate(self, filePath, folderPath):
        """
        Evaluate experiment
        
        Args:
            filePath (string):   path to the measurement file
            folderPath (string): path to the measurement folderPath           
        """
        os.makedirs(os.path.dirname(folderPath), exist_ok=True)   

        # read measurement file and save data in an array 
        rawData = None
        numberOfColumns = 0
        with open (filePath, "r") as myfile:
            data = myfile.readlines()
            numberOfColumns = len(data[0].split(';'))
            rawData = np.zeros((len(data),numberOfColumns))
            for idx, x in enumerate(data):
                tmp = x.split(';')
                for idy, y in enumerate(tmp):
                    rawData[idx][idy] = float(y)

        # divide data into arrays according to the number of agents & calculate mean values for each column
        numberOfAgents = np.unique(rawData[:,0])                    # get unique values for number of agents
        meanData = np.zeros((numberOfAgents.size,numberOfColumns))  # save statistic results here
        stdData = np.zeros((numberOfAgents.size,numberOfColumns))   # save statistic results here
                
        for idx, nof in enumerate(numberOfAgents):
            ids = np.where(rawData[:,0] == nof)
            currData = rawData[ids,:]
            currData = currData[0]
            
            for x in range(numberOfColumns):
                meanData[idx,x] = np.mean(currData[:,x])
                stdData[idx,x] = np.std(currData[:,x])
        
        # prepare data for plots
        xTicks = numberOfAgents.astype(int)
        xIndices = np.arange(numberOfAgents.size)
        clr = [17/255, 117/255, 94/255, 0.5] # fraunhofer color
        fntsz = 20
        xLabel = 'Number of Agents'

        ######################################################################################
        # PLOT RESULTS
        plt.close('all')
        
        # Experiment - simulation time
        yMean = meanData[:,2]
        yStd = stdData[:,2]
        plt.figure(figsize=(16, 9))
        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()
        plt.bar(xIndices, yMean, align='center', color=clr)
        plt.errorbar(xIndices, yMean, yerr=yStd, fmt='o', color="black", elinewidth=1.5,capthick=1.5,errorevery=1, alpha=1, ms=0, capsize=5)
        plt.xticks(xIndices, xTicks, fontsize=fntsz)
        plt.yticks(fontsize=fntsz)
        plt.xlabel(xLabel, fontsize=fntsz)
        plt.ylabel('Simulation time [s]', fontsize=fntsz)
        plt.savefig(folderPath + 'Simulation time.png', format='png', dpi=300, transparent=True)
        
        # Experiment - collected all tokens from source
        yMean = meanData[:,3]*meanData[:,1] 
        yStd = stdData[:,3]*meanData[:,1]
        plt.figure(figsize=(16, 9))
        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()
        plt.bar(xIndices, yMean, align='center', color=clr)
        plt.errorbar(xIndices, yMean, yerr=yStd, fmt='o', color="black", elinewidth=1.5,capthick=1.5,errorevery=1, alpha=1, ms=0, capsize=5)
        plt.xticks(xIndices, xTicks, fontsize=fntsz)
        plt.yticks(fontsize=fntsz)
        plt.xlabel(xLabel, fontsize=fntsz)
        plt.ylabel('Natural time - All tokens collected [s]', fontsize=fntsz)
        plt.savefig(folderPath + 'Time consumption - All tokens collected from source.png', format='png', dpi=300, transparent=True)
        
        # Experiment - discardes all tokens in sink - time consumption
        yMean = meanData[:,4]*meanData[:,1]
        yStd = stdData[:,4]*meanData[:,1]
        plt.figure(figsize=(16, 9))
        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()
        plt.bar(xIndices, yMean, align='center', color=clr)
        plt.errorbar(xIndices, yMean, yerr=yStd, fmt='o', color="black", elinewidth=1.5,capthick=1.5,errorevery=1, alpha=1, ms=0, capsize=5)
        plt.xticks(xIndices, xTicks, fontsize=fntsz)
        plt.yticks(fontsize=fntsz)
        plt.xlabel(xLabel, fontsize=fntsz)
        plt.ylabel('Natural time - All tokens discarded [s]', fontsize=fntsz)
        plt.savefig(folderPath + 'Time consumption - All tokens discarded in sink.png', format='png', dpi=300, transparent=True)      
        
        # Experiment - average collisions per agents
        yMean = meanData[:,5]/meanData[:,0]
        yStd = stdData[:,5]/meanData[:,0]
        plt.figure(figsize=(16, 9))
        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()
        plt.bar(xIndices, yMean, align='center', color=clr)
        plt.errorbar(xIndices, yMean, yerr=yStd, fmt='o', color="black", elinewidth=1.5,capthick=1.5,errorevery=1, alpha=1, ms=0, capsize=5)
        plt.xticks(xIndices, xTicks, fontsize=fntsz)
        plt.yticks(fontsize=fntsz)
        plt.xlabel(xLabel, fontsize=fntsz)
        plt.ylabel('Average collisions', fontsize=fntsz)
        plt.savefig(folderPath + 'Average collisions.png', format='png', dpi=300, transparent=True)
        
        # Experiment - average broadcasts per agent
        yMean = meanData[:,6]/meanData[:,0]
        yStd = stdData[:,6]/meanData[:,0]
        plt.figure(figsize=(16, 9))
        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()
        plt.bar(xIndices, yMean, align='center', color=clr)
        plt.errorbar(xIndices, yMean, yerr=yStd, fmt='o', color="black", elinewidth=1.5,capthick=1.5,errorevery=1, alpha=1, ms=0, capsize=5)
        plt.xticks(xIndices, xTicks, fontsize=fntsz)
        plt.yticks(fontsize=fntsz)
        plt.xlabel(xLabel, fontsize=fntsz)
        plt.ylabel('Average broadcasts', fontsize=fntsz)
        plt.savefig(folderPath + 'Average broadcasts.png', format='png', dpi=300, transparent=True)
        
        
        # Experiment - average received messages per agent
        yMean = meanData[:,7]/meanData[:,0]
        yStd = stdData[:,7]/meanData[:,0]
        plt.figure(figsize=(16, 9))
        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()
        plt.bar(xIndices, yMean, align='center', color=clr)
        plt.errorbar(xIndices, yMean, yerr=yStd, fmt='o', color="black", elinewidth=1.5,capthick=1.5,errorevery=1, alpha=1, ms=0, capsize=5)
        plt.xticks(xIndices, xTicks, fontsize=fntsz)
        plt.yticks(fontsize=fntsz)
        plt.xlabel(xLabel, fontsize=fntsz)
        plt.ylabel('Average received messages', fontsize=fntsz)
        plt.savefig(folderPath + 'Average messages.png', format='png', dpi=300, transparent=True)
        
        
    