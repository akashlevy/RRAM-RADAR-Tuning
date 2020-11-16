import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt


# Load data
names = ['addr', 'pw', 'blv', 'wlv', 'ri', 'rf']
stepsize = 0.05
fname = 'data/set-sweep-wl-200ns-step-%.2f-9-21-20' % stepsize
data = pd.read_csv(fname + '.csv', delimiter='\t', names=names).to_dict('records')
for i, row in enumerate(data):
    if i != 0 and row['wlv'] == 0:
        row = data[i-1]
        while row['wlv'] < 4:
            row = row.copy()
            row['wlv'] = row['wlv'] + stepsize
            data.append(row)
        print i
data = pd.DataFrame.from_records(data, columns=names)
data.to_csv(fname + '-augment.csv', sep='\t', index=False, header=False, float_format='%g')