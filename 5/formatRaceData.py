import os

def stripComma( fname ):
  ifile = open( fname, 'r' )
  lines = ifile.readlines()
  ifile.close()
  
  if 'stripped' not in lines[0]:
    newlines = ['stripped']
    for line in lines:
      lline = list(line)
      lline.remove(',')
      newlines.append( ''.join(lline) )
    
    ofile = open( fname, 'w' )
    ofile.writelines( newlines )
    ofile.close()
  return

dirname = 'race_prediction_data/'
files = os.listdir( dirname )
for fname in files:
  if fname[0] != '.':
    print fname
    stripComma( dirname + fname )
