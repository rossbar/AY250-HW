import aifc
from scipy import *
from matplotlib.pyplot import *
import numpy as np

topC = 4186

A4 = aifc.open('A4_PopOrgan.aif')
frames = A4.readframes(A4.getnframes())
integer_data = fromstring(frames, dtype=np.int32)
time = arange(size(integer_data)) / float( A4.getframerate() )
figure()
plot(time, integer_data, 'r-')
title('Note from file (time domain)')
# FFT
F = np.fft.fft( np.fft.fftshift(integer_data) )
power = abs(F**2)
timestep = 1/float( A4.getframerate() )
freq = np.fft.fftfreq(len(power), d=timestep)
posfreq = freq[freq > 0]
pospow = power[freq > 0]
outfreq = posfreq[posfreq < topC]
outpow = pospow[posfreq < topC]
#normalize
outpow /= outpow.max()
figure()
plot(outfreq, outpow)
title('fft')
show()
