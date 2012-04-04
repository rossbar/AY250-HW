import numpy as np
import featureExtractor

# Change the format of the results so that the first entry is the type of the
# object and the second is the corresponding feature vector
for i in range(len(results)):
  results[i][0] = results[i][0].split('/')[1]

# Create feature vectors in proper format for use with rndforest
Xv = np.zeros( [len(results), len(results[0][1])] )
for i in range(len(results)):
  for j in range(len(results[0][1])):
    Xv[i][j] = results[i][1][j]

# The random forest classifier can only deal with ints as the target variable.
# Create a dictionary converting each name to a unique integer, and a dictionary
# for translating back as well
n = list(np.unique(results[:,0]))
v = range(len(n))
nameToInt = dict(zip(n,v))
intToName = dict(zip(v,n))
# Create the target vector for the random forest classifier
Yv = []
for item in results[:,0]:
  Yv.append(nameToInt[item])

# Determine how many of each example type there are
for name in types:
  num = 0
  for i in range(len(results)):
      if results[i,0] == name:
          num += 1
  numExamples.append(num)

