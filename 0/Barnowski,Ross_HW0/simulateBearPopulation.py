def simulateBears(numYears):
  '''This function simulates the propagation of a bear population from three
     starting bears. The functionality includes the mating of bears and the
     removal of dead bears. The mating occurs only every 5 years (according
     to the problem prompt, but this can be changed). The function returns
     the number of bears alive after the set simulation time, as well as the
     number of bears born within the first 100 years (or x years if x < 100 ''' 
  from BearClass import Bear
  from BearPopulationClass_tryNotN2 import BearPopulation
  import networkx as nx

  # Create the starting population
  # Make some "bear gods" to use as the parents for the progenitors
  beargod1 = Bear('bg1','M',None, None)
  beargod2 = Bear('bg2','M',None, None)
  beargod3 = Bear('bg3','F',None, None)
  adam = Bear('Adam', 'M',beargod1,beargod1)
  eve = Bear('Eve', 'F',beargod2,beargod2)
  mary = Bear('Mary', 'F',beargod3,beargod3)
  year = 0
  numBornInFirst100Years = 0
  
  # Create a bear population from the progenitors
  progenitors = [adam, eve, mary]
  population = BearPopulation(progenitors)
  
  # Start stepping through time
  years = range(1,numYears+1)
  for year in years:
#    print "It is now the year: %s" %(year)
    # First things first: each bear gets a year older
    population.ageBears()
  
    population.checkForDead(year)
    # Create a list of bears that are capable of procreating
    population.checkIfCanBang(year)
    # Generate off-spring and keep track of how many are born per year
    numBornThisYear = population.generateOffspring(year)
    if year <= 100:
      numBornInFirst100Years += numBornThisYear
    # Print the size of the population each year
#    print "Number of bears in population after %s years: %s" %(year, \
#          len(population.allBears) )
  
  print "Final Number of Bears after %i Years: %s" \
        %(numYears, len(population.allBears))
  # Print the genealogy tree of the bears. This is only done if there is a 
  # relatively small number of bears otherwise the graph becomes pretty 
  # hard to read
  if len(population.allBears) <= 1500:
    nx.draw_circular(population.tree)
  return numBornInFirst100Years, len(population.allBears)
