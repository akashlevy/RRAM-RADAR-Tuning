# Import libraries
import math, re
import matplotlib as mpl, matplotlib.pyplot as plt, numpy as np, pandas as pd


# LaTEX quality figures 
mpl.rcParams.update(
    {
    'text.usetex': True,
    'pgf.texsystem': 'lualatex',
    'pgf.rcfonts': True
    }
)
plt.rc('font', family='serif', serif='Times', size=13)

# Trip points for SET/RESET
SET_VOLTAGE = 0.75
RESET_VOLTAGE = -2

# SET (True) or RESET (False)
SET = True
TRIP_POINT = SET_VOLTAGE if SET else RESET_VOLTAGE

# Regex for extracting Vbl/Vsl and resistor value
colre = re.compile('/Vdr \(V.l.vdc=([^,]*),R0.r=([^)]*)\) Y')

# Load data and clean up columns (remove repeated X cols and rename to Vwl)
data = pd.read_csv('sim-results-set.csv') if SET else pd.read_csv('sim-results-reset.csv')
data.rename(columns={'/Vdr (Vbl.vdc=0,R0.r=1000) X': 'Vwl', '/Vdr (Vsl.vdc=0,R0.r=1000) X': 'Vwl'}, inplace=True)
droplist = [i for i in data.columns if i.endswith('X')]
data.drop(droplist, axis=1, inplace=True)

# Restructure the data
columns = ['Vwl', 'Vbl', 'Vsl', 'R', 'Vr']
data2 = []
for column in data.columns[1:]:
    if SET:
        (Vbl, R), Vsl = tuple(float(x) for x in colre.match(column).groups()), 0
    else:
        (Vsl, R), Vbl = tuple(float(x) for x in colre.match(column).groups()), 0
    data[column] = Vbl - data[column]
    for Vwl, Vr in zip(data['Vwl'], data[column]):
        data2.append([Vwl, Vbl, Vsl, R, Vr])
data = pd.DataFrame(data2, columns=columns)

# Change R to kOhm
data['R'] = data['R']/1000

# Compute gradients
knob = 'Vbl' if SET else 'Vsl'
gdata = data.groupby([knob, 'R'])
data['dVr/dVwl'] = gdata['Vr'].transform(pd.Series.diff)/gdata['Vwl'].transform(pd.Series.diff)
gdata = data.groupby(['Vwl', 'R'])
data['dVr/d{knob}'.format(knob=knob)] = gdata['Vr'].transform(pd.Series.diff)/gdata[knob].transform(pd.Series.diff)
data.fillna(0, inplace=True)

# Setup figure
plt.figure(figsize=(4,2.5))

# Find nearest point to the trip point
pd.set_option('display.max_rows', None)
neardata = data[np.abs(data['Vbl'] - 2) < 1e-5] if SET else data[np.abs(data['Vsl'] - 2.8) < 1e-5]
neardata['tripdist'] = np.abs(neardata['Vr']-TRIP_POINT)
indices = neardata.groupby('R')['tripdist'].transform('idxmin')
neardata = neardata.loc[indices].drop_duplicates()
neardata.plot('R', 'dVr/dVwl', ax=plt.gca(), marker='.')
print(neardata)

neardata = data[np.abs(data['Vwl'] - 3) < 1e-5] if SET else data[np.abs(data['Vwl'] - 3.5) < 1e-5]
neardata['tripdist'] = np.abs(neardata['Vr']-TRIP_POINT)
indices = neardata.groupby('R')['tripdist'].transform('idxmin')
neardata = neardata.loc[indices].drop_duplicates()
neardata.plot('R', 'dVr/d{knob}'.format(knob=knob), ax=plt.gca(), marker='.')
print(neardata)

plt.xlabel('$R$ (k$\\Omega$)')
plt.ylabel('Voltage Gain')
plt.tight_layout()
plt.show()