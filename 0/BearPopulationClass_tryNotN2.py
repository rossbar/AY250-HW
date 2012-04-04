from BearClass import Bear
from globalFunctions_tryrand import *
import networkx as nx

# Some important variables
waitPeriod = 5 # number of years between procreations
ofAge = 5      # age at which bears start doin it
ageDiff = 10   # Max age difference allowed between mating bears

class BearPopulation(object):
  '''An object of this class stores the population of bears'''

  def __init__(self, bearList):
    self.allBears = bearList
    self.tree = nx.DiGraph() 
#    self.index = -1
#    self.size = len(self.allBears)

#  def __iter__(self):
#    return self

#  def next(self):
#    if self.index == self.size - 1:
#      raise StopIteration
#    self.index += 1
#    return self.allBears[self.index]

  def ageBears(self):
    for bear in self.allBears:
      bear.age += 1 

  def checkForDead(self, year):
    for bear in self.allBears: 
      if bear.age >= bear.TOD:
        self.allBears.remove(bear)
#        print "%s died in year %s at age %.0f" %(bear.name, year, bear.TOD)

#  def removeDead(self):
#    for bear in self.allBears:
#      if bear.Dead == True:
#        sel

  def checkIfCanBang(self, year):
    self.canProcreate = []
    for bear in self.allBears:
      if bear.age >= ofAge and ( bear.LastProcreation == None or \
                             year - bear.LastProcreation >= waitPeriod ):
        bear.canBreed = True
        self.canProcreate.append(bear)
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
    
#    numMales = len(self.canProcreateMale)
#    numFemales = len(self.canProcreateFemale)
#    print "num males: %s\tnumfemales: %s" %(numMales, numFemales)
    numBorn = 0
    for i,bear1 in enumerate(self.canProcreate):
      if bear1.canBreed:
#        print "Bear 1 is: ", bear1
        while i+1 < len(self.canProcreate) and \
             abs(bear1.age - self.canProcreate[i+1].age) <= ageDiff:
          bear2 = self.canProcreate[i+1]
#          print "Bear 2 candidate: ", bear2
          if ( bear1.mother != bear2.mother ) \
             and ( bear1.father != bear2.father ) \
             and ( bear1.sex != bear2.sex ) \
             and bear2.canBreed:
            if bear1.sex == 'M':
              male, female = bear1, bear2
            else:
              female, male = bear1, bear2
            cub = self.createCub(female, male)
            numBorn += 1
#            print "Cub Made!"
            self.allBears.append(cub)
            self.tree.add_node(cub)
            self.tree.add_edge(male, cub)
            self.tree.add_edge(female, cub)
            male.LastProcreation = year
            female.LastProcreation = year
            ############# watchout
            male.canBreed = False
            female.canBreed = False
            break
          i += 1
    return numBorn
