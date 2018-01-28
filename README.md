Testbenches for Analog Blocks
==========================================

Purpose
-------------------------------------------

I want a set of tests so I can set up testbenches quickly to
easily compare different architectures/sizings of the basic
analog building blocks.

There are a few aspects to this then:
1. basic testbench setup
2. datasheet generation
3. comparason of datasheets


I dunno. there's so many different things. comparators with hyst, without
latched. etc. Is this mad?

Output
--------------------------------------------
An [example of the output](doc/cmos_24p2-ds/cmos_24p2-ds.html) can be found
in the `doc/cmos_24p2-ds/` directory.


Design
--------------------------------------------

The initial design is NGSPICE, Python and TOML.

Each type of design, for example op-amp or comparator, has a python script
to launch sims. This requires that the design under test (DUT) is wrapped
in, for example `opampwrapper.sp` so that the testbench knows which nodes
to connect to.

The design has a TOML file to specify supply voltages and path to things.

It's set up so that a single test can be run from the workarea directly if
things need debugging.

Each design type has a `testbench`.
Each `testbench` has one or more `sims`.
Each `sim` has one or more `measures`.


Datasheet
-----------------------------------------------

Open Questions
* HTML with graphs and measurements?
* CVS file with raw data?
* How do I collate the results from multiple sims?


Regressions
------------------------------------------------
How do I run a regression?

Maybe the easiest thing is just to write out loads of directories with the
files?

Q: What do I need to specify a sweep?
 1. The testbench to use
 2. Each variable

Q: How do I specify what to sweep?
A: In the TOML file?

    [multicase.pvt]
    var1 = ["P", "slow", "fast", "nominal"]
    var2 = ["V", 0.9, 1.0, 1.1]
    var3 = ["T", 0, 25, 125]

Would create a regression with 3x3x3 = 27 simulations.

Values verses ranges with stepsize?

Say I want to run the above, but have only three sims? Set?

Python would:

    for analysis in config['multicase']:
        for var in analysis.values():


    [multicase.pvt]
      label = "PVT Analysis of offset or something"
      testbench = ""
      measures = [ "offset", "input_range" ]
      [multicase.pvt.var1]
        label = "P"
        var = "library"
        list = ["slow", "fast", "nominal"]
      [multicase.pvt.var2]
        label = "V"
        var = "vdd"
        range = [0.9, 1.1, 0.05]
      [multicase.pvt.var3]
        label = "T"
        var = "tdegc"
    	list = [0, 25, 125]


    [multicase.trim]
      label = "PSSR at corners"
      testbench = ""
      measures = [ "psrr+", "pssr-" ]

      [multicase.trim.var1]
        label = "P"
        var = "library"
        list = ["slow", "fast", "nominal"]
        set = 0

      [multicase.trim.var2]
        label = "V"
        var = "vdd"
        range = [0.9, 1.1, 0.05]

      [multicase.trim.var3]
        label = "T"
        var = "tdegc"
    	list = [0, 25, 125]

      [multicase.trim.var4]
        label = "Trim Setting"
        var = "trim"
    	list = [4, 23, '0x34']
        set = 0


Still only 27 sims - trim setting moves with the process setting.



### Limits

The toplevel `testbench.toml` for a design should be able to specify limits
for each measurement.

Need to be able to list what measurements are taken:

    opamp --measures

To update the .toml file automatically?

    opamp --limits <measure> --max <> --min <>


### PVT



### Monte-Carlo



