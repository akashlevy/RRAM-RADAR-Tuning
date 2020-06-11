startaddr = 0
endaddr = 2048

with open('endurance-set.digipatsrc', 'w') as f:

    string = '''
file_format_version 1.1;
timeset tset0;

pattern endurance_set (WL_SEL, BL_EN, WL_EN, BL_SEL_0, SL_SEL, addr:u)
{'''
    for addr in range(startaddr, endaddr):
        string += '''
repeat(5)							tset0       1       1       1       0       0       .d{addr};            // set addr and hold for 100ns
set_loop(5)							-			1		1		1		0		0		.d{addr};			// set_pulse_time (5*20ns)
setloop:
end_loop(setloop)					-			1		1		1		1		0		.d{addr};			// pulse set'''.format(addr=addr)
    string += '''
halt								-			0		0		0		0		0		.d{addr};
}}\n'''.format(addr=addr)
    f.write(string)

with open('endurance-set.digipatsrc', 'w') as f:

    string = '''
file_format_version 1.1;
timeset tset0;

pattern endurance_set (WL_SEL, BL_EN, WL_EN, BL_SEL_0, SL_SEL, addr:u)
{'''
    for addr in range(startaddr, endaddr):
        string += '''
repeat(5)							tset0       1       1       1       0       0       .d{addr};            // set addr and hold for 100ns
set_loop(5)							-   		1		1		1		0		0		.d{addr};			// set_pulse_time (5*20ns)
rstloop:
end_loop(rstloop)					-			1		1		1		0		1		.d{addr};			// pulse reset'''.format(addr=addr)
    string += '''
halt								-			0		0		0		0		0		.d{addr};
}}\n'''.format(addr=addr)
    f.write(string)