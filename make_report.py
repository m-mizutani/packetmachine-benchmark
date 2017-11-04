#!/usr/bin/env python

# import matplotlib.pyplot as plt
import json
import collections
import pprint
from bokeh.io import show, output_file, save
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.transform import factor_cmap
from bokeh.palettes import Spectral6
from bokeh.models import PrintfTickFormatter


def main():
    basis = json.load(open('./base.json', 'rt'))
    results = json.load(open('./results.json', 'rt'))
    targets = ['PacketMachine', 'libtins', 'GoPacket']
    task_name = {
        'task1': 'Task1: Count number of TCP port 80 packet',
        'task2': 'Task2: Count number of new TCP session',
        'task3': 'Task2: Count number of DNS query with ".google."',
    }
    for task_label, res_set in results.items():
        data = {}
        ds_names = list(res_set.keys())

        for dname in ds_names:
            pkt_count = basis['dataset'][dname]['count']
            res = res_set[dname]
            for pf, values in res.items():
                data[(dname, pf)] = (float(pkt_count) / float(min(values))) * 1000

        src = [(d, l, v) for (d, l), v in data.items()]
        x = [(s[0], s[1]) for s in src]
        counts = [s[2] for s in src]

        source = ColumnDataSource(data=dict(x=x, counts=counts))

        p = figure(x_range=FactorRange(*x), title=task_name[task_label],
                   toolbar_location=None, tools="")
        p.vbar(x='x', top='counts', width=0.9, source=source, line_color="white",
               fill_color=factor_cmap('x', palette=Spectral6, factors=targets,
                                      start=1, end=2))
        p.y_range.start = 0
        p.x_range.range_padding = 0.1
        p.xaxis.major_label_orientation = 1
        p.xgrid.grid_line_color = None
        p.yaxis.axis_label = 'PPS (Packet Per Second)'
        p.xaxis.axis_label = 'Dataset'
        p.yaxis[0].formatter = PrintfTickFormatter(format="%5f K")

        output_file('{}.html'.format(task_label))
        save(p)

        


if __name__ == '__main__': main()
