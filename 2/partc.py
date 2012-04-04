from scipy import stats
import rejectionSample

# Calculate the samples according to the student t dist. with 2 deg. of 
# freedom
[samples, M, tAccept] = rejectionSample.rejectionSampler( \
                                         '(1/2.0)*exp(-abs(x))', 't(2)', 1000 )

# Use the ks test to test the samples for goodness of fit with the true
# laplacian distribution
(s, p) = stats.kstest(samples, 'laplace')
print '''The p-value from the k-s test of the rejection samples versus the 
       laplace distribution was: %s ''' %(p)

# Compare the acceptance rate to that of partb
[samples, M, cauchyAccept] = rejectionSample.rejectionSampler( \
                   '(1/2.0)*exp(-abs(x))', 'cauchy', 1000, verbose=False )

print '''The proportion accepted using the cauchy reference distribution: %s\nThe proportion accepted using the t(2) reference distribution: %s\n%s higher portion of samples were accepted from the t(2) reference ''' \
%(cauchyAccept, tAccept, abs(tAccept - cauchyAccept))
