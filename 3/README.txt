Files included with homework submission:

featureExtractor.py
 - Contains the functions used to extract features from the images
parallelFeatures.py
 - Script for extracting the features from the images provided in the 50 
   categories folder. The script then uses the extracted features to train
   the classifier on a training set (2/3 of the images in 50_categories by
   default) and then use the classifier to predict the remaining 1/3 of the
   images. The output is the success rate (compared to the 2% expected from
   unweighted random guessing). Individual output can be activated by un-
   commenting line 191
 - NOTE: This script is based on the parallelization script given out to 
   speed up the feature extraction. As such, the new code is simply added to the
   "main" part of that script.
crossValidate.py
 - This code uses the same feature extraction as parallelFeatures.py. The main
   difference is that instead of training the classifier and using it to 
   predict images as in the last part, it uses some of the classifier tuning
   functionality built into sklearn. 

NOTE: The programs must be run in a directory containing the 50_categories file!
This file is not included in the submission due to its excessive size. The user
must provide their own copy.

Part 1:
  - The functions for feature extraction are included in featureExtractor.py. 
    The file is not used directly, but imported as a module in both part2 and
    part 3.

Part 2:

In [1]: run parallelFeatures

Note: This takes about 410 seconds to run on my 3.4 GHz AMD Phenom Quad-Core.
Also, since the feature extraction is based on a parallel script written by one
of the instructors, the classifier training and use is integrated directly with
the feature extraction. This is not necessary (part 2 only requires the feature
extraction) but serves as a good sanity check to ensure the feature extraction
and the machine vision parts are working as expected.
 - More features were tested and developed, but were not included in the 
   interest of saving computation time (see commented sections in the 
   main feature extraction function. 

The relevant output of the feature extraction includes an array called "results"
that contains the name followed by the feature vector for each image. This 
array is subsequently broken into training and testing inputs (Xtr, Ytr) and
(Xte, Yte) for use with the RF classifier.

Part 3:

In [1]: run crossValidate

Note:The feature extraction took 238 seconds and the cross validation took 69
seconds on a 2.6 GHz i7 8-core cpu. The results for the optimal model and its
performance are output to stdout.

Note: It is possible that the multi-threading will run into a memory error (
occurred once on my work machine with 16 GB of ram). I have no idea how the
multithreading works and no idea how to fix this - just beware that it can
occur.

Part 4:

In [1]: run runFinalClassifier

** When prompted, enter the path to the file containing the validation pics.
