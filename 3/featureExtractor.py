from skimage import filter
from scipy import ndimage
import numpy as np

##############################################################################
# This module contains the functions that will extract the features from the
# images. All of these functions should accept an image array (which has 
# already been loaded) and extract a feature from it

def getCOM(img, colorDim):
  '''Use calculate the center of mass of an array of pixels. If the image is
     rgb, the colorDim determines which color the COM will be calculated for '''
  if img.ndim == 3:
    img = img[:,:,colorDim]
  return ndimage.center_of_mass(img)

def getVariance(img, colorDim):
  '''Uses ndimage to calculate the variance of an array of pixels. If the image
     is rgb, the colorDim determines which color the variance will be 
     calculated for '''
  if img.ndim == 3:
    img = img[:,:,colorDim]
  return ndimage.variance(img)

def getCentralRatio(img):
  '''This function divides the input image matrix into a 3x3 coarse grid. It
     then returns the ratio of the intensity of the central coarse pixel to 
     the sum of the intensity of the whole image.'''
  xdim = int( img.shape[0]/3. )
  ydim = int( img.shape[1]/3. )
  if img.ndim == 3:
    img = img.mean(axis=2)
  center = img[xdim:2*xdim, ydim:2*ydim]
  return float(np.sum(center)) / np.sum(img)

def getEdgePercent(img, emat):
  '''Using the edge matrix calculated below, this function returns what 
     fraction of the pixels lie on the edges found by the canny filter.'''
  propEdge = sum(sum(emat))
  if np.ndim(img) == 3:
    return propEdge / (np.size(img)/3.)
  else:
    return propEdge / (np.size(img)/1.)

def getSize(img):
  '''Returns the size (lxw) of the image.'''
  if np.ndim(img) == 3:
    return int( np.size(img)/3. )
  else:
    return np.size(img)

def getMeanColorVal(img, colorDim):
  '''Returns the mean value of the color given by colorDim'''
  if np.ndim(img) == 3:
    img = img[:,:,colorDim]
  return img.mean()

def getEdgeMatrix(img, sigpercent=.01, axis=0):
  '''Use the canny filter to produce a boolean matrix with the same dimensions
     as the image where the value True indicates an edge and False indicates
     no edge. sig is the tuning parameter for the canny filter: a higher sig
     means fewer edges detected (smoother image) '''
  # If the image is not already grayscale, scale it down
  if np.ndim(img) == 3:
    img = img.mean(axis=2)
  edgeMat = filter.canny(img, sigma=sigpercent*np.shape(img)[axis])
  return edgeMat

def getNumMeridialEdges(edgeMat):
  '''This function takes in an edge matrix calculated by the function above
     and returns an int value representing the number of edges at the vertical
     horizon of the image. '''
  # Determine the column of pixels nearest the center of the image
  vc_ind = np.shape(edgeMat)[1] / 2
  vedges = edgeMat.T
  vcedges = vedges[vc_ind]
  return sum(vcedges)

def getNumEquatorialEdges(edgeMat):
  '''Same as above, except at the horizon instead of meridian'''
  hc_ind = np.shape(edgeMat)[0] / 2
  hcedges = edgeMat[hc_ind]
  return sum(hcedges)
