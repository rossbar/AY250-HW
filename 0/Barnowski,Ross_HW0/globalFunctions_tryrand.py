import numpy
import string
import random

def getNewName(gender):
  '''This function randomly generates a new (gender-appropriate) name. This
     version specifically generates a random 5 letter string and appends it 
     to the name to ensure randomness. Another version of the function 
     assigns names and then checks against the current names in the population
     to guarantee against overlap. This version is faster though, and the 
     probability of having the same suffix is 1/52^5.'''

  if gender == 'M':
    namesFile = 'MaleNames.txt'
  elif gender == 'F':
    namesFile = 'FemaleNames.txt'

  f = open(namesFile, 'r')
  names = f.readlines()
  f.close()

  # Choose a name from the correct gender-list of names
  name = random.choice(names)

  # Append a random 5-letter suffix to the name to ensure uniqueness
  l = ['']*5
  for i in range(5):
    l[i] = random.choice(string.letters)
  suffix = ''.join(l)

  newName = name.strip() + '_' + suffix
  return newName

def determineSex(sampleBear):
  '''Determine the sex of a new cub according to the probabilities of 
     producing a male/female - an attribute of the BearClass'''
  if numpy.random.rand() >= sampleBear.probMale:
    newSex = 'F'
  else:
    newSex = 'M'
  return newSex
