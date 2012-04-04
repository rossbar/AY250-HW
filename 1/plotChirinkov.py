from chirinkov import generateChirinkovMap
import matplotlib.pyplot as plt

ax = []
ks = [.5, .75, .9, 1]
for i,k in enumerate(ks):
  ax.append( generateChirinkovMap(k, 20, 10000) )
