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
  # If no current residence, use birthplace
  if ri == -1:
    town, state = sw.getBirthplace( lines, bi , states )
  else:
    town, state = sw.getResidence( lines, ri, states )
  canInfo.append( (can.replace('_',' '), bday, town, state) )
  
