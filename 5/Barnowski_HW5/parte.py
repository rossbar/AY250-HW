import sqlite3
import numpy as np
import scrapeWiki as sw
import racedb as rdb
import os
from matplotlib.pyplot import *
   
# ########### Mason Dixon Part
def predictMasonDixon( cursor ):
  '''Uses the Mason Dixon data saved in states.txt (see readme). Reads the 
     database to get data from the predictions and candidates table (joined)
     For each day in each race, loop through the candidates and determine
     whether their home state is above or below the MDLine. Then sum the 
     results and determine the probability by dividing by the total price that
     day. '''
  # Initialize. The mason-dixon determinations for each of the states (and DC) 
  # are contained in states.txt
  mddata = np.loadtxt('states.txt', usecols=(0,3), delimiter='\t', dtype=object)
  races = ['PresElect', 'RepNom', 'RepVPNom']

  # Do this for each of the three given races
  for race in races:
    # Get the info you need from the database
    cmd = '''select candidates.canid,candidates.state,predictions.raceid,\
    predictions.day,predictions.price from candidates join predictions on\
     predictions.canid = candidates.canid where raceid="%s"''' %race
    cursor.execute(cmd)
    db = np.array( cursor.fetchall() )
    days = np.unique( db[:,3].astype(int) )
    
    # Get the probabilities for each day in the given race
    probs = []
    for i in days:
      val = rdb.getMDProb( db, i, mddata )
      probs.append( (i, val) )
    
    # Plot the proability vs. the day for each race
    probary = np.array(probs)
    figure()
    plot( probary[:,0], probary[:,1] )
    title('Probability of Candidate from Above MD Line winning %s' %race)
    xlabel('Days since 11/3/2008')
    ylabel('Prob. of Race Winner being from Above MD Line')
    show()
