import numpy as np
from scipy import ndimage

def rotateImage(img):
  '''Returns a new image that has been rotated 90 degrees counter-clockwise'''
  theta=90
  rotatedIm = ndimage.rotate(img, theta)
  return rotatedIm

def swapColorChannels(img):
  '''Returns a new image with the color channels swapped.
     If the image is color (RGB), this function transforms the colors like so:
     orig -> new
      G   -> R
      B   -> G
      R   -> B
     If the image is gray scale, the image is inverted.'''

  newimg = np.zeros( img.shape, dtype=np.uint8 )
  if img.ndim == 3:
    newimg[:,:,0] = img[:,:,1]
    newimg[:,:,1] = img[:,:,2]
    newimg[:,:,2] = img[:,:,0]
  else:
    print '''Warning: Color swapping does not work for grayscale images! The\
 image has been inverted instead.'''
    newimg = 255 - img
  return newimg

def blurImage(img):
  '''Returns a blurred version of the original image. Blurring from uniform 
     filter with width= 3% of the largest image dimension.'''
  newimg = np.empty(img.shape, dtype=np.uint8)
  blurval = int( 0.03*max(img.shape) )
  if img.ndim == 3:
    for i in range(img.ndim):
      newimg[:,:,i] = ndimage.uniform_filter(img[:,:,i], blurval)
  else:
    newimg = ndimage.uniform_filter(img, blurval)
  return newimg
