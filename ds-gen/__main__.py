""" Operational Amplifier Characterisation SPICE Simulations.

Usage:
    opamp datasheet [--regression=REGR] [--analyse] [--cleanall] [--debug] [--list] [--cleanall] --cfg=FILE
    opamp bench BENCH [--regression=REGR] [--analyse] [--clean] [--list] --cfg=FILE
    opamp --cleanall --cfg=FILE
    opamp -h | --help | --version

Actions:
    datasheet           Generate a full datasheet for the design
    bench BENCH         Run just a single testbench 

Options:
    --cfg=FILE          The TOML configuartion file specifying the design
    --list              Show what testcases and measurements are available. No runs.
    --debug             Print extra debug info for this command
    --cleanall          Delete the work directory

"""

import os
import sys
import subprocess
import pprint as pp

import toml
import docopt

import testbench
import regression
import database
import plotter
import datasheet

arguments = docopt.docopt(__doc__, version='0.0.1')
config = toml.load( arguments['--cfg'] )
regressions = toml.load('regressions.toml')
regressions = regressions['regressions']
designtype = config['circuit']['design'] 

if arguments['--debug']:
    pp.pprint(arguments)
    pp.pprint(config)


# Prepare the working directory
designdir = os.path.join( config['circuit']['workdir'], config['circuit']['name'] )
if arguments['--cleanall']:
    subprocess.check_output(['rm', '-rf', designdir ])


launchdir = os.getcwd()
scriptpath = os.path.realpath(__file__)
scriptdir = os.path.dirname(scriptpath)
scriptdir = os.path.dirname(scriptdir)
scriptdir = os.path.join(scriptdir, designtype)

def run_spice(testbench, case='c0000'):

    os.chdir( os.path.join(testbench.simdir, case) )

    # Call NGSPICE
    # https://sourceforge.net/p/ngspice/ngspice/ci/KLU-3-try-to-rebase/tree/BUGS 
    print("[SPICE] " + testbench.simcfg['label'])
    try:
        output = subprocess.check_output(
            testbench.runcmd(),
            stderr=subprocess.STDOUT)
    except (subprocess.CalledProcessError):
        print("oops")

    os.chdir(launchdir)


N = 1
regr = None
if arguments['--regression']:
    print('[REGRESSION]')
    if arguments['--list']:
        for regrdfn in regressions.values():
            print('[REGRESSION] {}'.format(regrdfn['label']))
            regr = regression.Regression(config, regrdfn)
            regr.build_table()
        sys.exit(0)

    # if we're not listing regressions, select the one to run
    regrdfn = regressions[ arguments['--regression'] ]
    regr = regression.Regression(config, regrdfn)
    regr.build_table()
    N = regr.N


if arguments['datasheet']:
    print('[DATASHEET]')

db = database.Database()

# find what we've got
tb_used = []

tbcfg = toml.load( os.path.join( scriptdir, designtype + '.toml') )
for tbname in tbcfg['benches']:

    tb_enable = arguments['datasheet'] or ( arguments['BENCH'] == tbname )
    if not tb_enable:
        continue

    tb = testbench.Testbench(config, tbname)
    if arguments['--list']:
        print(tb.list())
        continue

    tb_used.append(tb)

    if arguments['--analyse']:
        continue

    for case in range(N):
        casename = 'c{:04}'.format(case)
        simdir = os.path.join(tb.simdir, casename)
        subprocess.check_output(['mkdir', '-p', simdir ])

        params = None
        if regr:
            params = regr.build_case(case)
            print('[CASE-{:04}] {}'.format(case, list(params.values())))

        tb.setup(params)
        run_spice(tb, casename)
        measures = tb.extract(casename)
        for m in measures:
                print('  [MEASURE] {:<30} : {:12} {:<5}'.format(m[1], m[2], m[3]))
                db.record( [case, m[0], m[2]] )

if arguments['--list']:
    sys.exit()


if not arguments['--analyse']:
    if N > 1:
        hDAT = open( os.path.join(designdir, 'results.db'), 'w')
        db.dump(hDAT)
        hDAT.close()
else:
    hDAT = open( os.path.join(designdir, 'results.db'), 'r')
    db.load(hDAT)
    hDAT.close()


artist = None

if N > 1:
    measure_info = {}
    for tb in tb_used:
        for m in tb.simcfg['measures']:
            m_info = {}
            m_info['name'] = m
            m_info['testbench'] = tb.name
            m_info['unit'] = tb.simcfg['measures'][m]['unit']
            m_info['label'] = tb.simcfg['measures'][m]['label']

            m_info.update( db.stats(m) )
            #pp.pprint(m_info)
            measure_info[m] = m_info

    # atm, these aren't serialised to the database file
    db.tom = measure_info
    db.toc = regr.table

    # draw some charts
    artist = plotter.Plotter(db)
    for tb in tb_used:
        print('[DISTRIBUTIONS]', tb.name)
        for histdfn in tb.simcfg.get('histograms', {}).values():
            artist.outdir = tb.simdir
            artist.histogram(histdfn, tb.name)


