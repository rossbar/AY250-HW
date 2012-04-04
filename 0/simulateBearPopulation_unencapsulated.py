from BearClass import Bear
from BearPopulationClass import BearPopulation

# Create the starting population
adam = Bear('Adam', 'M')
eve = Bear('Eve', 'F')
mary = Bear('Mary', 'F')
year = 0

# Create a bear population from the progenitors
progenitors = [adam, eve, mary]
population = BearPopulation(progenitors)

# Start stepping through time
years = range(1,44)
for year in years:
  print "It is now the year: %s" %(year)
  for i,bear in enumerate(population.allBears):
    # First things first: each bear gets a year older
    bear.age += 1
    # Now, what happens as the bears age

    # First, check if any bears died and add them to the part of the population
    # that has died
    if bear.age >= bear.TOD:
      died = population.allBears.pop(i)
      population.deceased.append( (died, year) )
      print "%s died in year %s at age %s" %(bear.name, year, bear.age)
    # Create a list of bears that are capable of procreating
    if bear.canBreed:
      population.canProcreate.append(bear)
    print bear
