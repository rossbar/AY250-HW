Readme file for HW0 project - simulating a bear population.

Included files:
BearClass.py
BearPopulationClass_tryNotN2.py
simulateBearPopulation.py
calculateAverage.py
findMaleMin.py
getBabyNames.py
globalFunctions_tryrand.py

### The following 3 files are tweaked versions of the above files and are used
### in the findMaleMin.py script. See __doc__findMaleMin for details
BearClass_varProb.py
BearPopulationClass_varProb.py
simulateBearPopulation_varProb.py

NOTE: Programs should be run with 'run' cmd in ipython. The scripts were not 
written to be run from command line (i.e. no #! /usr/env/python) - this is 
to avoid any complications from not having the modules that are automatically
included when running ipython with the --pylab flag

1) open ipython
2) run getBabyNames.py - Goes to the internet and retrieves some names. Must
	have a working internet connection or urllib.urlopen will fail (no
	catch).
3) To simply run the simulation:
	In[1]: from simulateBearPopulation import simulateBears
	In[2]: simulateBears(<# of years you wish the simulation to run for>)
   - Note: I only briefly attempted the networkx stuff, so it may not be
     implemented 100% correctly as stated in the prompt. The simulation is 
     set to only print the genealogy if the nubmer of bears is less than 1500
     to prevent creating a very cluttered graph
4) To estimate the minimum P(male) required to create a population that 
   survives until 150 years:
	In[1]: run findMaleMin.py
   - Note: This algorithm is stochastic. Increasing the number of iterations
           in the file will increase the accuracy of the answer
5) To determine the average number of bears after 150 years and the average
   number born in the first 100:
	In[1]: run calculateAverage.py
   - Note: The default number of runs to average over is 10 and can be changed
           in the script
	   It takes ~10-30s (depending on the computer)to run a single
	   population simulation to 150 years (if it doesn't die out) so keep
	   that in mind when changing the number of averaging cycles
	   The algorithm is very sensitive to small changes in the number of
	   years. For instance, the current algorithm starts at year 1 and 
           goes til year 150 (range(1,151)). Slight alterations in these 
           numbers (changing 151 -> 150 for instance) may influence the number
           of "mating cycles" that are undergone in the simulation, which can
           greatly influence the outcome.
