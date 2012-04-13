Included Files:
- dartEstimator.py: Contains all the functions associated with the throwing of
  darts and estimating Pi for all three methods (serial, multiproc, ipy-par).
- evaluateMethods.py: Evaluation script for running all three methods and 
  producing the plot requested by the homework.
- results.png: Example output of the evaluateMethods.py script when run on my
  work computer.

To run (linux instructions only):

1) Before opening an ipython interpreter, open a terminal and type:
   "ipcluster start --n=#" where # is the number of cores you wish to use (must
   be <= to the number of cores available on your machine).
2) Open an ipython interpreter

In [1]: run evaluateMethods.py

Notes:
- Depending on the #/speed of the processors, evaluateMethods.py may take a 
  while to run (e.g. it takes ~15 seconds for the serial method with 10^7 darts,  about 30s total on my lab computer (2.4 GHz i7))
- If you forget to start the ipcluster machinery, the script will fail. I have 
  experienced 2 different errors: an AssertionError and a TimeoutError. A catch
  has been included for the AssertionError but not the TimeoutError (which is 
  not the proper format to be recognized by except). Either way, the program
  will exit. Go to step 1 of the above instructions then try again.
- When producing the plot on whatever machine you are running, the title will
  not include the processor configuration unless you add it to the 
  evaluateMethods.py file yourself (I couldn't find any pythonic way to easily
  get the type and speed of the system processor. I tried the platform module, 
  but it gave me mostly garbage).
Observations:
- From results.png, the parallel methods don't become faster until about 10^4
  darts are run. This is due to the overhead involved in setting up the 
  parallel machinery. As the number of darts increases and the solution time
  becomes dominated by the dart-throwing algorithm itself, the parallel 
  implementations converge to an execution rate about 6x faster than the
  serial implementation. 
