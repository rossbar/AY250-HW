import aifc
from scipy import *
from matplotlib.pyplot import *
import numpy as np

def getFramesAndTime(aifobj, pltflg=False):
  '''Load frame information and time data from the aif file. Return two arrays
     of ints containing the time data and the sound information (converted to
     np.uint32)'''
  frames = aifobj.readframes( aifobj.getnframes() )
  soundData = fromstring( frames, np.int32 )
  time = arange( size(soundData) ) / float( aifobj.getframerate() )
  if pltflg:
    figure()
    plot(time, soundData, 'r-')
    xlabel('Time (s)')
    ylabel('Amplitude')
    title('Sound from file (time domain)')
  return time, soundData

def truncateFreq(freq, power, maxFreq=5000):
  '''Truncate the frequency domain so that we are only looking from 0 to 5000
     Hz '''
  posMask = freq > 0
  pfreq, ppower = freq[posMask], power[posMask]
  limMask = pfreq < maxFreq
  tf, tp = pfreq[limMask], ppower[limMask]
  return tf, tp

def getFrequency(aifobj, soundData, fname, pltflg=True):
  '''Get the normalized power spectrum in the frequency domain. Takes the
     integer sound data as input and uses np.fft.fft on it (with appropriate
     shifting). Uses np.fft.fftfreq to generate the x-axis data. The power
     spectrum is calculated by abs( FT**2 ) where FT is the fourier transformed
     data. Default behavior is to plot the power spectrum '''
  FTsound = np.fft.fft( np.fft.fftshift(soundData) )
  power = abs( FTsound*FTsound )
  timestep = 1 / float( aifobj.getframerate() )
  freq = np.fft.fftfreq( len(power), d=timestep )
  freq, power = truncateFreq(freq, power)
  #normalize
  power /= power.max()
  if pltflg:
    figure()
    plot(freq, power)
    title('Normalized Power Spectrum from %s, (Frequency Domain)' %fname)
    xlabel('Frequency (Hz)')
    ylabel('Power (Normalized)')
  return freq, power

def isNear(val1, val2, cutoff):
  '''Determines whether val1 is within [val2 - cutoff, val2 + cutoff] '''
  if val1 >= val2 - cutoff and val1 <= val2 + cutoff:
    return True
  else:
    return False

def clusterData(fAry, HzCut):
  '''Cluster data from the peak finding so that like values are averaged 
     together. "Like Values" are values within HzCut of each other. Returns
     the averages of the clustered values (i.e. an estimate of the peak location
     '''
  groups = []
  group = [fAry[0]]
  i = 0
  while i < len(fAry) - 1:
    if isNear( fAry[i+1], group[-1], HzCut):
      group.append( fAry[i+1] )
    else:
      groups.append( np.array(group).mean() )
      group = [ fAry[i+1] ]
    i += 1
  groups.append( np.array(group).mean() )
  return np.array( groups )

def findPeaks(freq, power, fCut):
  maxes = freq[power > fCut]
  peaks = clusterData(maxes, 5)
  return peaks

def buildNoteDict():
  '''Uses information from the wikipedia page on the frequency of piano notes
     to build a dictionary relating frequency to the note name. Only does
     whole tones (no sharps or flats) '''
  f = open('pianoNotes.html', 'r')
  lines = f.readlines()
  f.close()
  notelines = []
  for i,line in enumerate(lines):
    if 'bgcolor' in line and 'Unicode' not in lines[i+2]:
      note = lines[i+2][4:6]
      freqline = lines[i+3]
      freq = []
      for char in freqline:
        if char.isdigit() or char == '.': freq.append(char)
      if '<' not in note:
        notelines.append( (float(''.join(freq)),note) )
  return dict(notelines)

def searchForNote(freqVal, noteDict):
  '''Given a frequency, determine whether or not there is a note in the 
     noteDict that corresponds to that frequency. '''
  flist = noteDict.keys()
  answer = None
  for val in flist:
    if isNear(freqVal, val, .03*val):
      answer = noteDict[val]
  if answer == None:
    print 'Note not Identified!'
  return answer
