def simulateBears(numYears, pMale):
  
  from BearClass_varProb import Bear
  from BearPopulationClass_varProb import BearPopulation

  # Create the starting population
  # Make some "bear gods" to use as the parents for the progenitors
  beargod1 = Bear(pMale,'bg1','M',None, None)
  beargod2 = Bear(pMale,'bg2','M',None, None)
  beargod3 = Bear(pMale,'bg3','F',None, None)
  adam = Bear(pMale, 'Adam', 'M',beargod1,beargod1)
  eve = Bear(pMale, 'Eve', 'F',beargod2,beargod2)
  mary = Bear(pMale, 'Mary', 'F',beargod3,beargod3)
  year = 0
  numBornInFirst100Years = 0
  
  # keep track of the number of males and females created
  #nMale = 1
  #nFemale = 2
  
  # Create a bear population from the progenitors
  progenitors = [adam, eve, mary]
  population = BearPopulation(progenitors)
  
  # Start stepping through time
  years = range(1,numYears+1)
  for year in years:
#    print "It is now the year: %s" %(year)
    # First things first: each bear gets a year older
    population.ageBears()
    # Now, what happens as the bears age
  
    # First, check if any bears died and add them to the part of the population
    # that has died
    population.checkForDead(year)
  #  for bear in population.allBears:
  #    print bear
    # Create a list of bears that are capable of procreating
    population.checkIfCanBang(year)
    numBornThisYear = population.generateOffspring(year, pMale)
    if year <= 100:
      numBornInFirst100Years += numBornThisYear
  #  nMale += newM
  #  nFemale += newF
    # Print the size of the population each year
#    print "Number of bears in population after %s years: %s" %(year, \
#          len(population.allBears) )
  #  for bear in population.canProcreate:
  #    print bear
  
  # Print the bear population
  #for bear in population.allBears:
  #  print bear
  
#  print "Final Number of Bears after %i Years: %s" \
#        %(numYears, len(population.allBears))
  return numBornInFirst100Years, len(population.allBears)
