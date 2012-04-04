import numpy

class Bear(object):
  ''' This class definition differs from the other BearClass because it allows
      for the user to define the probability of P(male) rather than having
      it hard-coded. Developing a new class is not the right way to do this,
      but I don't quite fully understand how classes and 'self' work yet'''
  def __init__(self, pMale, name, sex, mother=None, father=None):
    ''' The name and sex are determined at time of birth, the age is 0. The '''
    self.name = name
    self.sex = sex
    self.age = 0
    self.mother = mother
    self.father = father
    self.probMale = pMale
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
