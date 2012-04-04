from PIL import Image
from urllib import urlretrieve
from matplotlib.pyplot import imshow
import pybing
import numpy as np

def getFirstImage( searchTerm, APIkey, show=False ):
  '''Given a search term, this function returns the first image that results
     from a bing image search for that term. '''
  bing = pybing.Bing( APIkey )
  response = bing.search_image( searchTerm )
  results = response['SearchResponse']['Image']['Results']
  firstResult = results[0]
  imglink = firstResult['MediaUrl']
  imgdata = urlretrieve( imglink )
  img = imgdata[0]
  im = Image.open(img)
  imAry = np.array( im )
  if show: imshow(imAry)
  return imAry, imglink
