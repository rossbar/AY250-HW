# Import modules
import argparse

# Setup appropriate path for importing HW5 modules
import sys
sys.path.append('/home/ross/Dropbox/AY250/HW/5/')

# Import HW 5 modules
import createDatabase
import racedb as rdb

# Create parser
parser = argparse.ArgumentParser(description='Election Application')
parser.add_argument('-c', action='store', dest='candidate', \
                    help="Store the candidate's name")
parser.add_argument('-r', action='store', dest='raceName', \
                    help="Store the race name. Options are 'RepNom, RepVPNom,\
                         'PresElect'")
parser.add_argument('-d', action='store', dest='date', help='Enter the date\
                    you are interested in seeing information about.')
parser.add_argument('-p', action='store_true', default=False, dest='pltflg',\
                    help='Plots the price of the given candidate over time')
results = parser.parse_args()
