import numpy
import string
import random

def getNewName(gender):

  if gender == 'M':
    namesFile = 'MaleNames.txt'
  elif gender == 'F':
    namesFile = 'FemaleNames.txt'

  f = open(namesFile, 'r')
  names = f.readlines()
  f.close()

  name = random.choice(names)

  l = ['']*5
  for i in range(5):
    l[i] = random.choice(string.letters)
  suffix = ''.join(l)

  newName = name.strip() + '_' + suffix
  return newName

def determineSex(sampleBear):
  if numpy.random.rand() >= sampleBear.probMale:
    newSex = 'F'
  else:
    newSex = 'M'
  return newSex
