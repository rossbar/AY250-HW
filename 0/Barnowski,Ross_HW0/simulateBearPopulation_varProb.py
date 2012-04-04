def simulateBears(numYears, pMale):
  '''Same functionality as the other simulateBears function, but tweaked to
     handle variable p(male). For documentation, see simulateBearPopulation.py
     '''  
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
  
  # Create a bear population from the progenitors
  progenitors = [adam, eve, mary]
  population = BearPopulation(progenitors)
  
  # Start stepping through time
  years = range(1,numYears+1)
  for year in years:
    population.ageBears()
    population.checkForDead(year)
    population.checkIfCanBang(year)
    numBornThisYear = population.generateOffspring(year, pMale)
    if year <= 100:
      numBornInFirst100Years += numBornThisYear
  
#  print "Final Number of Bears after %i Years: %s" \
#        %(numYears, len(population.allBears))
  return numBornInFirst100Years, len(population.allBears)
