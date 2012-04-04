import identifyNotes
import aifc
from matplotlib.pyplot import *
import numpy as np
from os import listdir

# Generate note dictionary
noteDict = identifyNotes.buildNoteDict()
# Get files to operate on
dirname = 'sound_files'
soundfiles = listdir(dirname)

for fname in soundfiles:
  # Open file
  fn = aifc.open(dirname + '/' + fname)
  
  # Get normalized power spectrum in frequency domain
  time, sound = identifyNotes.getFramesAndTime(fn)
  freq, power = identifyNotes.getFrequency(fn, sound, fname)
  # Threshold for peak identification. Default behavior = 20x baseline
  fcut = 20*abs(np.mean(power[3580:3620]))
  # Find peaks in the spectrum
  freqMaxes = identifyNotes.findPeaks(freq, power, fcut)
  
  notesFound = []
  # For each peak, match the frequency to a note
  for val in freqMaxes:
    note = identifyNotes.searchForNote(val, noteDict)
    if note not in notesFound:
      notesFound.append(note)
  
  print 'The file   %s    was found to contain these notes:' %fname
  print notesFound
  show()
