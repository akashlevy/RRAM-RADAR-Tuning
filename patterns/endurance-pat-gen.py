for i, (startaddr, endaddr) in enumerate(zip(range(22528, 30720, 512), range(22528+512, 30729+512, 512))):
    with open('endurance-set-%s.digipatsrc' % i, 'w') as f:

        string = '''
    file_format_version 1.1;
    timeset tset0;

    pattern endurance_set (WL_SEL, BL_EN, WL_EN, BL_SEL_0, SL_SEL, addr:u)
    {'''
        for addr in range(startaddr, endaddr):
            string += '''
    repeat(5)							tset0       1       0       0       0       0       .d{addr};            // set addr and hold for 100ns
    repeat(5)							-			1		1		1		1		0		.d{addr};			 // pulse set 100ns
    repeat(5)							-           1       0       0       0       0       .d{addr};            // set addr and hold for 100ns'''.format(addr=addr)
        string += '''
    halt								-			0		0		0		0		0		.d0;
    }}\n'''.format(addr=addr)
        f.write(string)

    with open('endurance-reset-%s.digipatsrc' % i, 'w') as f:

        string = '''
    file_format_version 1.1;
    timeset tset0;

    pattern endurance_reset (WL_SEL, BL_EN, WL_EN, BL_SEL_0, SL_SEL, addr:u)
    {'''
        for addr in range(startaddr, endaddr):
            string += '''
    repeat(5)							tset0       1       0       0       0       0       .d{addr};            // set addr and hold for 100ns
    repeat(5)							-   		1		1		1		0		1		.d{addr};			 // pulse reset 100ns
    repeat(5)							-           1       0       0       0       0       .d{addr};            // set addr and hold for 100ns'''.format(addr=addr)
        string += '''
    halt								-			0		0		0		0		0		.d0;
    }}\n'''.format(addr=addr)
        f.write(string)