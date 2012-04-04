#!/usr/bin/env python
"""
AY 250 - Scientific Research Computing with Python
Homework Assignment 3 - Parallel Feature Extraction Example
Author: Christopher Klein
"""
from os import listdir
from multiprocessing import Pool, cpu_count
from pylab import imread
from time import time
import numpy as np
import featureExtractor
from scipy import ndimage

# FUNCTION DEFINITIONS
# Quick function to divide up a large list into multiple small lists, 
# attempting to keep them all the same size. 
def split_seq(seq, size):
        newseq = []
        splitsize = 1.0/size*len(seq)
        for i in range(size):
            newseq.append(seq[int(round(i*splitsize)):
                int(round((i+1)*splitsize))])
        return newseq
# Our simple feature extraction function. It takes in a list of image paths, 
# does some measurement on each image, then returns a list of the image paths
# paired with the results of the feature measurement.
def extract_features(image_path_list):
  feature_list = []
  for image_path in image_path_list:
    features = []
    image_array = imread(image_path)
# Note: Looping through multiple filters for edge detection drastically slows
# Down the feature extraction while only marginally improving performance, thus
# it is left out for the HW submission
#     for ax in [0,1]:
#       for pct in [.01, .02]:
    emat = featureExtractor.getEdgeMatrix(image_array, sigpercent=.01, \
                                               axis=0)
    features.append( featureExtractor.getEdgePercent(image_array, emat) )
    features.append( featureExtractor.getNumMeridialEdges(emat) )
    features.append( featureExtractor.getNumEquatorialEdges(emat) )
    features.append( featureExtractor.getSize(image_array) )
    features.append( featureExtractor.getCentralRatio(image_array) )
    features.append( featureExtractor.getCentralRatio(emat) )
    features.append( featureExtractor.getMeanColorVal(image_array, 0) )
    features.append( featureExtractor.getMeanColorVal(image_array, 1) )
    features.append( featureExtractor.getMeanColorVal(image_array, 2) )
    features.append( featureExtractor.getVariance( image_array, 0 ) )
    features.append( featureExtractor.getVariance( image_array, 1 ) )
    features.append( featureExtractor.getVariance( image_array, 2 ) )
    xr, yr = featureExtractor.getCOM(image_array, 0)
    features.append(xr)
    features.append(yr)
    xg, yg = featureExtractor.getCOM(image_array, 1)
    features.append(xg)
    features.append(yg)
    xb, yb = featureExtractor.getCOM(image_array, 2)
    features.append(xb)
    features.append(yb)
    feature_list.append([image_path, features])
  return feature_list



### Main program starts here ###################################################
# We first collect all the local paths to all the images in one list
image_paths = []
categories = listdir("50_categories")
for category in categories:
    image_names = listdir("50_categories/" + category)
    for name in image_names:
        image_paths.append("50_categories/" + category + "/" + name)

print ("There should be 4244 images, actual number is " + 
    str(len(image_paths)) + ".")

# Then, we run the feature extraction function using multiprocessing.Pool so 
# so that we can parallelize the process and run it much faster.
numprocessors = cpu_count() # To see results of parallelizing, set numprocessors
                            # to less than cpu_count().
# numprocessors = 1

# We have to cut up the image_paths list into the number of processes we want to
# run. 
split_image_paths = split_seq(image_paths, numprocessors)

# Ok, this block is where the parallel code runs. We time it so we can get a 
# feel for the speed up.
start_time = time()
p = Pool(numprocessors)
result = p.map_async(extract_features, split_image_paths)
poolresult = result.get()
end_time = time()

# All done, print timing results.
print ("Finished extracting features. Total time: " + 
    str(round(end_time-start_time, 3)) + " s, or " + 
    str( round( (end_time-start_time)/len(image_paths), 5 ) ) + " s/image.")
# This took about 10-11 seconds on my 2.2 GHz, Core i7 MacBook Pro. It may also
# be affected by hard disk read speeds.

# To tidy-up a bit, we loop through the poolresult to create a final list of
# the feature extraction results for all images.
combined_result = []
for single_proc_result in poolresult:
    for single_image_result in single_proc_result:
        combined_result.append(single_image_result)
# Convert the results from list to an array for easy indexing
results = np.array(combined_result, dtype=object)
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
results.sort(axis=0)
n = list(np.unique(results[:,0]))
v = range(len(n))
nameToInt = dict(zip(n,v))
intToName = dict(zip(v,n))
# Create the target vector for the random forest classifier
Yv = []
for item in results[:,0]:
  Yv.append(nameToInt[item])

# Determine how many of each example type there are
numExamples = []
for name in n:
  num = 0
  for i in range(len(results)):
      if results[i,0] == name:
          num += 1
  numExamples.append(num)
# Determine how many examples will be used as trainers and testers
cutoff = (2/3.)
lims = np.array(numExamples) * cutoff
lims = lims.astype(int)

# Get the training examples and test examples
cumsum = np.cumsum(numExamples)
Xtr = []
Ytr = []
Xte = []
Yte = []

start = 0
ind = 0
k = 0
while k < len(results):
  if k < start + lims[ind]:
    Xtr.append(Xv[k])
    Ytr.append(Yv[k])
  else:
    Xte.append(Xv[k])
    Yte.append(Yv[k])
  if k in np.cumsum(numExamples):
    start = k
    ind += 1
  k += 1

# Machine Learning part
from sklearn.ensemble import RandomForestClassifier
from sklearn import grid_search
from sklearn import metrics

parameters = {'n_estimators':[10, 20, 50, 100], 'max_features':[10, 15]}
print "Classifier tuning beginning..."
trainStart = time()
rf_tune = grid_search.GridSearchCV(RandomForestClassifier(), parameters,\
          score_func=metrics.zero_one_score, n_jobs=8, cv=5)
rf_opt = rf_tune.fit(Xtr, Ytr)
trainEnd = time()
print "Training Complete! Training took %s seconds" %( trainEnd-trainStart )
print "Best zero-one score: " + str(rf_opt.best_score) + "\n"
print "Optimal Model:\n" + str(rf_opt.best_estimator_)

print 'Success Rate = %s --- %s times better than \
unweighted guessing' %(rf_opt.best_score, rf_opt.best_score/(.02) )
