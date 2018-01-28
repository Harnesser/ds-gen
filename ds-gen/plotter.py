import os

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

class Plotter(object):

	def __init__(self, database_handle):
		self.dbh = database_handle
		self.outdir = "./"

	
	def plot(self, pltdfn, tbname):
		if pltdfn['plot_style'] == 'overlay':
			self._plot_overlay(pltdfn, tbname)
		elif pltdfn['plot_style'] == 'stack':
			self._plot_stack(pltdfn, tbname)


	def _plot_stack(self, pltdfn, tbname):
		print(' [STACK]', pltdfn['label'])

		num_subplots = len( pltdfn['waveforms'] )

		fig = Figure()
		FigureCanvas(fig)
		for sp in range(num_subplots):

			# stuff to plot
			dbhw = self.dbh.waveforms[tbname]
			waveforms = pltdfn['waveforms'][sp].split(';')

			# set up the plot
			fig.suptitle(pltdfn.get('label',''))
			ax = fig.add_subplot(num_subplots, 1, sp+1)
			ax.set_xscale(pltdfn.get('xscale', 'linear'))
			ax.set_yscale(pltdfn.get('yscale', 'linear'))
			ax.grid(True)


			# set title, axis labels and units from 1st waveform
			wv1name = pltdfn['waveforms'][sp].split(';')[0]
			wv1db = dbhw[0][wv1name]

			xlabel = "{} ({})".format(
					wv1db['indep'].get('label','?'),
					wv1db['indep'].get('unit', ''))
			ax.set_xlabel(xlabel)

			ylabel = "{} ({})".format(
					wv1db['dep'].get('label','?'),
					wv1db['dep'].get('unit', ''))
			ax.set_ylabel(ylabel)


			# Scientific notation
			# live with 'sci' for now, 'eng' if upgrading matplotlib
			# Filtering units don't want this for phase
			if wv1db['dep'].get('unit','') in ['V', 'A']:
				ax.ticklabel_format(axis='y', style='sci', scilimits=(-2,2))


			for c in range( len(dbhw) ):
				for wv in waveforms:
					indep = dbhw[c][wv]['indep']['data']
					dep = dbhw[c][wv]['dep']['data']
					ax.plot(indep, dep)

		name = self.filenamer('waveforms', tbname, pltdfn['label'])
		fig.savefig( os.path.join(self.outdir, name) )


	def _plot_overlay(self, pltdfn, tbname):
		print(' [OVERLAY]', pltdfn['label'])

		fig = Figure()
		FigureCanvas(fig)
	
		# hack, cos I copied from __plot_stack()
		num_subplots = 1
		sp = 0

		# stuff to plot
		dbhw = self.dbh.waveforms[tbname]
		waveforms = pltdfn['waveforms'][sp].split(';')

		# set up the plot
		fig.suptitle(pltdfn.get('label',''))
		ax = fig.add_subplot(num_subplots, 1, sp+1)
		ax.set_xscale(pltdfn.get('xscale', 'linear'))
		ax.set_yscale(pltdfn.get('yscale', 'linear'))
		ax.grid(True)


		# set title, axis labels and units from 1st waveform
		wv1name = pltdfn['waveforms'][sp].split(';')[0]
		wv1db = dbhw[0][wv1name]

		xlabel = "{} ({})".format(
				wv1db['indep'].get('label','?'),
				wv1db['indep'].get('unit', ''))
		ax.set_xlabel(xlabel)

		ylabel = "{} ({})".format(
				wv1db['dep'].get('label','?'),
				wv1db['dep'].get('unit', ''))
		ax.set_ylabel(ylabel)


		# Scientific notation
		# live with 'sci' for now, 'eng' if upgrading matplotlib
		# Filtering units don't want this for phase
		if wv1db['dep'].get('unit','') in ['V', 'A']:
			ax.ticklabel_format(axis='y', style='sci', scilimits=(-2,2))


		for c in range( len(dbhw) ):
			for wv in pltdfn['waveforms']:
				indep = dbhw[c][wv]['indep']['data']
				dep = dbhw[c][wv]['dep']['data']
				ax.plot(indep, dep)

		name = self.filenamer('waveforms', tbname, pltdfn['label'])
		fig.savefig( os.path.join(self.outdir, name) )


	def filenamer(self, prefix, tbname, label):
		name = '__'.join([prefix, tbname, label])
		name = name.replace('(','_')
		name = name.replace(')','_')
		name = name.replace(' ','_')
		return name

	
	def histogram(self, histdfn, tbname):
		""" Plot all the measures in a barchart. """
		measures = histdfn['measures']
		print(' [HISTOGRAM]', measures)

		fig = Figure()
		FigureCanvas(fig)

		minfo = self.dbh.tom[ measures[0] ]

		# set up the plot
		fig.suptitle(histdfn.get('label',''))
		ax = fig.add_subplot(1,1,1)
		ax.set_xscale(histdfn.get('xscale', 'linear'))
		ax.set_yscale(histdfn.get('yscale', 'linear'))
		ax.grid(True)


		# set title, axis labels and units from 1st waveform
		xlabel = " ({})".format( minfo.get('unit', '') )
		ax.set_xlabel(xlabel)

		ylabel = "Count"
		ax.set_ylabel(ylabel)


		# https://matplotlib.org/devdocs/api/_as_gen/matplotlib.axes.Axes.hist.html#matplotlib.axes.Axes.hist
		dat = []
		for m in measures:
			dat.append( self.dbh.values(m) )
		ax.hist(dat)

		name = self.filenamer('measures', tbname, histdfn['label'])
		fig.savefig( os.path.join(self.outdir, name) )
