#!/usr/bin/env python3

"""\
Plot the growth rate of B. subtilis for different concentrations of 
theophylline.

Usage:
    theo_growth_curve.py <layout.toml> [options]

Options:
    -s --show
        Open the figures in a GUI.

    -g --gfp-only
        Only show the GFP plot.

    -o --od600-only
        Only show the OD600 plot.

    -t --t12-only
        Only show the doubling time plot.
"""

import docopt, toml
import numpy as np
import matplotlib.pyplot as plt
from color_me import ucsf
from collections import defaultdict
from scipy.optimize import curve_fit
from sgrna_sensor import plate_reader
from pathlib import Path

# expt = PerkinElmerExperiment('20180720_b_subtilis_theo_growth_curve.xlsx')
# od600 = expt.reads['absorbance_600_nm']
# gfp = expt.reads['gfp']

# I accidentally added cells to the blank wells, so I'm missing blanks.  Ugh.
# plate_layout = {
#         ('on',    '4 mM'): ['B03', 'C03', 'D03'],
#         ('on',    '2 mM'): ['B04', 'C04', 'D04'],
#         ('on',    '1 mM'): ['B05', 'C05', 'D05'],
#         ('on',  '500 µM'): ['B06', 'C06', 'D06'],
#         ('on',  '250 µM'): ['B07', 'C07', 'D07'],
#         ('on',  '125 µM'): ['B08', 'C08', 'D08'],
#         ('on',    '0 µM'): ['B09', 'C09', 'D09'],
#         ('off',   '4 mM'): ['E03', 'F03', 'G03'],
#         ('off',   '2 mM'): ['E04', 'F04', 'G04'],
#         ('off',   '1 mM'): ['E05', 'F05', 'G05'],
#         ('off', '500 µM'): ['E06', 'F06', 'G06'],
#         ('off', '250 µM'): ['E07', 'F07', 'G07'],
#         ('off', '125 µM'): ['E08', 'F08', 'G08'],
#         ('off',   '0 µM'): ['E09', 'F09', 'G09'],
# }
colors = {
        'on': ucsf.black[1],
        'off': ucsf.black[0],
        '11': ucsf.navy[0],
        '30': ucsf.teal[0],
}
formats = {
        'PerkinElmer': plate_reader.PerkinElmerExperiment,
        'Biotek': plate_reader.BiotekExperiment,
}

