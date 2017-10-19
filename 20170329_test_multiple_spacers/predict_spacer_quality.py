#!/usr/bin/env python3

"""
Usage:
   predict_spacer_quality.py [options]
   predict_spacer_quality.py <spacer> <design> [options]

Options:
    -a --algorithm <name>     [default: mfe]
        Specify which algorithm to use to score the interaction between the 
        spacer and the aptamer.  Valid options are:

        mfe:
            Calculate the minimum free energy (MFE), only considering intra- 
            chain base-pairs.
        mfe-dimer:
            Calculate the minimum free energy (MFE), considering intra- and 
            inter-chain base-pairs.
        pf-dimer:
            Calculate the partition function normalized free energy (MFE), 
            considering intra- and inter-chain base-pairs.

    -m --max-change
        Plot the maximum change in cleavage, rather than the average change.  
        The maximum change might better reflect the true activity of the 
        sensors, because the assay is very sensitive to conditions (the age of 
        the Cas9 in particular).  So the maximum represents the most ideal 
        conditions.

    -A --aptamer-only
        Only consider interactions between the spacer and the aptamer, exclude 
        the linker sequences that were found during screening.
"""

import sys
import docopt
import RNA
import sgrna_sensor
import numpy as np
import matplotlib.pyplot as plt

from sgrna_sensor import densiometry
from scipy.stats import linregress
from color_me import ucsf

args = docopt.docopt(__doc__)

if args['--aptamer-only']:
    inserts = {
            'rxb 11,1': 'AUACCAGCCGAAAGGCCCUUGGCAG',
            'mhf 30': 'AUACCAGCCGAAAGGCCCUUGGCAG'
    }
else:
    inserts = {
            'rxb 11,1': 'GUGGGAUACCAGCCGAAAGGCCCUUGGCAGCCUAC',
            'mhf 30': 'GCCGAUACCAGCCGAAAGGCCCUUGGCAGCGAC'
    }

def calc_energy(spacer, insert):
    if args['--algorithm'] == 'mfe':
        duplex = RNA.duplexfold(spacer, insert)
        return duplex.energy
    elif args['--algorithm'] == 'mfe-dimer':
        fc = RNA.fold_compound(f'{spacer}&{insert}')
        return fc.mfe_dimer()[1]
    elif args['--algorithm'] == 'pf-dimer':
        fc = RNA.fold_compound(f'{spacer}&{insert}')
        return fc.pf_dimer()[1]
    else:
        raise ValueError(f"unknown algorithm: '{args['--algorithm']}'")

def calc_energy_from_row(row):
    spacer = sgrna_sensor.spacer(row.spacer).seq
    insert = inserts[row.design]
    return calc_energy(spacer, insert)


if args['<spacer>'] and args['<design>']:
    spacer = sgrna_sensor.spacer(args['<spacer>']).rna
    insert = inserts[args['<design>']]
    print(f"Spacer: {spacer}")
    print(f"Insert: {insert}")
    print(f"ΔG:     {calc_energy(spacer, insert)}")

else:
    df = densiometry.load_cleavage_data_from_xlsx_dir('densiometry')
    df = densiometry.calc_mean_change(df)

    # Drop all the controls
    df = df[df.design.isin(inserts.keys())]


    # Calculate the minimum free energy (MFE) for binding between the spacer 
    # and the aptamer insert.
    df['binding_energy'] = df.apply(calc_energy_from_row, axis='columns')

    def plot_design(design, color): #
        i = df.design == design
        x = abs(df[i].max_change if args['--max-change'] else df[i].mean_change)
        y = df[i].binding_energy
        m, b, R, p, err = linregress(x, y)

        X = np.linspace(0, 1)
        Y = m * X + b

        plt.plot(x, y, 'o', color=color, label='_nolegend_')
        plt.plot(X, Y, '-', color=color, label=f'{design} (R={R:.3f})')

    plot_design('mhf 30', ucsf.teal[0])
    plot_design('rxb 11,1', ucsf.navy[0])
    plt.xlabel('Δ cleavage (%)')
    plt.ylabel('ΔG (kcal/mol)')
    plt.legend()
    plt.savefig('predict_spacer_quality.svg')
    plt.title(' '.join(sys.argv))
    plt.show()
