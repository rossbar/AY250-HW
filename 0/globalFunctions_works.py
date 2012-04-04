from numpy import random

def getNewName(currentNameList, gender, approxNumBears):
  if gender == 'M':
    namesFile = 'MaleNames.txt'
  elif gender == 'F':
    namesFile = 'FemaleNames.txt'

  f = open(namesFile, 'r')
  names = f.readlines()
  f.close()

  # An attempt to speed up the name searching. As the number of bears grows, 
  # this little section of code is intended to increase the likelihood of
  # a cub being assigned a new name so that there are no nested loops in the
  # unique name lookup section
  i = 0
  titles = ['', 'Jr', 'Sr', 'I', 'II', 'III']#, 'IV', 'V', 'VI', 'VII', 'VIII' \
#            'IX', 'X']
  while approxNumBears/2 > 200:
    approxNumBears -= 200
    i += 1
  if i >= len(titles):
    i = i % len(titles)

  for name in names:
    name = name.strip() + titles[i]
    if name not in currentNameList:
      newName = name
  return newName

def determineSex(sampleBear):
  if random.rand() >= sampleBear.probMale:
    newSex = 'F'
  else:
    newSex = 'M'
  return newSex
