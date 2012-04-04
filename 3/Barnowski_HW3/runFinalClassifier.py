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


def trainClassifier():
  image_paths = []
  categories = listdir("50_categories")
  for category in categories:
      image_names = listdir("50_categories/" + category)
      for name in image_names:
          image_paths.append("50_categories/" + category + "/" + name)
  
  print ("There should be 4244 images, actual number is " + 
      str(len(image_paths)) + ".")
  numprocessors = cpu_count()
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
  
  Xtr = Xv 
  Ytr = Yv

  # Train the RF classifier with the training set only
  from sklearn.ensemble import RandomForestClassifier
  classifier = RandomForestClassifier(n_estimators=100)
  print "Classifier training beginning..."
  trainStart = time()
  classifier.fit(Xtr, Ytr)
  trainEnd = time()
  print "Training Complete! Training took %s seconds" %( trainEnd-trainStart )
  
  return classifier

def runFinalClassifier(classifier, path_to_validation):
  image_paths = []
  image_names = listdir(path_to_validation)
  for name in image_names:
    image_paths.append(path_to_validation + "/" + name)
  numprocessors = cpu_count()
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

  # Use the trained classifier to predict the outcomes of the images in the
  # test set
  numCorrect = 0
  for val in range(len(Yv)):
    predVal = intToName[ int( classifier.predict( Xv[val] ) ) ]
    realVal = intToName[ Yv[val] ]
  # Uncomment below to see individual results
    print 'Predicted Image: %s\t\t Actual Image: %s' %(predVal, realVal)
    if predVal == realVal:
      numCorrect += 1
  # Output the final statistics
  print '%s out of %s correct - Success Rate = %s --- %s times better than \
  unweighted guessing' %(numCorrect, len(Yv), float(numCorrect)/len(Yv), \
  (float(numCorrect)/len(Yv)) / (.02) )

################# MAIN

classifier = trainClassifier()
filename = raw_input('Enter the path to the file where the validation photos\
 are kept: ')
runFinalClassifier(classifier, filename)
