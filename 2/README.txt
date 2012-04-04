1a)

The rejection sampler is contained in the rejectionSample.py module. The 
function takes the following input:
 - The target distribution, entered as a string
 - The name of the reference distribution
 	- Note: The function searches for the distribution in 
 	  scipy.stats.distributions by default, so only the name (and any 
          input parameters) are required (DO NOT prepend the
          scipy.stats part).
 - The number of samples
The function returns the accepted samples, the value of M that was used (having
been determined by the algorithm) and the proportion of samples that were
accepted.

NOTES:
 - The target distribution must be 1-D with ind. var. x. Other distribution
   parameters must be hard-coded in tDist. For instance:
 
   '(1/(2*b))*exp(-abs(x-u)/b)' with u = 0 and b = 1 should be written:
   '(1/(2*1.0))*exp(-abs(x-0)/1.0)'
 - When entering numeric values in the target distribution, be sure to enter
   them as floats so that the correct form of division is used; i.e. use 
   '(1/2.)' instead of (1/2)

iPython example:

In [1]: import rejectionSample
In [2]: (samples, M, propAccept) = rejectionSample.rejectionSampler( \
        '(1/2.0)*exp( -abs(x) )', 'norm(0,1)', 1000 )
        # This uses the standard normal distribution for reference and the
        # laplacian with hard-coded values of mu = 0 and b = 1.0.

1b) This part uses the rejection sampler described above as well as some 
additional tools from scipy.stats such as kstest.

To run:
In [1]: import partb

The script in partb calls the rejection sampler with the arguments:
[samples, M, proportion] = rejectionSample.rejectionSampler( \
                           '(1/2.0)*exp(-abs(x))', 'cauchy', 1000 )

1c) Same as part b except this time the reference distribution is 't(2)'. 

To run:
In [1]: import partc

1d) The rejection sampler is used with the 1-D Nakagami distribution as the 
target continuous distribution and the gaussian centered about x=1 with stdev=1
as the reference.

To run:
In [1]: import partd
