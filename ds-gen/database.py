import statistics

class Database(object):

        def __init__(self):
                self.data = []  # list of measurements from simulations
                self.tom = {}   # table of measurements - info on measurement units, etc
                self.toc = {}   # table of cases - values of params in each case
                self.waveforms = {} # [testbench][case]

        def record(self, datum):
                """ Add an entry to the results database """
                self.data.append(datum)

        def dump(self, hDAT):
                """ Write out the database to a file """
                for entry in self.data:
                        hDAT.write('{}\n'.format(entry))

        def values(self, measure):
                return [ a[2] for a in self.data if a[1] == measure ]


        def load(self, hDAT):
                """ Read in data from a file """
                for line in hDAT:
                        line = line.strip()
                        line = line[1:-1]
                        bits = line.split(',')
                        case = int(bits[0])
                        measure = bits[1].strip()
                        measure = measure.replace("'",'')
                        value = float(bits[2])
                        self.data.append([case, measure, value])

        def stats(self, measure):
                """ Calc stats for the given measure """
                values = self.values(measure)
                stats = {}
                stats['measure'] = measure
                stats['min'] = min(values)
                stats['max'] = max(values)
                stats['mean'] = statistics.mean(values)
                return stats

