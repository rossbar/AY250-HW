import numpy

class Bear(object):
  ''' A class for a bear - this includes all attributes that are common to all bears such as the probability of having male offspring'''
  def __init__(self, name, sex, mother=None, father=None):
    ''' The name and sex are determined at time of birth, the age is 0. The '''
    self.name = name
    self.sex = sex
    self.age = 0
    self.mother = mother
    self.father = father
    self.probMale = 0.5
    self.probFemale = 1 - self.probMale
    self.avgLifespan = 35.0 # years
    self.stdLifespan = 5 # years
    # Determine the time of death (i.e. play god)
    self.TOD = numpy.random.normal(self.avgLifespan, self.stdLifespan)
    self.LastProcreation = None
    self.canBreed = False
  
  def __str__(self):
    outStr = "Name: %s\t Sex: %s\t Age: %s\t" %(self.name, self.sex, self.age)
    return outStr

#  def checkIfCanBreed(self)
#    if self.age >= 5 and 
