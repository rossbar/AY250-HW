# Import modules
import argparse
import datetime
import numpy as np
from matplotlib.pyplot import *

# Setup appropriate path for importing HW5 modules
import sys
sys.path.append('../5/')

# Import HW 5 modules
import createDatabase
import racedb as rdb

# Create parser
parser = argparse.ArgumentParser(description='Election Application')
parser.add_argument('-c', action='store', dest='candidate', default='Obama', \
                    help="Store the candidate's name")
parser.add_argument('-r', action='store', dest='raceName', default='PresElect',\
                    help="Store the race name. Options are 'RepNom, RepVPNom,\
                         'PresElect'")
parser.add_argument('-d', action='store', dest='date', default='09-10-2011',\
                    help='Enter the date\
                    you are interested in seeing information about. Must be\
                    in the format mm-dd-yyyy')
parser.add_argument('-p', action='store_true', default=False, dest='pltflg',\
                    help='Plots the price of the given candidate over time')
results = parser.parse_args()

# Check the input
posRaces = ['PresElect', 'RepNom', 'RepVPNom']
if results.raceName not in posRaces:
  print 'Incorrect race name!'
  sys.exit()

# Build the database
cursor, connection = createDatabase.createDatabase()

# Get the prices on the given day
date = results.date.split('-')
month = int(date[0])
day = int(date[1])
year = int(date[2])
refdate = datetime.date(2008, 11, 3)
stockdate = datetime.date(year, month, day)
day = (stockdate - refdate).days
pricesOnGivenDate = rdb.getPriceOnDay( cursor, day, results.raceName )

# If the candidate the user specified exists and the price for the candidate
# for the given races is known, print the result
canPrice = 'unk'
for item in pricesOnGivenDate:
  if results.candidate in item[0]:
    canName = item[0]
    canPrice = item[1]
if canPrice != 'unk':
  print 'The price for %s on %s was: %s' %(results.candidate, results.date, \
        canPrice)
else:
  print 'Candidate Not Found, please make sure you used the full candidate \
           name!'

# Plotting part.
if results.pltflg:
  cursor.execute('select day from predictions')
  days = np.unique( cursor.fetchall() )
  
  prices = []
  for i in days.ravel():
    val = rdb.getPriceOnDayForCand( cursor, i, results.raceName, canName )
    if val > -1: prices.append( (i, val) )

  # Plot the prices with the day of interest highlighted
  hold(True)
  priceAry = np.array(prices, dtype=object)
  plot( priceAry[:,0], priceAry[:,1] )
  title('Price for %s vs Time' %(results.candidate))
  xlabel('Days since 11/3/2008')
  ylabel('Price ($)')
  plot(day, canPrice, 'ro')
  show()
