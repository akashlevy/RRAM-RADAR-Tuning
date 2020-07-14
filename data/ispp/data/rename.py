import os
from glob import glob

for i, fname in enumerate(sorted(glob('*.csv.*'))):
    vwl = (i+1)*0.005
    os.rename(fname, "ispp-wl%.3f-7-13-20.csv" % vwl)