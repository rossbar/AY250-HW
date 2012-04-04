from numpy import random

def getNewName(gender, mNum, fNum):

  # These are the number of names stored in the .txt files
  totalMaleNames = 238
  totalFemaleNames = 283

  if gender == 'M':
    namesFile = 'MaleNames.txt'
    ind = mNum
    numNames = totalMaleNames
  elif gender == 'F':
    namesFile = 'FemaleNames.txt'
    ind = fNum
    numNames = totalFemaleNames

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
  while ind >= numNames:
    ind -= numNames
    i += 1

  newName = names[ind].strip() + titles[i]
  return newName

def determineSex(sampleBear):
  if random.rand() >= sampleBear.probMale:
    newSex = 'F'
  else:
    newSex = 'M'
  return newSex
