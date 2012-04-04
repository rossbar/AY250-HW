from scipy import stats
import rejectionSample

# Use rejection sampling to estimate the Nakagami distribution with nu = 1.0.
# Note that the distribution is only defined for x > 0. The reference 
# distributin used is a gaussian centered about x = 1 with stdev = 1.
[samples, M, tAccept] = rejectionSample.rejectionSampler( \
                           '2 * 1**1 / gamma(1) * x**(2*1-1) * exp(-1.0*x**2)',\
                           'norm(1,1)', 5000, gzOnly=True )

