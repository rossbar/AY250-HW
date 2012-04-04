import sqlite3
import numpy as np
import racedb
import os
import datetime
from matplotlib.pyplot import *

# Get the market efficiency
def getInefficiency( cursor, refDate ):
  '''Given a cursor to a database and a reference date (the earliest date in the
     data contained in the database) plot the market efficiency vs. day for the
     presidential election race. Find dates where the market efficiency 
     deviates from 100% by more than a threshold value (default=8%). Print
     and return these dates. '''

  # Get the dates of interest
  cursor.execute('select day from predictions')
  days = np.unique( cursor.fetchall() )
  
  # Loop through the days and calculate the market efficiency for each.  
  mkteff = []
  for i in days.ravel():
    val = racedb.getEfficiencyOnDay( cursor, 'predictions', i, 'PresElect' )
    if val > -1:
      mkteff.append( (i, val) )
  
  # Plot the market efficiency
  mktary = np.array(mkteff)
  plot( mktary[:,0], mktary[:,1] )
  title('Market Efficiency vs. Time')
  xlabel('Days since 11/3/2008')
  ylabel('Market Efficiency (%)')
  show()
  
  # Find points where the market efficiency if furthest from normal (100%)
  d = mktary[:,0]
  e = mktary[:,1]
  thresh = 8 # Threshold = 8% deviation from perfect market
  lows = d[e < 100 - thresh].tolist()
  his = d[e > 100 + thresh]
  cuthis = racedb.clusterData(his, 3)
  cutlos = racedb.clusterData(lows, 3)
  ineffDays = cuthis.tolist() + cutlos.tolist()
  ineffDates = racedb.getDatesOfMarketInefficiency( ineffDays, refDate )
  print 'Here are some dates of market inefficiency:\n'
  np.sort(ineffDates)
  for date in ineffDates:
    print date
  return ineffDates
