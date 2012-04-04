import sqlite3
import numpy as np
import os
import datetime

def createDB( location ):
  '''Create a sqlite3 database in the given location. Return the connection and
     the cursor that points to that database. '''
  connection  = sqlite3.connect( location )
  cursor = connection.cursor()
  return connection, cursor

def stripComma( fname ):
  '''Convert the format of the dates contained in the csv data so that it
     can be more easily read in and converted to database entries. WARNING:
     THIS FUNCTION OVERWRITES THE ORIGINAL FILE. '''
  ifile = open( fname, 'r' )
  lines = ifile.readlines()
  ifile.close()

  if 'stripped' not in lines[0]:
    newlines = ['stripped']
    for line in lines:
      lline = list(line)
      lline.remove(',')
      newlines.append( ''.join(lline) )
  
    ofile = open( fname, 'w' )
    ofile.writelines( newlines )
    ofile.close()
  return

def importDataFromFile( fname ):
  '''Get the stock data from the csv file.'''
  stripComma( fname )
  data = np.loadtxt( fname ,skiprows=1, delimiter=',', usecols=(0,4,5),\
         dtype=[('date','S13'), ('price','float'), ('volume','float')] )
  return data

def getRaceAndCanIds( fname ):
  '''For a given file in race_precition_data, get the candidate name and the
     race name from the file name. '''
  dl = fname.split('_')
  raceid = dl[-1].strip('.csv')
  canid = ' '.join( dl[0:-1] )
  return raceid, canid

def getEfficiencyOnDay( cursor, tblname, day, race ):
  '''Read the database for the given day and race and determine the market
     efficiency on that day. This is done by summing up the price for each
     candidate in that race on the given day. If there is no info for the
     given day, return -1'''
  # Read the database
  cmd = '''SELECT canid,price FROM %s WHERE day=%s AND raceid="%s"'''\
           %(tblname, day, race)
  cursor.execute(cmd)
  info = np.array( cursor.fetchall() )
  repPrices = []
  obamaPrice = 0
  if info != []:
    # For each datum in the loaded data, determine the price. Calculates the 
    # information for Obama separate from the other candidates - Not used in 
    # current version of code
    for datum in info:
      name = datum[0]
      price = float( datum[1] )
      if 'Obama' in name: obamaPrice = price
      else: repPrices.append( price )
    return obamaPrice + sum(repPrices)
  else: return -1

def getMDProb( data, day, md):
  '''For the data on a given, determine whehter or not each candidate is from
     above or below the MD line. The MD data is boolean and loaded from 
     states.txt (not in this function, passed in by md) '''
  onDay = data[data[:,3] == str(day)]
  # Determine the total price on that day to normalize against
  totalPrice = onDay[:,4].astype(float).sum()
  above = []
  # For each candidate in the given race on the given day, if they are from 
  # above the MDLine, append their price to the list 'above'.
  for datum in onDay:
    state = datum[1].strip()
    if state == 'null': continue
    truthVal = md[ md[:,0] == state,1 ][0]
    if truthVal == 'True': isAboveMDLine = True
    else: isAboveMDLine = False
    if isAboveMDLine: above.append( float(datum[4]) )
  # Sum the prices from candidates above the MDLine and normalize to the total
  # price on the given day
  return sum(above)/float(totalPrice)

def clusterData(ary, cut):
  '''Cluster data from the peak finding so that like values are averaged 
     together. "Like Values" are values within cut of each other. Returns
     the averages of the clustered values (i.e. an estimate of the peak location
     '''
  groups = []
  group = [ary[0]]
  i = 0
  while i < len(ary) - 1:
    if isNear( ary[i+1], group[-1], cut):
      group.append( ary[i+1] )
    else:
      groups.append( np.array(group).mean() )
      group = [ ary[i+1] ]
    i += 1
  groups.append( int(np.array(group).mean()) )
  return np.array( groups ).astype(int)

def isNear(val1, val2, cutoff):
  '''Determines whether val1 is within [val2 - cutoff, val2 + cutoff] '''
  if val1 >= val2 - cutoff and val1 <= val2 + cutoff:
    return True
  else:
    return False

def getDatesOfMarketInefficiency( dayList, refDate ):
  '''Convert days to dates for the market inefficiency calculation. '''
  dates = []
  for day in dayList:
    delta = datetime.timedelta(day)
    dates.append( refDate + delta )
  return dates
