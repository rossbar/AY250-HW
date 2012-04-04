import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

# Load the data
filename = 'randomData.txt'
coord = np.dtype(dict(names=('x', 'y', 'z'), \
                      formats=('float', 'float', 'float') ) )
data = np.loadtxt(filename, dtype=coord, delimiter=',')

# create the subplots
fig, axs = plt.subplots(2,2)
axs[0][0].plot(data['x'], data['y'], 'bo')
axs[0][0].set_title('Blue Data')
axs[0][1].plot(data['x'], data['z'], 'ro')
axs[0][1].set_title('Red Data')
axs[1][0].plot(data['y'], data['z'], 'go')
axs[1][0].set_title('Green Data')
axs[1][1].plot(data['x'], data['y'], 'bo', data['y'], data['z'], 'ro', \
               data['x'], data['z'], 'go' )
axs[1][1].set_title('All Data')

# First attempt at adding a rectangle
# rect = Rectangle( (.219,.223), .3, .3, fill=False)
# axs[1][1].add_patch(rect)
# fig.canvas.draw()

# Write functions to do the point highlighting stuff
def isInRect( x, y, rect ):
  xl, yl = rect.get_xy()
  w, h = rect.get_width(), rect.get_height()
#  print 'X and Y:', x, y
#  print 'Xbounds:', xl, xl+abs(w)
#  print 'Ybounds:', yl, yl+abs(h)
  xl, xh = min(xl, xl+w), max(xl, xl+w)
  yl, yh = min(yl, yl+h), max(yl, yl+h)
  # ONLY WORKS IF DRAG FROM LOWER LEFT TO UPPER RIGHT!
  if ( x >= xl and x <= xh ) and ( y >= yl and y <= yh ):
    return True
  else:
    return False

def getHighlightedPoints(xdata, ydata, rect):
  xout = []
  yout = []
  for i in range(0,len(xdata)):
    if isInRect(xdata[i], ydata[i], rect):
      xout.append(xdata[i])
      yout.append(ydata[i])
  return xout, yout



# Try the rectangle drawing widget stuff
from matplotlib.widgets import RectangleSelector
from pylab import *
from matplotlib.patches import Rectangle

def onselect(eclick, erelease):
  'eclick and erelease are matplotlib events at press and release'
  print ' startposition : (%f, %f)' % (eclick.xdata, eclick.ydata)
  print ' endposition   : (%f, %f)' % (erelease.xdata, erelease.ydata)
#  print ' used button   : ', eclick.button
  w = erelease.xdata - eclick.xdata
  h = erelease.ydata - eclick.ydata
  rect = Rectangle( (eclick.xdata, eclick.ydata), w, h, fill=False )
  axs[1][1].add_patch(rect)
  show()
  # try the point occlusion thing
  newx, newy = getHighlightedPoints(data['x'], data['y'], rect)
  if len(axs[0][0].lines) == 1:
    axs[0][0].lines.pop()
    axs[0][0].plot(data['x'], data['y'], 'bo', alpha=0.1)
#  print newx, newy
    axs[0][0].plot(newx, newy, 'bo', alpha=1.0)
    show()
  else:
    axs[0][0].plot(newx, newy, 'bo', alpha=1.0)
    show()

def toggle_selector(event):
    print ' Key pressed.'
    if event.key in ['Q', 'q'] and toggle_selector.RS.active:
        print ' RectangleSelector deactivated.'
        toggle_selector.RS.set_active(False)
    if event.key in ['A', 'a'] and not toggle_selector.RS.active:
        print ' RectangleSelector activated.'
        toggle_selector.RS.set_active(True)
    if event.key in ['D', 'd']:
        if len(axs[1][1].patches) > 0:
          print 'Deleting previous rectangle'
          axs[1][1].patches.pop()
          show()
          if len(axs[0][0].lines) >= 1:
            print len(axs[0][0].lines)
            axs[0][0].lines.pop()
            show()
#          else:
#            axs[0][0].lines.pop()
#            axs[0][0].lines.pop()
          if len(axs[0][0].lines) == 1:
            axs[0][0].lines.pop()
            axs[0][0].plot(data['x'], data['y'], 'bo')
            show()
          if len(axs[0][0].lines) == 0:
            axs[0][0].plot(data['x'], data['y'], 'bo')
            show()
           

toggle_selector.RS = RectangleSelector(axs[1][1], onselect, drawtype='box')
connect('key_press_event', toggle_selector)
show()