def slurp_data(tbsimdir, case):
    filename = os.path.join( tbsimdir, 'c{:04}'.format(case), 'plot.data')
    data = []
    hDAT = open(filename, 'r')
    for line in hDAT:
        dataline = [ float(a) for a in line.split() ]
        data.append(dataline)
    hDAT.close()

    # transpose the data
    # https://stackoverflow.com/a/6473724
    return list(map(list, zip(*data)))


# load waveform data
for tb in tb_used:
    print('[DATABASE]', tb.name)
    wvinfo = tb.simcfg['waveforms']
    keys = [int(a) for a in wvinfo.keys()]
    keys.sort()

    db.waveforms[tb.name] = {}

    for case in range(N):
        #print('  [CASE]', case)
        spice_data = slurp_data(tb.simdir, case)

        db.waveforms[tb.name][case] = {}

        for wvi in keys:
            #print(  '[WAVE]', wvi)
            wvis = str(wvi)

            indep = {
                'label': wvinfo[wvis]['indep']['label'],
                'unit': wvinfo[wvis]['indep']['unit'],
                'data': spice_data[wvi*2]
            }
            dep = {
                'label': wvinfo[wvis]['dep']['label'],
                'unit': wvinfo[wvis]['dep']['unit'],
                'data': spice_data[wvi*2+1]
            }

            waveform = {
                'indep': indep,
                'dep': dep,
            }

            db.waveforms[tb.name][case][dep['label']] = waveform


# do the plots
if not artist:
    artist = plotter.Plotter(db)


for tb in tb_used:
    for pltdfn in tb.simcfg['plots'].values():
        artist.outdir = tb.simdir
        artist.plot(pltdfn, tb.name)



# write the datasheet markdown
mdfiles = []

cktname = config['circuit']['name']
dsdir = os.path.join(designdir, "{}-ds".format(cktname))

subprocess.check_output(['rm', '-rf', dsdir ])
os.makedirs(dsdir)

ds = datasheet.Datasheet(db)

dsfilename = os.path.join(dsdir, "{}-ds.md". format(cktname))
mdfiles.append(dsfilename)
hDS = open(dsfilename, 'w' )
hDS.write("# Datasheet for `{}`\n".format(cktname))

hDS.write('## Measurements\n')
hDS.write('\n'.join( ds.table_heading()) )
hDS.write('\n')


for tb in tb_used:

    # Measurement table
    hDS.write( ds.measurement_table(tb.name, with_links=True, with_heading=False) + '\n')

    # Write testbench page
    os.makedirs( os.path.join(dsdir, tb.name) )
    pagefilename = os.path.join(dsdir, tb.name, '{}-ds.md'.format(tb.name))
    mdfiles.append(pagefilename)
    hDSP = open(pagefilename, 'w')

    hDSP.write("# Testbench Results for `{}`\n".format(cktname))
    hDSP.write("\n##Measurements")
    hDSP.write( ds.measurement_table(tb.name, with_links=False) + '\n')

    hDSP.write('\n##Plots\n')
    for pltdfn in tb.simcfg['plots'].values():
        plot_label = pltdfn['label']
        filename = artist.filenamer('waveforms', tb.name, plot_label)

        # copy plot so we can link relatively
        fullpath = os.path.join(tb.simdir, filename+'.png')
        destpath = os.path.join(dsdir, tb.name)
        subprocess.check_output(['cp', fullpath, destpath])

        hDSP.write('\n### {}\n'.format(plot_label))
        hDSP.write('![{}]({})\n'.format(plot_label, filename+'.png'))

    if N > 1:
        hDSP.write('\n##Distributions\n')
        for histdfn in tb.simcfg.get('histograms', {}).values():
            hist_label = histdfn['label']

            filename = artist.filenamer('measures', tb.name, hist_label)

            # copy plot so we can link relatively
            fullpath = os.path.join(tb.simdir, filename+'.png')
            destpath = os.path.join(dsdir, tb.name)
            subprocess.check_output(['cp', fullpath, destpath])

            hDSP.write('\n### {}\n'.format(hist_label))
            hDSP.write('![{}]({})\n'.format(hist_label, filename+'.png'))

    hDSP.close()

if N > 1:
    hDS.write('\n'.join(regr.report_config()) + '\n')


# Configuration
hDS.write('\n## Configuration\n')


# Links
hDS.write( '\n'.join(ds.link_defs() ))

hDS.close()


# convert everything to HTML
for mdfile in mdfiles:
    ds.to_html(mdfile)


# vim: tabstop=4 softtabstop=4 shiftwidth=4 expandtab

