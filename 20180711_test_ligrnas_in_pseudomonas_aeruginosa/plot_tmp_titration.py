#!/usr/bin/env python3

"""\
Plot plate reader data titrating TMP in order to determine its MIC in different 
conditions.

Usage:
    plot_tmp_titration.py <toml> [options]

Arguments:
    <toml>
        A TOML-formatted file describing the plate-layout.

Options:
    -o --output PATH
        The path to save the resulting plot.  The extension determines the file 
        format.  If "$" is present in the path,. it will be replaced with the 
        name of the given TOML file (minus the extension).

    -x --explicit-controls
        Show separate plots for the controls.  Without this, the positive and 
        negative controls can't be distinguished expect by how they look.  So 
        if you're not sure the controls worked, use this option.
"""

import docopt
import pandas as pd
from pathlib import Path
from matplotlib import pyplot as plt
from sgrna_sensor import plate, plate_reader, style
from sgrna_sensor.style import pick_style

def load_data(toml_path):
    meta = plate.load_plate(toml_path)
    expt = plate_reader.BiotekExperiment(meta['paths']['default'])
    layout = pd.DataFrame(meta['well']).T

    df = expt.kinetic[600]
    df = df.merge(layout, left_on='well', right_index=True)
    return df

def plot_data(df, explicit_controls=True):
    tmp_concs = df.groupby(['tmp_ug_mL'])

    fig, axes = plt.subplots(
            len(tmp_concs), 4 if explicit_controls else 2,
            sharex=True, sharey=True,
            figsize=(8.5 if explicit_controls else 6, 11),
    )

    def plot_growth_curves(ax, df, sgrnas):
        df_sgrnas = df[df.sgrna.isin(sgrnas)]

        for key, sele in df_sgrnas.groupby(['sgrna', 'theo_mM']):
            sgrna, theo_mM = key
            style = pick_style(sgrna, theo_mM, color_controls=True)
            ax.semilogy(sele.minutes/60, sele.read, **style)

    y_labels = []
    if explicit_controls:
        x_labels = 'on', 'off', 'rxb 11,1', 'mhf 30'
    else:
        x_labels = 'rxb 11,1', 'mhf 30'

    for i, (key, group) in enumerate(tmp_concs):
        y_labels.append(key)
        if explicit_controls:
            plot_growth_curves(axes[i,0], group, ['on'])
            plot_growth_curves(axes[i,1], group, ['off'])
            plot_growth_curves(axes[i,2], group, ['on', 'off', 'rxb/11/1'])
            plot_growth_curves(axes[i,3], group, ['on', 'off', 'mhf/30'])
        else:
            plot_growth_curves(axes[i,0], group, ['on', 'off', 'rxb/11/1'])
            plot_growth_curves(axes[i,1], group, ['on', 'off', 'mhf/30'])
    
    for i, ax in enumerate(axes[0,:]):
        ax.set_title(x_labels[i])
    for ax in axes[-1,:]:
        ax.set_xlabel('time [hr]')
        ax.set_xlim(0, 24)
        ax.set_xticks(range(0, 25, 4))
    for i, ax in enumerate(axes[:,0]):
        ax.set_ylim(df.read.min(), max(1, df.read.max()))
        ax.set_ylabel(f'[TMP]\n{y_labels[i]} µg/mL\n\nOD600')

    fig.tight_layout()

if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    toml = Path(args['<toml>'])
    df = load_data(toml)
    plot_data(df, args['--explicit-controls'])

    if args['--output']:
        plt.savefig(args['--output'].replace('$', toml.stem))
    else:
        plt.show()



