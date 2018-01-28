""" 
"""

import os

import toml

spice_template = """* {TITLE}

* Setup
.param vdd={VDD}
.param vss={VSS}
.param rload={RLOAD}
.param cload={CLOAD}

* send params to the .control section
.csparam vdd={{vdd}}
.csparam vss={{vss}}

.option TEMP={TDEGC}

.lib '{LIBPATH}' {LIBNAME}

* Op-Amp Sub-circuit
.include '{LAUNCHDIR}/opampwrapper.sp'

* Analysis
.include '{SCRIPTDIR}/{DECK}'

"""


class Testbench(object):

    def __init__(self, config, name):

        self.config = config
        self.name = name

        self.launchdir = os.getcwd()
        self.scriptdir = self._scriptdir()
        toml_filename = os.path.join( self.scriptdir, name, name + '.toml')
        print("[TOML]", toml_filename)
        self.simcfg = toml.load( toml_filename )
        self.simdir = os.path.join(
            self.config['circuit']['workdir'],
            self.config['circuit']['name'],
            name )
        self.cktfile = os.path.join( self.launchdir, config['circuit']['spice'])


    def _scriptdir(self):
        scriptpath = os.path.realpath(__file__)
        scriptdir = os.path.dirname(scriptpath)
        scriptdir = os.path.dirname(scriptdir)
        scriptdir = os.path.join(scriptdir, self.config['circuit']['design'])
        return scriptdir


    def setup(self, case_parameters=None):
        """ Write SPICE files needed for the simulation """
        #print '[SETUP] ' + self.simcfg['label']
        
        if case_parameters == None:
                params = {}
                params['case'] = 'c0000'
                params['corner'] = self.config['parameters']['corner']
                params['vdd'] = self.config['parameters']['vdd']
                params['vss'] = self.config['parameters']['vss']
                params['rload'] = self.config['parameters']['rload']
                params['cload'] = self.config['parameters']['cload']
                params['tdegc'] = self.config['parameters']['tdegc']
        else:
            params = case_parameters

        corner = params['corner']
        libname = self.config['techlib']['corners'][corner]
        libpath = self.config['techlib']['path']
        libpath = libpath.replace('${USER}', os.environ['USER'])
        libpath = os.path.join(libpath, libname + '.lib')

        sub_dict = {
            'TITLE': self.simcfg['label'],
            'DECK': self.simcfg['deck'],
            'LIBPATH': libpath,
            'LIBNAME': libname,
            'SCRIPTDIR': os.path.join( self.scriptdir, self.name),
            'LAUNCHDIR': self.launchdir,
            'VDD': params['vdd'],
            'VSS': params['vss'],
            'RLOAD': params['rload'],
            'CLOAD': params['cload'],
            'TDEGC': params['tdegc'],
        }

        hSPICE = open( os.path.join( self.simdir, params['case'], 'go.sp'), 'w' )
        hSPICE.write( spice_template.format(**sub_dict) )

        hSPICE.write("\n* Sub-circuits\n")
        hSPICE.write(".include '{}'\n".format(self.cktfile) )
        for inc in self.config['circuit']['includes']:
            inc = inc.replace("${USER}", os.environ['USER'])
            hSPICE.write( ".include '{}'\n".format(inc) )

        hSPICE.close()


    def runcmd(self):
        return ['ngspice', '-b', 'go.sp', '-r', 'plot.dat', '-o', 'spice.log']


    def extract(self, case='c0000'):
        """ Read the log file, and extract the measurements from it. """

        # expect that measurements have '[MEASURE]' in the spice log file
        measurelines = []
        hLOG = open( os.path.join(self.simdir, case, 'spice.log') )
        for line in hLOG:
            if line.find('[MEASURE]') >= 0:
                measurelines.append(line)
        hLOG.close()

        # some measurements don't have units
        measures = []
        for m in measurelines:
            bits = m.split(':')

            unit = ''
            if len(bits) == 5:
                unit = bits[4].strip()

            value = float('inf')
            try:
                value = float(bits[3])
            except(ValueError):
                pass

            measure = [ bits[1].strip(), bits[2].strip(), value, unit ] 
            measures.append( measure )

        return measures


    def list(self):
        txt = []
        txt.append('[TESTCASE] ' + self.simcfg['label'])
        for meas in list(self.simcfg['measures'].values()):
            txt.append('  [MEASURE] ' + meas['label'] )

        return '\n'.join(txt)

