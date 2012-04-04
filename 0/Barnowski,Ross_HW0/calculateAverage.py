from simulateBearPopulation import simulateBears
import math

# This script calculates the average number of bears after 150 years and the
# average number of bears born in the first 100 years

numBearList = []
numBornList = []
numRuns = 10	# Number of runs to average over
numYears = 150	# Number of years to run the simulation for
for i in range(1,numRuns+1):
  print "Run #: %s out of %s" %(i, numRuns)
  numBorn, numBears = simulateBears(numYears)
  numBearList.append(numBears)
  numBornList.append(numBorn)

avgAlive = sum(numBearList)/numRuns
#errAlive = math.sqrt(avgAlive)/math.sqrt(numRuns)

avgBorn = sum(numBornList)/numRuns
#errBorn = math.sqrt(avgBorn)/math.sqrt(numRuns)

print "The average number of bears after %s years is %s" \
      %(numYears, avgAlive)
print "The average number of bears born in the first 100 years is: \
      %s" %(avgBorn)
