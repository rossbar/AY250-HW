import urllib

# This script goes to momswhothink.com and looks at the lists of the top 100
# baby names from each decade from 1880 til today. Each unique name is then 
# stored in either 'MaleNames.txt' or 'FemaleNames.txt'.

baseURL = '''http://www.momswhothink.com/baby-names/top-100-baby-names-for-the-'''
endURL = 's.html'

years = range(1880,2010,10)
boyList = []
girlList = []
for year in years:
  fullURL = baseURL + str(year) + endURL
  handle = urllib.urlopen(fullURL)
  lines = handle.readlines()

  for i,line in enumerate(lines):
    if "<td>" in line and "</td>" in line:
      line = line.strip()
      val = line[4]
      if val.isdigit():
        boy = lines[i+1]
        boy = boy.strip()
        boy = boy[4:-5] + '\n'
        if ( boy not in boyList ) and ('<' not in boy ):
          boyList.append(boy)
        girl = lines[i+2]
        girl = girl.strip()
        girl = girl[4:-5] + '\n'
        if ( girl not in girlList ) and ('<' not in girl ):
          girlList.append(girl)

  print "Now accessing names from %s" %(year)

b = open('MaleNames.txt', 'w')
b.writelines(boyList)
b.close()

g = open('FemaleNames.txt','w')
g.writelines(girlList)
g.close()

print "Obtained %s boy names and %s girl names" %( len(boyList), len(girlList))
