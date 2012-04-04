import urllib2

def getWikiInfo( fname ):
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
  line = html[resInd + 1]
  linelist = list(line)
  if line.find('title=') != -1:
    start = line.find('title="') + 7
  else:
    start = line.find('class="') + 7
  end = line[start:].find('"') + start
  residence = line[start:end]

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
  line = html[ pid + 1 ]
  if 'Republican' in line: party='Republican'
  elif 'Democrat' in line: party='Democrat'
  else: party = 'Independent'
  return party
