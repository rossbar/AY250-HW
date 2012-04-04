from BearClass import Bear
from globalFunctions import *

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
        print "%s died in year %s at age %s" %(bear.name, year, bear.age)

  def checkIfCanBang(self, year):
    self.canProcreate = []
    for bear in self.allBears:
      if bear.age >= ofAge and ( bear.LastProcreation == None or \
                             year - bear.LastProcreation > waitPeriod ):
        self.canProcreate.append(bear)

  def createOffspring(self, year, nMale, nFemale):

#    if len(self.canProcreate) > 0:
#      print "Now in createOffspring"
    # Need a list of currently used names so we don't double up
   
    numFemale = 0
    numMale = 0
    fcubs, mcubs = 0, 0
    for bear in self.canProcreate:
      if bear.sex == 'F':
        numFemale += 1
      else:
        numMale += 1
    
    numTries = 0
    while ( (numFemale != 0) and (numMale != 0) ):
#      currentNames = []
#      for bear in self.allBears:
#        currentNames.append(bear.name)
 

      # This part sorts the list so that the least common sex is chosen as the
      # mater
      self.canProcreate.sort(key=lambda x:x.sex)
#      if numMale < numFemale:
      self.canProcreate.reverse()
      bear1 = self.canProcreate[0]

      for bear in self.canProcreate:
        if bear.sex != bear1.sex:
          bear2 = bear
    
### Below okay
      if ( bear1.mother != bear2.mother ) and ( bear1.father != \
           bear2.father ) and ( bear1.sex != bear2.sex ) and ( bear1.age - \
           bear2.age <= ageDiff ):
        # Determine which bear is the mother
        if bear1.sex == 'F':
          mother, father = bear1, bear2
        else:
          mother, father = bear2, bear1
        # Get cub's sex
        sex = determineSex(bear1)
        if sex == 'M':
          mcubs += 1
        else:
          fcubs += 1
        # Get cub's name
#        name = getNewName(currentNames, sex, nMale + mcubs, nFemale + fcubs)
        name = getNewName(sex, nMale + mcubs, nFemale + fcubs )
        # Add the new cub
        cub = Bear(name, sex, mother, father)
        self.allBears.append(cub)
        # Remove parents from the list and UPDATE lastProcreated and deprecate 
        # the while loop
        bear1.LastProcreation = year
        bear2.LastProcreation = year
        self.canProcreate.remove(bear1)
        self.canProcreate.remove(bear2)
        numFemale -= 1
        numMale -= 1
#        print 'Cub made!'
############### DANGER - THIS SHIT IS WHY IT'S SO SLOW! ######################
      if numTries > len(self.canProcreate)*2:
        print "Broke Out!"
        break
      else:
        numTries += 1
        continue 
    return mcubs, fcubs
