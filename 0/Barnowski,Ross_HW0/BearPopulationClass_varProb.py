from BearClass_varProb import Bear
from globalFunctions_tryrand import *

# Some important variables
waitPeriod = 5 # number of years between procreations
ofAge = 5      # age at which bears start doin it
ageDiff = 10   # Max age difference allowed between mating bears

class BearPopulation(object):
  '''Same as BearPopulationClass but tweaked to be able to handle a variable
     P(male). For full documentation, see BearPopulationClass_tryNotN2.py'''

  def __init__(self, bearList):
    self.allBears = bearList

  def ageBears(self):
    for bear in self.allBears:
      bear.age += 1 

  def checkForDead(self, year):
    for bear in self.allBears: 
      if bear.age >= bear.TOD:
        self.allBears.remove(bear)

  def checkIfCanBang(self, year):
    self.canProcreate = []
    for bear in self.allBears:
      if bear.age >= ofAge and ( bear.LastProcreation == None or \
                             year - bear.LastProcreation >= waitPeriod ):
        bear.canBreed = True
        self.canProcreate.append(bear)

  def createCub(self, pMale, mother, father):
    sex = determineSex(father)
    name = getNewName(sex)
    cub = Bear(pMale, name, sex, mother, father)
    return cub
 
  def generateOffspring(self, year, pMale):
    
    numBorn = 0
    for i,bear1 in enumerate(self.canProcreate):
      if bear1.canBreed:
        while i+1 < len(self.canProcreate) and \
             abs(bear1.age - self.canProcreate[i+1].age) <= ageDiff:
          bear2 = self.canProcreate[i+1]
          if ( bear1.mother != bear2.mother ) \
             and ( bear1.father != bear2.father ) \
             and ( bear1.sex != bear2.sex ) \
             and bear2.canBreed:
            if bear1.sex == 'M':
              male, female = bear1, bear2
            else:
              female, male = bear1, bear2
            cub = self.createCub(pMale, female, male)
            numBorn += 1
            self.allBears.append(cub)
            male.LastProcreation = year
            female.LastProcreation = year
            male.canBreed = False
            female.canBreed = False
            break
          i += 1
    return numBorn
