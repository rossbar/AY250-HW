import numpy as np
from matplotlib.widgets import RectangleSelector
from pylab import *
from matplotlib.patches import Rectangle

def isInRect( x, y, rect ):
  '''Given a point defined by x and y, determine if it is within the rectangle.
     rect must be a matplotlib.Patches.Rectangle object'''
  xl, yl = rect.get_xy()
  w, h = rect.get_width(), rect.get_height()
  xl, xh = min(xl, xl+w), max(xl, xl+w)
  yl, yh = min(yl, yl+h), max(yl, yl+h)
  if ( x >= xl and x <= xh ) and ( y >= yl and y <= yh ):
    return True
  else:
    return False

def getHighlightedPoints(xdata, ydata, rect):
  '''For each of the points in xdata, ydata; if the point is in the within the
     rectangle defined by rect, add that point to a list of new points and 
     return the list at the end. These new points will be used to plot the
     "highlighted" points in the clicking widget'''
  xout = []
  yout = []
  for i in range(0,len(xdata)):
    if isInRect(xdata[i], ydata[i], rect):
      xout.append(xdata[i])
      yout.append(ydata[i])
  return xout, yout

#### The meat of the code: Define the functions that are used with the widget
def onselect(eclick, erelease):
  '''eclick and erelease are matplotlib events at press and release. This
     function draws a rectangle in the lower-right subplot (the one with all
     the data in it) and then subsequently highlights any data points that are
     within that rectangle as it is defined in each of the other three sub
     plots'''

  # Only do anything if the button release occurs within the 4th subplot
  # (automatically doesn't do anything if the click is in the 4th subplot)
  if erelease.inaxes == axs[1][1]:
    # Define the rectangle using the coordinates from the mouse clicking
    w = erelease.xdata - eclick.xdata
    h = erelease.ydata - eclick.ydata
    rect = Rectangle( (eclick.xdata, eclick.ydata), w, h, fill=False )

    # Add the rectangle to the 4th subplot
    axs[1][1].add_patch(rect)
    show()

    # Replot all of the points with those that are within the rectangle defined
    # above as "highlighted" in each subplot. Points not within any of the 
    # defined rectangles are transparent
    for i,ax in enumerate(sax):
      newx, newy = getHighlightedPoints(data[pd[i][0]], data[pd[i][1]], rect)
      # Handle the case where you are dealing with a fresh plot (all data 
      # highlighted)
      if len(ax.lines) == 1:
        ax.lines.pop()
        ax.plot(data[pd[i][0]], data[pd[i][1]], pd[i][2], alpha=0.1)
        ax.plot(newx, newy, pd[i][2], alpha=1.0)
        show()
      else:
        ax.plot(newx, newy, pd[i][2], alpha=1.0)
        show()

def toggle_selector(event):
  '''Catch key press events. If the user presses 'd' or 'D', remove the most
     recently added rectangle from the 4th subplot and unhighlight any data
     that was contained in ONLY THAT rectangle in the other 3 subplots. If
     data is contained in more than one rectangle and one of the rectangles 
     is removed, the data will remain highlighted until it is no longer within
     ANY rectangle '''
  if event.key in ['D', 'd']:
    # Check that there is something to remove
    if len(axs[1][1].patches) > 0:
      print 'Deleting previous rectangle...'
      # Remove rectangle from 4th plot
      axs[1][1].patches.pop()
      show()
      # Unhighlight data in the other three subplots
      for j,ax in enumerate(sax):
        if len(ax.lines) >= 1:
          ax.lines.pop()
          show()
        if len(ax.lines) == 1:
          ax.lines.pop()
          ax.plot(data[pd[j][0]], data[pd[j][1]], pd[j][2])
          show()
        # If there are no remaining plots in the axis object, replot the 
        # original data
        if len(ax.lines) == 0:
          ax.plot(data[pd[j][0]], data[pd[j][1]], pd[j][2])
          show()
########################### End function defn's ###############################

#### Load the data
filename = 'randomData.txt'
coord = np.dtype(dict(names=('x', 'y', 'z'), \
                      formats=('float', 'float', 'float') ) )
data = np.loadtxt(filename, dtype=coord, delimiter=',')
####

#### Initialize all the artists, containers, and other information to be used
   # in the widget
fig, axs = subplots(2,2)
   # create a tuple of the 1st 3 axes to loop over. The 4th axis contains all
   # the data and will be handled separately
sax = (axs[0][0], axs[0][1], axs[1][0])
   # Create a tuple that contains all of the plotting data for the corresponding
   # axis. E.g. axs[0][0] from sax[0] will plot 'x' vs. 'y' with blue dots and
   # be titled 'Blue Data'
pd = ( ('x','y','bo','Blue Data'), ('x','z','ro','Red Data'),\
       ('y','z','go','Green Data') )
####

#### Plot the initial data
for k,ax in enumerate(sax):
  ax.plot(data[pd[k][0]], data[pd[k][1]], pd[k][2])
  ax.set_title(pd[k][3])
axs[1][1].plot(data['x'], data['y'], 'bo', data['y'], data['z'], 'ro', \
               data['x'], data['z'], 'go' )
axs[1][1].set_title('All Data')
####

           
#### Connect and run everything
toggle_selector.RS = RectangleSelector(axs[1][1], onselect, drawtype='box')
connect('key_press_event', toggle_selector)
show()
