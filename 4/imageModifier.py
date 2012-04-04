import numpy as np
from formatImage import *
from scipy import ndimage

class imageModifier(object):
  def rotateImage(self, imgVec, theta):
    '''Usage: rotateImage(imgVec, theta)
       
       imgVec -- python list object with the following format:
       imgVec[0:3] = [ # dimensions, img length, img width] (all ints)
       imgVec[3:]  = [ Actual image values (i.e. image.ravel().tolist() ]

       theta = Angle that image will be rotated
       
       Rotates the given image by theta degrees. Returns the following tuple:
       (original image, rotated image) in the same format as the input'''
    img = unpackImage(imgVec)
    rotatedIm = ndimage.rotate(img, theta)
    orig = packImage(img)
    rotated = packImage(rotatedIm)
    return orig, rotated
  
  def swapColorChannels(self, imgVec):
    '''Usage: swapColorChannels(imgVec)

       imgVec -- python list object with the following format:
       imgVec[0:3] = [ # dimensions, img length, img width] (all ints)
       imgVec[3:]  = [ Actual image values (i.e. image.ravel().tolist() ]

       If the image is color (RGB), this function transforms the colors like so:
       orig -> new
        G   -> R
        B   -> G
        R   -> B

       If the image is grayscale, the image is inverted and a warning appears
       alerting the user that the behavior is the same as for the
       invertImage function

       Rerturns a tuple: (orignal image, swapped image) in the "packed" format
       '''
    img = unpackImage(imgVec)
    newimg = np.zeros( img.shape, dtype=np.uint8 )
    if img.ndim == 3:
      newimg[:,:,0] = img[:,:,1]
      newimg[:,:,1] = img[:,:,2]
      newimg[:,:,2] = img[:,:,0]
    else:
      print '''Warning: Color swapping does not work for grayscale images! The\
 Image has been inverted instead.'''
      newimg = 255 - img
    orig = packImage(img)
    swapped = packImage(newimg)
    return orig, swapped

  def invertImage(self, imgVec, invertLim=255, useImgMax=False):
    '''Usage: edgeDetector(imgVec, sig)

       imgVec -- python list object with the following format:
       imgVec[0:3] = [ # dimensions, img length, img width] (all ints)
       imgVec[3:]  = [ Actual image values (i.e. image.ravel().tolist() ]
       
       invertLim: The limit against which the color (or brightness for 
       grayscale) of a pixel will be inverted. Default value = 255.

       useImgMax: Boolean - if True, uses the maximum pixel value from the 
       image as invertLim. Default = False

       Generates an image where every pixel in the image has be inverted, i.e.
       newPixVal = invertLim - origPixVal

       NOTE: Code does not check for negative values. If invertLim is set below
       the maximum possible value, the code will not produce an error, but the
       resulting image will not be the true inversion of the original.

       Rerturns a tuple: (orignal image, inverted image) in the "packed" format
       '''
    img = unpackImage(imgVec)
    if useImgMax:
      maxVal = img.max()
    else:
      maxVal = invertLim
    invertedImg = maxVal - img
    orig = packImage(img)
    inverted = packImage(invertedImg)
    return orig, inverted
