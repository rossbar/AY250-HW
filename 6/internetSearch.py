from enthought.traits.api import HasTraits, Str, Int, Directory, Float, Array,\
                                 Enum, Button, Instance
from enthought.traits.ui.api import View, Item, Group, ButtonEditor
import imageSearch
from mpl_figure_editor import *
from matplotlib.pyplot import draw
from matplotlib import cm
from imageModifier import *

# Bing API developer key
key = 'F5C4151C230CD2C58D679FE7438FE2C315CAE19A'

class internetSearchUI(HasTraits):
  '''Class containing traited and non-traited features. The traited features
     are used to build the GUI while the non-traited features are used by the
     functions called by the buttons.'''

  # Initialize some fields with traits
  Query = Str("<Enter Query and Press Search Button>")
  Result = Str
  figure = Instance(Figure, ())

  # Create the buttons
  searchButton = Button('Search')
  rotateButton = Button('Rotate 90 CCW')
  blurButton = Button('Blur')
  swapColorButton = Button('Swap Color Channels')
  revertButton = Button('Revert Image')

  #### Helper functions called whenever an image manipulation button is pressed
  def showImage(self):
    '''Correctly displays grayscale and color images'''
    if self.image.ndim == 3: self.axes.imshow(self.image)
    else: self.axes.imshow( self.image, cmap=cm.gist_gray )
    self.figure.canvas.draw()

  def checkNoImage(self):
    '''Returns True if there is no axis object in the figure yet (i.e. the 
       internet search hasn't been carried out)'''
    if self.figure.axes == []:
      print 'No image yet... search first'
      return True
  
  def _searchButton_fired(self):
    '''When the button is pressed, use the query to find an image from the
       interwebz. '''
    if self.Query == "<Enter Query and Press Search Button>":
      print 'Enter a search term!'
      return
    else:
      # Use the pybing module to get the image
      self.image, self.Result = imageSearch.getFirstImage( self.Query, key,\
                                show=False )
      # Set the image as the original in case the user wants to revert
      self.originalImage = self.image
      # Put axes in the figure
      self.axes = self.figure.add_subplot(111)
      self.showImage()

  def _swapColorButton_fired(self):
    '''When the button is pressed, swap the color channels'''
    if self.checkNoImage(): return
    else:
      self.image = swapColorChannels(self.image)
      self.showImage()
      

  def _blurButton_fired(self):
    '''When the button is pressed, blur the image.'''
    if self.checkNoImage(): return
    else:
      self.image = blurImage(self.image)
      self.showImage()

  def _rotateButton_fired(self):
    '''When the button is pressed, rotate the image 90 degrees'''
    if self.checkNoImage(): return
    else:
      self.image = rotateImage(self.image)
      self.showImage()

  def _revertButton_fired(self):
    '''When pressed, reverts to the original image '''
    if self.checkNoImage():return
    else:
      self.image = self.originalImage
      self.showImage()

# Simpler view - not used
defaultView = View( Item('Query', width=-250, resizable=False), Item('Result',\
              width=-250, resizable=False),\
              Item('figure', editor=MPLFigureEditor(), show_label=False, \
              width=400, height=400, resizable=True), Item('swapColorButton',\
              editor=ButtonEditor(label_value='SwapColors'), show_label=False),\
              Item('rotateButton', editor=ButtonEditor(), show_label=False),\
              Item('blurButton', editor=ButtonEditor(), show_label=False),\
              Item('searchButton',editor=ButtonEditor(label_value='Search'),\
              show_label=False),\
              title='Web Image Roulette', resizable=True, scrollable=False )

# View that includes grouping. This is the view currently being used.
view1 = View(Group(Item( name = 'Query', width=-250, resizable=False ),\
Item( 'searchButton', editor=ButtonEditor(), show_label=False, dock='fixed' ),\
label = 'Search', show_border = True),\
Item('figure', editor=MPLFigureEditor(), show_label=False, width=400, height=\
400, resizable=True),
Group( Item( name='rotateButton', editor=ButtonEditor(), show_label=False, \
dock='horizontal'),\
Item( name = 'blurButton', editor=ButtonEditor(), show_label=False, \
dock='horizontal'), Item( name = 'swapColorButton', editor=ButtonEditor(),\
 show_label=False, dock='horizontal'),\
Item( name = 'revertButton', editor=ButtonEditor(), show_label=False ),\
label = 'Image Manipulation', show_border=True),\
title='Web Image Roulette', resizable=True, scrollable=False )

# Create the object and view the gui
ui = internetSearchUI()
ui.configure_traits(view=view1)
