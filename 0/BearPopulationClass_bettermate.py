from BearClass import Bear
from globalFunctions_tryrand import *

# Some important variables
waitPeriod = 5 # number of years between procreations
ofAge = 5      # age at which bears start doin it
ageDiff = 10   # Max age difference allowed between mating bears

class BearPopulation(object):
  '''An object of this class stores the population of bears'''

  def __init__(self, bearList):
    self.allBears = bearList
    self.index = -1
    self.size = len(self.allBears)
    self.deceased = []

  def __iter__(self):
    return self

  def next(self):
    if self.index == self.size - 1:
      raise StopIteration
    self.index += 1
    return self.allBears[self.index]

  def ageBears(self):
    for bear in self.allBears:
      bear.age += 1

  def checkForDead(self, year):
    for i,bear in enumerate(self.allBears): 
      if bear.age >= bear.TOD:
        died = self.allBears.pop(i)
        self.deceased.append( (died.name, year) )
        self.size = len(self.allBears)
#        print "%s died in year %s at age %s" %(bear.name, year, bear.age)

  def checkIfCanBang(self, year):
    self.canProcreateMale = []
    self.canProcreateFemale = []
    for bear in self.allBears:
      if bear.age >= ofAge and ( bear.LastProcreation == None or \
                             year - bear.LastProcreation >= waitPeriod ):
        bear.canBreed = True
        if bear.sex == 'F':
          self.canProcreateFemale.append(bear)
        else:
          self.canProcreateMale.append(bear)
#    for bear in self.canProcreateMale:
#      print bear
#    for bear in self.canProcreateFemale:
#      print bear

  def createCub(self, mother, father):
    sex = determineSex(father)
    name = getNewName(sex)
    cub = Bear(name, sex, mother, father)
    return cub
 
  def generateOffspring(self, year):
    
    numMales = len(self.canProcreateMale)
    numFemales = len(self.canProcreateFemale)
#    print "num males: %s\tnumfemales: %s" %(numMales, numFemales)
    
    for male in self.canProcreateMale:
      if male.canBreed:
        for female in self.canProcreateFemale:
          if female.canBreed:
            if ( male.mother != female.mother ) and ( male.father != \
               female.father ) and ( male.age - female.age <= ageDiff ):
              cub = self.createCub(female, male)
              self.allBears.append(cub)
              male.LastProcreation = year
              female.LastProcreation = year
              ############# watchout
              male.canBreed = False
              female.canBreed = False
