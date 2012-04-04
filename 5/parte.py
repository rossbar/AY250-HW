import sqlite3
import numpy as np
import scrapeWiki as sw
import racedb as rdb
import os
from matplotlib.pyplot import *
   
# ########### Mason Dixon Part
def predictMasonDixon( cursor ):
  mddata = np.loadtxt('states.txt', usecols=(0,3), delimiter='\t', dtype=object)
  races = ['PresElect', 'RepNom', 'RepVPNom']
  for race in races:
    cmd = '''select candidates.canid,candidates.state,predictions.raceid,\
    predictions.day,predictions.price from candidates join predictions on\
     predictions.canid = candidates.canid where raceid="%s"''' %race
    
    cursor.execute(cmd)
    db = np.array( cursor.fetchall() )
    days = np.unique( db[:,3].astype(int) )
    
    probs = []
    for i in days:
      val = rdb.getMDProb( db, i, mddata )
      probs.append( (i, val) )
    
    probary = np.array(probs)
    figure()
    plot( probary[:,0], probary[:,1] )
    title('Probability of Candidate from Above MD Line winning %s' %race)
    xlabel('Days since 11/3/2008')
    ylabel('Prob. of Race Winner being from Above MD Line')
    show()