class TheoGrowthCurve:

    def __init__(self, layout):
        self.expt = formats[layout['format']](layout['expt'])
        self.layout = layout['layout']
        self.num_sgrnas = len(self.layout)
        self.num_conc = max(len(v) for v in self.layout.values())

        # These are calculated in `plot_od600()`, so that needs to be called 
        # before anything else.
        self.doubling_times = {
                k: defaultdict(lambda: [])
                for k in self.layout
        }

    def plot_od600(self, path=None, figsize=(12,6)):
        t_max = 300
        od600 = self.expt.reads['absorbance_600_nm']

        fig = plt.figure(figsize=figsize)
        axes = fig.subplots(
                self.num_sgrnas, self.num_conc,
                sharex=True, sharey=True,
        )

        for i in range(axes.shape[0]):
            axes[i,0].set_ylabel('OD600')
        for j in range(axes.shape[1]):
            axes[-1,j].set_xlabel('time (min)')

        for i, j, sgrna, conc, wells in self._iter_wells():
            color = colors[sgrna]
            style = dict(linestyle='none', marker='+')
            label = f'{sgrna} [{conc}]'

            ax = axes[i,j]
            ax.set_title(label)
            ax.set_xlim(0, t_max)
            ax.set_ylim(0.05, 0.20)

            for well in wells:
                df = od600[od600['well'] == well]
                t = df['minutes']
                od = df['absorbance_600_nm']

                t_fit_min = abs(df.minutes - 0).idxmin()
                t_fit_max = abs(df.minutes - 170).idxmin()

                t_fit  =  t.loc[t_fit_min:t_fit_max]
                od_fit = od.loc[t_fit_min:t_fit_max]
                t_lin  = np.linspace(0, t_max, t_max)

                p0 = 1e-3, 1/30, od.iloc[0]  # Initial guess.
                fit, cov = curve_fit(growth_curve, t_fit, od_fit, p0=p0)
                t12 = 1/fit[1]

                self.doubling_times[sgrna][conc].append(t12)

                ax.plot(
                        t_lin, growth_curve(t_lin, *fit),
                        color=color,
                        zorder=3,
                )
                ax.plot(
                        t_fit, od_fit,
                        markerfacecolor='none',
                        markeredgecolor=color,
                        zorder=4,
                        marker='o',
                        linestyle='none',
                ),
                ax.plot(
                        t, od,
                        color=color,
                        zorder=4,
                        **style,
                )
                for other_ax in axes.flat:
                    if other_ax is not ax:
                        other_ax.plot(t, od, color=ucsf.light_grey[0], zorder=1, **style)

        return self._finalize_fig(fig, path)

    def plot_t12(self, path=None):
        fig = plt.figure()
        axes = fig.subplots(1, 1)
        axes_xticks = []
        axes.set_ylabel('t½ (min)')
        x = 0

        for i, j, sgrna, conc, wells in self._iter_wells():
            label = f'[{conc}] {sgrna}'
            color = colors[sgrna]
            t12 = self.doubling_times[sgrna][conc]
            y = np.mean(t12)
            yerr = np.std(t12)
            x += 1

            axes.plot([x, x], [0, y], color=color, linewidth=5)
            axes.errorbar([x], [y], [yerr], color=color)
            axes_xticks.append((x, label))

        xticks, xticklabels = zip(*axes_xticks)
        axes.set_xticks(xticks)
        axes.set_xticklabels(xticklabels, rotation='vertical')
        axes.set_xlim(xticks[0] - 0.5, xticks[-1] + 0.5)

        return self._finalize_fig(fig, path)

    def plot_gfp(self, path=None, figsize=(12,3)):
        gfp = self.expt.reads['gfp']

        fig = plt.figure(figsize=(12,3))
        axes = fig.subplots(1, self.num_conc, sharex=True, sharey=True)
        axes[0].set_ylabel('GFP (RFU)')
        for ax in axes:
            ax.set_xlabel('time (min)')
    
        for i, j, sgrna, conc, wells in self._iter_wells():
            ax = axes[j]
            ax.set_title(f'[{conc}]')
            ax.set_xlim(0, 600)
            ax.set_ylim(15000, 40000)

            for k, well in enumerate(wells):
                df = gfp[gfp['well'] == well]
                ax.plot(
                        df.minutes, df.gfp,
                        color=colors[sgrna],
                        label=sgrna if j == 0 and k == 0 else '_nolabel_',
                )

        axes[0].legend(loc='upper left')
        return self._finalize_fig(fig, path)

    def _iter_wells(self):
        for i, sgrna in enumerate(self.layout):
            for j, conc in enumerate(self.layout[sgrna]):
                yield i, j, sgrna, conc, self.layout[sgrna][conc]

    def _finalize_fig(self, fig, path):
        fig.tight_layout()
        if path: fig.savefig(path)
        return fig

def growth_curve(t, *fit):
    return fit[0] * 2**(fit[1] * t) + fit[2]


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    in_path = args['<layout.toml>']
    out_path = Path(in_path).stem
    layout = toml.load(in_path)
    analyst = TheoGrowthCurve(layout)

    if not args['--gfp-only'] and not args['--t12-only']:
        analyst.plot_od600(f'./{out_path}_od600.svg')
    if not args['--gfp-only'] and not args['--od600-only']:
        analyst.plot_t12(  f'./{out_path}_t12.svg')
    if not args['--od600-only'] and not args['--t12-only']:
        analyst.plot_gfp(  f'./{out_path}_gfp.svg')

    if args['--show']:
        plt.show()

