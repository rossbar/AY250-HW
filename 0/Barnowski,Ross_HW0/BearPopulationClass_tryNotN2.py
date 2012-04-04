from BearClass import Bear
from globalFunctions_tryrand import *
import networkx as nx

# Some important variables
waitPeriod = 5 # number of years between procreations
ofAge = 5      # age at which bears start doin it
ageDiff = 10   # Max age difference allowed between mating bears

class BearPopulation(object):
  '''An object of this class stores the population of bears. Attributes include
     the list containing all bears, the nx object containing the geneological
     info, and a list that contains all the bears who meet the criteria for
     mating. Methods include those to determine whether bears can mate, 
     create new bears and remove dead ones'''

  def __init__(self, bearList):
    self.allBears = bearList
    self.tree = nx.DiGraph() 

  def ageBears(self):
    '''Age the bears for the simulation. The value should be 1 if you want to
       see the details of how many bears die per year, but can be set to 5 if
       you don't. Make sure the value here matches the value in range() in
       the simulateBears function'''
    for bear in self.allBears:
      bear.age += 1 

  def checkForDead(self, year):
    '''Remove bears when the year is greater than their pre-determined, 
       normally distributed time of death'''
    for bear in self.allBears: 
      if bear.age >= bear.TOD:
        self.allBears.remove(bear)

  def checkIfCanBang(self, year):
    '''Puts all the bears that meet the criteria for mating in a list and set
       their can-breed flags to true'''
    self.canProcreate = []
    for bear in self.allBears:
      if bear.age >= ofAge and ( bear.LastProcreation == None or \
                             year - bear.LastProcreation >= waitPeriod ):
        bear.canBreed = True
        self.canProcreate.append(bear)

  def createCub(self, mother, father):
    '''Given 2 bears that can mate, make a cub'''
    sex = determineSex(father)
    name = getNewName(sex)
    cub = Bear(name, sex, mother, father)
    return cub
 
  def generateOffspring(self, year):
    '''Runs through the list of bears that can breed and makes sure that all
       the bears which are able to breed each year do so (occurs only every
       5 years using the default paramters). Since the list of bears that can
       procreate is sorted by age, the inner loop stops if the age difference
       gets greater than 10 to avoid O(N^2) behavior'''
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
            cub = self.createCub(female, male)
            numBorn += 1
            self.allBears.append(cub)
            # Add nodes to the genealogy tree
            self.tree.add_node(cub)
            self.tree.add_edge(male, cub)
            self.tree.add_edge(female, cub)
            male.LastProcreation = year
            female.LastProcreation = year
            # The 2 bears that have just bred are no longer eligible to do so
            # this turn
            male.canBreed = False
            female.canBreed = False
            break
          i += 1
    return numBorn
