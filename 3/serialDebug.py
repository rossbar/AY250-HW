#!/usr/bin/env python
"""
AY 250 - Scientific Research Computing with Python
Homework Assignment 3 - Parallel Feature Extraction Example
Author: Christopher Klein
"""
from os import listdir
from pylab import imread
from time import time
import featureExtractor

# Our simple feature extraction function. It takes in a list of image paths, 
# does some measurement on each image, then returns a list of the image paths
# paired with the results of the feature measurement.
def extract_features(image_path_list):
    feature_list = []
    for image_path in image_path_list:
        image_array = imread(image_path)
#        emat = featureExtractor.getEdgeMatrix(image_array, 3)
#        feature = featureExtractor.getNumMeridialEdges(emat)
        feature = featureExtractor.getMeanGreenVal(image_array)
        feature_list.append([image_path, feature])
    return feature_list



### Main program starts here ###################################################
# We first collect all the local paths to all the images in one list
image_paths = []
categories = listdir("50_categories")
for category in categories:
	image_names = listdir("50_categories/" + category )
	for name in image_names:
        	image_paths.append("50_categories/" + category + "/" + name)

print ("There should be 4244 images, actual number is " + 
    str(len(image_paths)) + ".")

start_time = time()
featureList = extract_features(image_paths)
end_time = time()

# All done, print timing results.
print ("Finished extracting features. Total time: " + 
    str(round(end_time-start_time, 3)) + " s, or " + 
    str( round( (end_time-start_time)/len(image_paths), 5 ) ) + " s/image.")
