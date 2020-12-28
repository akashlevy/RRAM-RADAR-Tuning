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
knob = 'Vbl' if SET else 'Vsl'

# Regex for extracting Vbl/Vsl and resistor value
colre = re.compile('/Vdr \(V.l.vdc=([^,]*),R0.r=([^)]*)\) Y') if SET else re.compile('/Vdr \(R0.r=([^)]*),V.l.vdc=([^,]*)\) Y')

# Load data and clean up columns (remove repeated X cols and rename to Vwl)
data = pd.read_csv('sim-results-set.csv') if SET else pd.read_csv('sim-results-reset.csv')
data.rename(columns={data.columns[0]: 'Vwl'}, inplace=True)
droplist = [i for i in data.columns if i.endswith('X')]
data.drop(droplist, axis=1, inplace=True)

# Restructure the data
columns = ['Vwl', 'Vbl', 'Vsl', 'R', 'Vr']
data2 = []
for column in data.columns[1:]:
    if SET:
        (Vbl, R), Vsl = tuple(float(x) for x in colre.match(column).groups()), 0
    else:
        (R, Vsl), Vbl = tuple(float(x) for x in colre.match(column).groups()), 0
    data[column] = Vbl - data[column]
    for Vwl, Vr in zip(data['Vwl'], data[column]):
        data2.append([Vwl, Vbl, Vsl, R, Vr])
data = pd.DataFrame(data2, columns=columns)

# Change R to kOhm
data['R'] = data['R']/1000

# Compute gradients
data = data.sort_values([knob, 'R', 'Vwl'], kind='mergesort')
gdata = data.groupby(['R', knob])
data['dVr/dVwl'] = gdata['Vr'].transform(pd.Series.diff)/0.01

gdata = data.groupby(['R', 'Vwl'])
data['dVr/d{knob}'.format(knob=knob)] = gdata['Vr'].transform(pd.Series.diff)/0.01
data.fillna(0, inplace=True)

# Setup figure
plt.figure(figsize=(4,2.5))

# Find nearest point to the trip point
pd.set_option('display.max_rows', None)
#data = data[data['Vwl'] <= 3]
data['tripdist'] = np.abs(data['Vr']-TRIP_POINT)
indices = data.groupby(['Vwl','R'])['tripdist'].transform('idxmin')
neardata = data.loc[indices].drop_duplicates()
selection = (np.abs(neardata['Vwl'] - 2) < 1e-5) & (np.abs(neardata['R'] - 4) < 1e-5)
selection |= (np.abs(neardata['Vwl'] - 1.86) < 1e-5) & (np.abs(neardata['R'] - 4.555) < 1e-5)
selection |= (np.abs(neardata['Vwl'] - 1.68) < 1e-5) & (np.abs(neardata['R'] - 5.063) < 1e-5)
selection |= (np.abs(neardata['Vwl'] - 1.52) < 1e-5) & (np.abs(neardata['R'] - 5.7) < 1e-5)
selection |= (np.abs(neardata['Vwl'] - 1.39) < 1e-5) & (np.abs(neardata['R'] - 6.547) < 1e-5)
selection |= (np.abs(neardata['Vwl'] - 1.27) < 1e-5) & (np.abs(neardata['R'] - 7.788) < 1e-5)
selection |= (np.abs(neardata['Vwl'] - 1.17) < 1e-5) & (np.abs(neardata['R'] - 11.67) < 1e-5)
neardata = neardata[selection].sort_values('R')

print(neardata)
neardata.plot('R', ['dVr/dVwl', 'dVr/d{knob}'.format(knob=knob)], ax=plt.gca(), marker='.')

plt.xlabel('$R$ (k$\\Omega$)')
plt.ylabel('Voltage Gain')
plt.tight_layout()
plt.show()