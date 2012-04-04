from simulateBearPopulation_varProb import simulateBears

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
               survival was found to be: %s''' %(100*pMale)
      done = True
      break
  if done: break
