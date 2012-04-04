Included Files:
 - imageModifier.py
	Contains the functions for modifying a loaded numpy image
 - imageSearch.py
	Contains the function for searching the web for an image. Relies on 
	pybing and a bing API developer key (stored in internetSearch.py)
 - mpl_figure_editor
	Third-party code written to generate a trait editor for a matplotlib
	figure object
 - internetSearch.py
	Main file. Creates the gui.

To Run:

In [1]: run internetSearch.py

This opens the gui, from here:

1) Enter a search term in the 'Query' box
2) When you are satisfied, click the 'Search button'
3) When the image is loaded, manipulate it with the 4 bottom buttons to your
   heart's content. The 'Revert button' redraws the original image.
4) To close the gui, click the 'x' in the window manager.

Notes:  No special error catching has been included in the web-searching so it
	may fail, but this will not crash the gui (you will just see the error
	message in the terminal). 
	- 2 such errors have been experienced:
	  1) IOError: timeout - if your search term is obscure or spelled 
             incorrectly, you may get a timeout from pybing. Either try again
             or modify the search term and try again
          2) IOError: unrecognized filetype. If the first image that the search
             pulls happens to be of a file type that the Image module of the 
             PIL doesn't understand, you may see this error. Modify the search
             term and try again (or go to the imageSearch.py file and change 
             the image index to <n> to get the (n-1)th image (default is 0).
	The image rotation function may take a couple seconds depending on the
        size of the image.
