from simulateBearPopulation_varProb import simulateBears

# This script estimates the value of P(male) required to sustain a bear 
# population to 150 years. It is stochastic, so the answer will be different
# after each run. Increase the numAttemptsPerPoint for a higher-confidence
# answer.

numYears = 150
numAttemptsPerPoint = 1000
done = False
for i in range(1,101):
  pMale = i*.01
  print "Checking probMale = %s" %pMale
  for j in range(1,numAttemptsPerPoint+1):
    numBorn, numAlive = simulateBears(numYears, pMale)
    if numAlive != 0:
      print '''The minimum probability for male production to ensure population
               survival was found to be: %s ''' %(pMale)
      done = True
      break
  if done: break
