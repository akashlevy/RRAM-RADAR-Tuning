# Generate endurance patterns
# Creates waveform for a range of addresses being SET/RESET
# Splits into multiple patterns to save memory on the NI card
# The digipatsrc files need to be compiled with compile-pats.cmd

# Start/end address and pulse width
addri = 40000
addrf = 48192 # exclusive
pw = 200

# Number of cycles corresponding to pulse width
pwcount = pw / 20

# Do 512 addresses per waveform
for i, (startaddr, endaddr) in enumerate(zip(range(addri, addrf, 512), range(addri+512, addrf+512, 512))):
    # SET waveform
    with open('endurance-set-%s.digipatsrc' % i, 'w') as f:

        string = '''
    file_format_version 1.1;
    timeset tset0;

    pattern endurance_set (WL_SEL, BL_EN, WL_EN, BL_SEL_0, SL_SEL, addr:u)
    {'''
        for addr in range(startaddr, endaddr):
            string += '''
    repeat({pwcount})							tset0       1       0       0       0       0       .d{addr};            // set addr and hold for {pw}ns
    repeat({pwcount})							-			1		1		1		1		0		.d{addr};			 // pulse set {pw}ns
    repeat({pwcount})							-           1       0       0       0       0       .d{addr};            // set addr and hold for {pw}ns'''.format(addr=addr, pwcount=pwcount, pw=pw)
        string += '''
    halt								-			0		0		0		0		0		.d0;
    }}\n'''.format(addr=addr)
        f.write(string)

    # RESET waveform
    with open('endurance-reset-%s.digipatsrc' % i, 'w') as f:

        string = '''
    file_format_version 1.1;
    timeset tset0;

    pattern endurance_reset (WL_SEL, BL_EN, WL_EN, BL_SEL_0, SL_SEL, addr:u)
    {'''
        for addr in range(startaddr, endaddr):
            string += '''
    repeat({pwcount})							tset0       1       0       0       0       0       .d{addr};            // set addr and hold for {pw}ns
    repeat({pwcount})							-   		1		1		1		0		1		.d{addr};			 // pulse reset {pw}ns
    repeat({pwcount})							-           1       0       0       0       0       .d{addr};            // set addr and hold for {pw}ns'''.format(addr=addr, pwcount=pwcount, pw=pw)
        string += '''
    halt								-			0		0		0		0		0		.d0;
    }}\n'''.format(addr=addr)
        f.write(string)