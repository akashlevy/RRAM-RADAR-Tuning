import numpy as np, matplotlib.pyplot as plt, matplotlib as mpl

ranges = ['10-20', '20-40', '40-60', '60-80', '80-100'] #, '100-120']

# LaTEX quality figures 
mpl.rcParams.update(
    {
    'text.usetex': True,
    'pgf.texsystem': 'lualatex',
    'pgf.rcfonts': True,
    }
)
plt.rc('font', family='serif', serif='Times')

start_pts = []
end_pts = []
for r in ranges:
    data = np.swapaxes(np.loadtxt('ret/ret_' + r + '.csv')[:128,6:],0,1)
    print(data)

    start_pts += list(data[0])
    end_pts += list(data[-1])

    plt.figure(figsize=(4, 3))
    plt.title('Resistance Relaxation')
    plt.xlabel('Read Number')
    plt.ylabel('Resistance ($\\Omega$)')
    plt.plot(data)
    plt.tight_layout()
    plt.savefig('figs/' + r + '_relax.pdf')

    plt.figure(figsize=(4, 3))
    plt.title('Mean Resistance')
    plt.xlabel('Read Number')
    plt.ylabel('Mean Resistance ($\\Omega$)')
    plt.plot(data.mean(axis=1))
    plt.tight_layout()
    plt.savefig('figs/' + r + '_mean.pdf')

    plt.figure(figsize=(4, 3))
    plt.title('Stdev Resistance')
    plt.xlabel('Read Number')
    plt.ylabel('Stdev Resistance ($\\Omega$)')
    plt.plot(data.std(axis=1))
    plt.tight_layout()
    plt.savefig('figs/' + r + '_std.pdf')

plt.figure(figsize=(4, 3))
plt.title('Initial to Final Resistance Scatter Plot')
plt.xlabel('Initial Resistance ($\\Omega$)')
plt.ylabel('Final Resistance ($\\Omega$)')
plt.plot(start_pts, end_pts, '.')
plt.tight_layout()
plt.savefig('figs/scatter.pdf')
        