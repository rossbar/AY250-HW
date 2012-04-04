Included Files:
createDatabase.py
  - Creates a database in RAM with 2 tables: one named 'predictions' and one 
    names 'candidates'. The tables contain the following info:
  pred: candidate id, race id, day, price, volume
  cand: candidate id, birthday, town, rep. state, part affiliation
parte.py
  - Contains the code for the Mason Dixon part of the assignment. Cannot be run
    unless createDatabase has already been run
partf.py
  - Contains the code for determining market inefficiency. Also cannot be run
    without the database.
racedb.py
  - Module containing functions relevant to creating and mining the database
scrapeWiki.py
  - Module containing functions relevant to scraping wikipedia for candidate 
    data
states.txt
  - Text file containing some information about each of the 50 states. This
    file is used by some of the routines and must be present in the working
    directory. The data is tab-delimited with 4 cols where the columns are:
      state name, state cap., state nickname, isAboveMDLine
    The last column determines whether the state is above or below the MD line.
    For states that are partly above or below the MD line, this metric is
    determined by whether or not the most populous areas of the state are
    above or below the MD line. For instance, California is 'below' the MD line
    while Illinois is 'Above' (because of Chicago)

To create the database with 2 tables named 'candidates' and 'predicitions'.

In [1]: run createDatabase

IMPORTANT: The folder contianing the race prediction data called 
           race_prediction_data/ must be contained in the working directory.
           RUNNING createDatabase WILL RE-FORMAT SOME OF THE DATA IN THE race_
           prediction_data DIRECTORY, SO MAKE SURE YOU UNZIP A FRESH VERSION
           WHEN YOU GO TO GRADE THE NEXT ASSIGNMENT!

Note: - This step needs to be done first before parts e and f can be answered. 
      - Reading wikipedia has timed out before. If you get a URLError, just
        run it again.
      - Can take several minutes to complete depending on the speed of your
        internet connection.
      - Database is created in RAM so make sure you have enough available
        (never had a problem on my home computer, but I have 8Gb)
      - The database can be accessed by a cursor object called cursor

To run part e:

In [2]: import parte
In [3]: parte.predictMasonDixon( cursor )

Note: - Whether or not a state is above the Mason Dixon line was determined by
        eye using google maps. For states that lie above and below it, I 
        decided that whatever part was more populous was the part that I would
        consider. The only state that was tricky based on this criterion was
        ohio, which I considered to be below the MD Line
      - Takes about 5-10 seconds to run

To run part f:

In [4]: import partf
In [5]: partf.getInefficiency( cursor, refDate )

Note: - Takes a little longer to run, about 15-20 seconds
      - prints and returns the date where the efficiency is not within a
        threshhold value of the expected efficiency (100%)
      - The default threshhold value is 8%

Other Notes:
 - The wikipedia scraping was difficult because the format is very different 
   between different pages. Using BeautifulSoup was more difficult than brute
   force due to the different formats of the pages, so it was not used in the
   end. The wikipedia scraping functions manage to fill the requested info
   about the given candidates with ~90-95% accuracy.
