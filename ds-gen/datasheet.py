""" Datasheet

Collate all the results and datasheet pages into a full datasheet
for the sims run.

Output is in markdown.

"""

import os
import markdown

html_header = """<!DOCTYPE html>
<meta name=viewport content="width=device-width, initial-scale=1">
<meta charset=utf-8>
<style type="text/css">
  body {
    max-width: 800px;
    margin: auto;
    line-height:1.6;
    font-size:18px;
    color:#444;
    padding:0
  }
  th, td {
    border-bottom: 1px solid #ddd;
  }
  tr:nth-child(even) {
    background-color: #f2f2f2;
  }
  table {
    width: 100%;
  }
  th {
    text-align: left;
  }
</style>

"""

html_footer = """ """

class Datasheet(object):

    def __init__(self, dbh):
        self.dbh = dbh
        self.table_headings = ['Measurement', 'Min.', 'Avg.', 'Max.', 'Unit']
        self.links = []

    def table_heading(self):
        md = [" "]
        md.append('| ' + ' | '.join(self.table_headings) + ' |')
        md.append('| ' + ' | '.join(['---'] * len(self.table_headings)) + ' |')
        return md

    def measurement_table(self, tbname, with_links=False, with_heading=True):
        """ Write out the measurement table for a given testbench.

        If no regression is run, then max and min values are '--'
        """
        md = []
        if with_heading:
            md.extend( self.table_heading() )

        for msmnt in self.dbh.tom.values():
            if msmnt['testbench'] != tbname:
                continue

            mmin = msmnt.get('min', '--')
            if mmin != '--':
                mmin = '{:0.3}'.format(mmin)

            mmax = msmnt.get('max', '--')
            if mmax != '--':
                mmax = '{:0.3}'.format(mmax)

            mavg = '{:0.3}'.format(msmnt['mean'])

            # if a front-page list, make the label clickable
            if with_links:
                link_text = msmnt['label']
                link_ref = msmnt['name']
                link_path = '{}/{}-ds.html#{}'.format(tbname, tbname, link_ref) 
                self.links.append( [link_text, link_ref, link_path] )
                label = '[{}][{}]'.format(msmnt['label'], msmnt['name'])
            else:
                label = msmnt['label']

            table_data = [
                label,
                mmin,
                mavg,
                mmax,
                msmnt['unit'],
            ]
            md.append('| ' + ' | '.join( table_data ) + ' |')

        return '\n'.join(md)


    def link_defs(self):
        """ """
        md = ["  "]

        # links
        for (link_text, link_ref, link_path) in self.links:
            md.append('   [{}]: {} "{}"'
                .format(link_ref, link_path, link_text)
            )

        return md


    def to_html(self, mdfile):
        """ Convert a Markdown file to HTML5 """
        md = open(mdfile, 'r').read()
        body = markdown.markdown(
            md,
            extensions=['markdown.extensions.tables'],
            output_format="html5",
        )
        html = [html_header, body, html_footer]

        htmlfilename = os.path.splitext(mdfile)[0] + '.html'
        hHTML = open(htmlfilename, 'w')
        hHTML.write('\n'.join(html))
        hHTML.close()

# vim: tabstop=4 softtabstop=4 shiftwidth=4 expandtab
