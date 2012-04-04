1) Chirikov Maps

The function generates 4 chirikov maps with different values for kicker 
intensity and plots them in the same subwindow. To use:

In [1]: from chirikov import generateChirikovMaps
In [2]: kvals = (.5, .75, .95, 1.0) # Make a tuple with 4 floats - these values
				    # work nicely
In [3]: generateChirikovMaps(kvals, 20, 10000)

# numInits should be at least 10. The higher this value, the more detailed
# the structure of the map
# numParticles should be at least 5000. 10000 works nicely. More than that 
# slows the algorithm down and may cause memory issues; values > 10000 are
# really not necessary

Warning: If running on computer with <8GB of ram, you may run into memory issues
if you run with >10000 particles

2) part2.py

In ipython:
In [1]: import part2

If you want to run it again after it has been imported already:
In [2]: reload(part2)

3) Brushing

This loads the file randomData.txt which is made by genRandData.py. The default
is 100 randomly generated values. You can change this by going into 
genRandData and changing numRows to a different number. numCols must be left =
3 otherwise the brushing code will fail when trying to load the data.

The brushing works like this: There are 4 subplots. The first 3 correspond to 
x vs y, y vs z, and x vs z (where x y and z are the 3 cols loaded from 
randomData.txt). The lower right subplot plots all of the data on the same 
pair of axes. 
You can then highlight data in the 4th subplot by clicking and dragging a 
rectangle within the axes. This will cause a rectangle to appear in the 4th
plot and the corresponding data points within the rectangle to be highlighted 
in the other 3.
You can add as many rectangles in this way as you want. Note that if a data 
point is contained in more than one rectangle, it will remain highlighted until
it is no longer contained in any rectangle.
Press d or D to delete the most recently added rectangle, and un-highlight the
data points that were contained ONLY in that rectangle
If the click or the release occurs anywhere outside of the bounds of the 4th 
subplot, nothing happens

In ipython:
In [1]: run brush
