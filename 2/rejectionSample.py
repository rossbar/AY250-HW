from scipy import stats
from matplotlib import pyplot as plt
import numpy as np
from math import *

def rejectionSampler( tDist, refName, nSamp, verbose=True, gzOnly=False ):
  '''Given a target distribution (tDist) and a reference distribution, this 
     function generates a list of samples from the target distribution using
     rejection sampling from the reference distribution. The verbose flag
     determines whether the distributions are plotted and the sample output is
     made visible (default behavior = ON). The gzOnly flag is for distributions
     that are only defined for x >= 0 (default behavior = OFF)

     Note: The tDist must be 1-D with ind. var. x. Other distribution 
     parameters must be hard-coded in tDist. 

     e.g. '(1/(2*b))*exp(-abs(x-u)/b)' with u = 0 and b = 1 should be written:
          '(1/(2*1))*exp(-abs(x-0)/1)' '''

#### Evaluate function input. Use try/except statements to notify the user if 
   # They made an error typing in the function or entering the reference
   # distribution name

  # Get the target distribution as a string and create a function target(x) out
  # of it. 
  numTries = 2
  while numTries > 0:
    try:
      target = lambda x: eval(tDist)
      target(0)
      break
    except (NameError, ValueError):
      print '''Warning: the tDist you entered was not a valid function.'''
      tDist = raw_input('Please try again, q to quit: ')
      if tDist == 'q':
        return
      numTries -= 1
    
  
  # Get the reference distribution and assign it to the variable ref.
  numTries = 2
  while numTries > 0:
    rname = 'stats.distributions.' + refName
    try:
      ref = eval(rname)
      break
    except AttributeError:
      print '''Warning: the name you entered is not the name of a valid 
               distribution in stats.distributions.'''
      refName = raw_input('Please try again, q to quit : ')
      if refName == 'q':
        return
      numTries -= 1
####

#### Initialize the problem

  # Set the boundaries to be 3*std of the reference distribution (encompassing
  # 99.7% of the pdf, in the case of a gaussian)
  if ref.std() < 2:
    xl = -3*ref.std()	
    xr = 3*ref.std()
  else:
    xl = -5
    xr = 5
  if gzOnly:
    xl = 0
  x = np.linspace(xl, xr)
  ytar = [target(n) for n in x]
  yref = ref.pdf(x)
  # Visualize the distributions
  if verbose:
    fig, (ax1, ax2) = plt.subplots(1,2,sharey=True)
    ax1.plot( x, ytar )
    ax1.set_title('Target Distribution')
    ax2.plot( x, yref )
    ax2.set_title('Reference Distribution (Before Scaling)')
####

#### Find an M such that M*g(x) > f(x) for all x
  truthVal = 0
  M = 1.0
  eps = .0000000001
  # Note: The default behavior here is to linearly increase M until the
  # criterion is met. Note that this may converge extremely slowly if the 
  # target distribution >> reference distribution on [xl, xr].
  while truthVal < 1.0 - eps:
    M += 0.1
    g_x = yref
    f_x = ytar
    compare = f_x < M*g_x
    truthVal = compare.mean()
  if verbose:
    print 'M = %s satisfies the condition that f(x) < M*g(x) for x in [%s, %s]'\
         %(M, xl, xr)
####

#### Do the rejection sampling
  samples = []
  numAttempts = 0
  while len(samples) < nSamp:
    xc = ref.rvs()
    u = stats.uniform.rvs()
    f = target(xc)
    g = ref.pdf(xc) 
    if u < (f/(M*g)):
      samples.append(xc)
      if verbose:
        print 'Sample #: %s' %(len(samples))
    numAttempts += 1
####

  # Spit out info
  if verbose:
    print 'M = ', str(M)
    print 'Proportion Accepted = %s in %s total attempts' %(len(samples)\
         /float(numAttempts), numAttempts)

  # visualize the samples
  if verbose:
    plt.figure()
    plt.hist(samples, 50, (xl, xr), normed=True)
    plt.plot(x,ytar,label='Target Distribution')
    plt.title('Histogram of Results from Rejection Sampling Algorithm')
    plt.xlabel('x')
    plt.ylabel('# samples')
    plt.legend()

  # Return the desired values
  return samples, M, len(samples)/float(numAttempts)
