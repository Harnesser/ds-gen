import itertools
import pprint as pp

class Regression(object):

    def __init__(self, config, regrdfn):
        self.config = config
        self.stuff = regrdfn
        self.table = {}
        self.labels = {}
        self.base_case = self._base_case()
        self.N = 0


    def _base_case(self):
        base_case = {}
        base_case['case'] = 'c0000'
        base_case['corner'] = self.config['parameters']['corner']
        base_case['vdd'] = self.config['parameters']['vdd']
        base_case['vss'] = self.config['parameters']['vss']
        base_case['rload'] = self.config['parameters']['rload']
        base_case['cload'] = self.config['parameters']['cload']
        base_case['tdegc'] = self.config['parameters']['tdegc']
        return base_case


    def build_table(self):
        self.N = 1
        parms = []
        self.labels = []
        # https://stackoverflow.com/questions/798854/all-combinations-of-a-list-of-lists
        vars = self.stuff['vars']
        for var in vars:
            self.labels.append(var)
            self.N *= len( vars[var]['list'] )
            parms.append( vars[var]['list'])
        print("Total number of cases:", self.N)

        self.table = list(itertools.product(*parms))
        self.list()


    def build_case(self, case=0):
        params = dict( self.base_case )
        params['case'] = 'c{:04}'.format(case)
        for (i, label) in enumerate(self.labels):
            params[label] = self.table[case][i]
        return params


    def list(self):
        print(self.labels)
        pp.pprint( self.table )


    def report_config(self):
        """ Return markdown table of the parameters of the regression """
        headings = ['Parameter', 'Values']
        md = [" "]
        md.append('\n## Regression: {}\n\n'.format(self.stuff['label']))
        md.append('Number of testcases: {}\n\n'.format(self.N))

        # Table heading
        md.append('| ' + ' | '.join(headings) + ' |')
        md.append('| ' + ' | '.join(['---']*len(headings)) + ' |')

        # Table data rows
        for var in self.stuff['vars'].values():
            row = []
            row.append(var['label'])
            try:
                row.append('; '.join(var['list']))
            except(TypeError):
                row.append('; '.join( [str(a) for a in var['list']] ) )
            md.append('| ' + ' | '.join(row) + ' |')

        return md

# vim: tabstop=4 softtabstop=4 shiftwidth=4 expandtab

