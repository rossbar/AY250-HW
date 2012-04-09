import sqlite3
import numpy as np
import os
import datetime

dateDict = {'Jan':1, 'Feb':2, 'Mar':3}

def createDB( location ):
  connection  = sqlite3.connect( location )
  cursor = connection.cursor()
  return connection, cursor

def stripComma( fname ):
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
  stripComma( fname )
  data = np.loadtxt( fname ,skiprows=1, delimiter=',', usecols=(0,4,5),\
         dtype=[('date','S13'), ('price','float'), ('volume','float')] )
  return data

def getRaceAndCanIds( fname ):
  dl = fname.split('_')
  raceid = dl[-1].strip('.csv')
  canid = ' '.join( dl[0:-1] )
  return raceid, canid

def getPriceOnDay( cursor, day, race ):
  '''Returns the price of all candidates on a given day'''
  cmd = '''SELECT canid, price FROM %s WHERE day=%s AND raceid="%s"'''\
        %( 'predictions', day, race )
  cursor.execute(cmd)
  info = np.array( cursor.fetchall() )
  return info

def getPriceOnDayForCand( cursor, day, race, cand ):
  '''Returns the price of a specific candidate on a given day'''
  cmd = '''select price from %s where day=%s and raceid="%s" and canid="%s"'''\
        %( 'predictions', day, race, cand )
  cursor.execute(cmd)
  info = cursor.fetchall()
  if info != []:
    datum = float( info[0][0] )
  else: datum = -1
  return datum

def getEfficiencyOnDay( cursor, tblname, day, race ):
  cmd = '''SELECT canid,price FROM %s WHERE day=%s AND raceid="%s"'''\
           %(tblname, day, race)
  cursor.execute(cmd)
  info = np.array( cursor.fetchall() )
  repPrices = []
#  print info
  # default obama price
  obamaPrice = 0
  if info != []:
    for datum in info:
      name = datum[0]
      price = float( datum[1] )
      if 'Obama' in name: obamaPrice = price
      else: repPrices.append( price )
    return obamaPrice + sum(repPrices)
  else: return -1

def getMDProb( data, day, md):
  onDay = data[data[:,3] == str(day)]
  totalPrice = onDay[:,4].astype(float).sum()
  above = []
  for datum in onDay:
    state = datum[1].strip()
    if state == 'null': continue
    truthVal = md[ md[:,0] == state,1 ][0]
    if truthVal == 'True': isAboveMDLine = True
    else: isAboveMDLine = False
    if isAboveMDLine: above.append( float(datum[4]) )
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
  dates = []
  for day in dayList:
    delta = datetime.timedelta(day)
    dates.append( refDate + delta )
  return dates
