startaddr = 0
endaddr = 1024

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
setloop{addr}:
end_loop(setloop{addr})					-			1		1		1		1		0		.d{addr};			// pulse set
repeat(5)							tset0       1       1       1       0       0       .d{addr};            // set addr and hold for 100ns'''.format(addr=addr)
    string += '''
halt								-			0		0		0		0		0		.d{addr};
}}\n'''.format(addr=addr)
    f.write(string)

with open('endurance-reset.digipatsrc', 'w') as f:

    string = '''
file_format_version 1.1;
timeset tset0;

pattern endurance_reset (WL_SEL, BL_EN, WL_EN, BL_SEL_0, SL_SEL, addr:u)
{'''
    for addr in range(startaddr, endaddr):
        string += '''
repeat(5)							tset0       1       1       1       0       0       .d{addr};            // set addr and hold for 100ns
set_loop(5)							-   		1		1		1		0		0		.d{addr};			// set_pulse_time (5*20ns)
rstloop{addr}:
end_loop(rstloop{addr})			    	-			1		1		1		0		1		.d{addr};			// pulse reset
repeat(5)							tset0       1       1       1       0       0       .d{addr};            // set addr and hold for 100ns'''.format(addr=addr)
    string += '''
halt								-			0		0		0		0		0		.d{addr};
}}\n'''.format(addr=addr)
    f.write(string)