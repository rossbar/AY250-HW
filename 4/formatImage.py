import numpy as np

def unpackImage(imgVec):
  '''Converts image from the specified input format into a np.ndarray image. '''
  if type(imgVec) != list:
    print 'Warning: Unexpected input format. Image must be a 1-D list!'
    return
  numDim = imgVec[0]
  imglen = imgVec[1]
  imgwth = imgVec[2]
  img = np.array( imgVec[3:], dtype=np.uint8 )
  if numDim == 3:
    img = img.reshape(imglen, imgwth, 3)
  elif numDim == 2:
    img = img.reshape(imglen, imgwth)
  else:
    print 'Warning: Image format not understood!'
    return
  return img

def packImage(img):
  '''Converts image from an np.ndarray object into a list so that it can be
     passed by the xmlrpc server. The output has the same format as described
     by the image modifier. '''
  if type(img) != np.ndarray:
    img = np.array(img)
  imgList = imgVec = [img.ndim, img.shape[0], img.shape[1]]\
                      + img.ravel().tolist()
  return imgList


