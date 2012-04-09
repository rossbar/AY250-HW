Files included:
- ElectionPrediction.py: Main. To be run from the command line
- gitlog.txt - "Answer" to HW question 2
- race_prediction_data - Folder containing newest race prediction data. The 
  prediction data for "any other candidate" was removed because it threw errors
  when used with the HW 5 wiki-scrape code
- states.txt - text file with info pertinent to the wiki scraping (copied from
  HW 5 directory)

Dependencies:
ElectionPrediction.py automatically adjusts the sys.path to include '../5/' so
the code from HW 5 (will only work with the code I wrote, not the solutions)
must be in the directory above. If you get this assignment from cloning the 
git repository on github, this should automatically work.

To Run:

In the directory that contains ElectionPrediction.py, type the following on the
command line:

usr@computer:/$ python ElectionPrediction.py -c cand_name -r race_name -d date
(in mm-dd-yyyy format) -p

cand_name, race_name, and date are all required (although they have default 
values set, so it will still run if you provide nothing). The -p option is the
plot flag: default is no plotting. add -p to include a plot of price over time.

Notes:
 - I added a couple functions to my HW 5 code to extract the price (HW 5 wanted
   more complicated metrics like market efficiency), so the code must be run
   with an up-to-date version of HW 5. 
 - I did not adjust any of the existing code for HW 5, so the database is still
   created in RAM, i.e. the database is created each time you run from the cmd
   prompt. While inconvenient at run-time, I didn't want to rewrite the code
   in HW 5.
