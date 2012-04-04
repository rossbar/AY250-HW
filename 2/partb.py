from scipy import stats
import rejectionSample

# Generate samples using the rejection scheme with the cauchy as a reference
[samples, M, proportion] = rejectionSample.rejectionSampler( \
                           '(1/2.0)*exp(-abs(x))', 'cauchy', 1000 )

# Perform the Kolmogorov-Smirinov test
(s, p) = stats.kstest(samples, 'laplace')
print '''The p-value from the k-s test of the rejection samples versus the 
       laplace distribution was: %s ''' %(p)
