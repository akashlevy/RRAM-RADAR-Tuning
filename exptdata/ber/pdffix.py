for fname in ['figs/dualplotboth.pdf']:
    with open(fname, 'rb') as infile:
        data = infile.read()
        newdata = data.replace(b'NimbusRomNo9L-Regu', b'Times')
    with open(fname, 'wb') as outfile:
        outfile.write(newdata)