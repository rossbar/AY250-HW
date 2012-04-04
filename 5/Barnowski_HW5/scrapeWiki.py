import urllib2

def getWikiInfo( fname ):
  '''Open the wikipedia page associated with the fname. Won't work if fname
     is not in the appropriate wikipedia format (capitalized names, separated
     by underscores). Reads and returns the page source info. '''
  opener = urllib2.build_opener()
  opener.addheaders = [('User-agent', 'Mozilla/5.0')]
  print 'Accessing Wiki Page For: %s...' %fname
  infile = opener.open('http://en.wikipedia.org/w/index.php?title='\
                       +str(fname)+"&printable=yes")
  print 'Loading Page Source...'
  lines = infile.readlines()
  print 'Done'
  return lines

def findKey( html, keyword, first=True ):
  '''Searches through html source data and returns the index of the first
     line found to contain the keyword. Note: "first" keyword functionality
     depricated. '''
  occurences = []
  for ind, line in enumerate(html):
    if keyword in line:
      occurences.append( ind )
#  print 'Keyword found %s times.' %( len(occurences) )
  if first and len(occurences) != 0:
    return occurences[0]
  else:
    return -1

def getBirthday( html, bornInd ):
  '''Given the html source from a wikipedia page for a political candidate, 
     return their birthday. Works for nearly all of the candidates given in
     race_prediction_data despite formatting conflicts. '''
  if 'name' not in html[bornInd + 1]:
    line = html[bornInd + 1]
    start = line.find('>') + 1
  else:
    line = html[bornInd + 2]
    start = 0
  end = line[start:].find('<') + start
  linelist = list(line)
  return ''.join(linelist[start:end])

def getBirthplace( html, bornInd, statenames ):
  '''Same as getBirthday except returns the town and state in which the 
     candidate was born. '''
  if 'name' not in html[bornInd + 1]:
    line = html[bornInd + 2]
  else:
    line = html[bornInd + 3]
  start = line.find('title="') + 7
  end = line[start:].find('"') + start
  residence = line[start:end]

  state = 'null'
  for name in statenames:
    if name in line:
      state = name
      break
  return residence, state

def getResidence( html, resInd, statenames ):
  '''If the wikipedia page contains info on the current residence of the 
     candidate, extract the name of the residence (or town) and the state. '''
  line = html[resInd + 1]
  linelist = list(line)
  if line.find('title=') != -1:
    start = line.find('title="') + 7
  else:
    start = line.find('class="') + 7
  end = line[start:].find('"') + start
  residence = line[start:end]

  # If the source info doesnt conform to the format used for the above routine,
  # try a second routine.
  state = 'null'
  if ',' in residence:
    town = residence.split(',')[0]
    state = residence.split(',')[-1]
    return town, state
  else:
    for name in statenames:
      if name in line:
        state = name
        break
  # Default: Assume they're from dc
  if state == 'null': state = 'Washington D.C.'
  return residence, state

def getParty( html, pid ):
  '''Same as getBirthday except returns the political party of the candidate.'''
  line = html[ pid + 1 ]
  if 'Republican' in line: party='Republican'
  elif 'Democrat' in line: party='Democrat'
  else: party = 'Independent'
  return party
