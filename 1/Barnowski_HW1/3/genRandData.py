import random

def generateRandomData(numRows, numCols):
  '''Generates a numRows x numCols matrix of random data in the range [0,1] in
     csv format '''
  datalines = []
  for i in range(0,numRows):
    dataline = []
    for j in range(0,numCols):
      dataline.append( str( random.random() ) )
    dataline.append('\n')
    datalines.append( ', '.join(dataline) )
  return datalines

def writeToFile(filename, data):
  '''Writes the data generated above to a file'''
  f = open( filename, 'w' )
  f.writelines(data)
  f.close()

numRows = 100 
numCols = 3
outfile = 'randomData.txt'
data = generateRandomData(numRows, numCols)
writeToFile(outfile, data)
