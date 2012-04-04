import sqlite3
import numpy as np
import racedb
import os
import datetime

#### Define date dictionary globally
dateDict = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7,\
            'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}

# Create the database in memory
connection, cursor = racedb.createDB(':memory:')

# Create the predition table
cmd = '''CREATE TABLE predictions (\
canid TEXT, raceid TEXT, day INT, price FLOAT, volume FLOAT)'''
cursor.execute(cmd)

# Create Candidate table
cmd = '''CREATE TABLE candidates (\
canid TEXT, birthday TEXT, town TEXT, state TEXT, party TEXT)'''
cursor.execute(cmd)

# Populate the prediction table
dirname = 'race_prediction_data/'
files = os.listdir( dirname )
# Earliest date in any of the files
refDate = datetime.date(2008, 11, 3)

for fname in files:
  if fname[0] != '.':
    data = racedb.importDataFromFile( dirname+fname )
    raceid, canid = racedb.getRaceAndCanIds( fname )
    for row in data:
      year = int( row['date'].split()[2].strip('"') )
      month = int( dateDict[ row['date'].split()[0].strip('"') ] )
      day = int( row['date'].split()[1] )
      stockDate = datetime.date(year, month, day)
      day = (stockDate - refDate).days
      d = (canid, raceid, day, row['price'], row['volume'])
      # sql command to insert row
      cursor.execute('INSERT INTO predictions VALUES (?,?,?,?,?)', d)
    connection.commit()

#Populate the candidate table
import scrapeWiki as sw
import racedb as rdb
import numpy as np
import os

# Load all the candidate files
dirname = 'race_prediction_data/'
files = os.listdir( dirname )

# Load state names for use in residence detection
states = np.loadtxt('states.txt', delimiter='\t', usecols=(0,), dtype=np.str )

# Get the candidate names
candidates = []
for fname in files:
  if fname[0] != '.':
    raceid, canid = rdb.getRaceAndCanIds( fname )
    candidates.append( canid.replace(' ','_') )
candidates = np.unique( candidates )
print candidates

# Loop through the candidate names on wikipedia and get as much info as you can
canInfo = []
for can in candidates:
  # Handle allen west's case
  if can == 'Allen_West': can = 'Allen_West_(politician)'
  elif can == 'John_Bolton': can = 'John_R._Bolton'
  elif can == 'Lindsay_Graham': can = 'Lindsey_Graham'
  lines = sw.getWikiInfo( can )
  # Get Birthday
  bi = sw.findKey(lines, 'Born')
  if bi == -1:
    bday = 'Unknown'
  else:
    bday = sw.getBirthday( lines, bi )
  # Get Residence
  ri = sw.findKey(lines, 'Residence')
  # If no current residence, use birthplace as residence
  if ri == -1:
    town, state = sw.getBirthplace( lines, bi , states )
  else:
    town, state = sw.getResidence( lines, ri, states )
  # Get party affiliation
  pid = sw.findKey(lines, 'Political party')
  if pid == -1: party = 'Unknown'
  else: party = sw.getParty( lines, pid )
  canInfo.append( (can.replace('_',' '), bday, town, state, party) )

#Populate candidate table
for row in canInfo:
  cursor.execute('INSERT INTO candidates VALUES (?,?,?,?,?)', row)
connection.commit()
