#!/usr/bin/env python3

"""\
Usage:
    induce_and_trizol_fast.py <apo/holo>

Arguments:
    <apo/holo>
        Indicate whether you will be adding ("holo") or removing ("apo")
        theophylline before taking timepoints.
"""

import docopt
import dirty_water

args = docopt.docopt(__doc__)
protocol = dirty_water.Protocol()

after = args['<apo/holo>']
before = 'apo' if after == 'holo' else 'holo'
sample = f'{before}→{after}'

protocol += f"""\
Start overnight cultures in 1 mL LB + Carb + Chlor 
for the 4 ligRNA constructs (on, off, rxb/11/1, 
mhf/30) and the wildtype MG1655 control.
"""

protocol += f"""\
Start day cultures:

- Thaw 50 mL each of apo and holo media.

- Subculture 44 µL of each overnight into 11 mL
  {before} media.

- Subculture 4 µL of each overnight into 1 mL
  {after} media.

- Subculture 4 µL of wildtype MG1655 (no GFP/RFP) 
  into 1 mL apo media.

- Grow at 37°C for 4h30.
"""

protocol += f"""\
Get ready to take timepoints:

- Label 41 1.5 mL tubes (one for each of the 
  conditions listed in the table below).

- Fill 8 columns of a 96-well block with 1.1 mL 
  {after} media in every other row.  Pre-warm the 
  block to 37°C.

- Prepare a workspace in the fume hood:
  - Benchtop centrifuge
  - 37°C block with at least 40 slots.
  - Waste beaker (for media)
  - Container for TRIzol waste
  - 8-channel P1000
  - Three boxes of P1000 tips, two with tips only 
    in every other row
  - Wipe surface with ethanol and RNaseZap

- Just before starting the next step:
  - Fill a reservoir with 50 mL TRIzol
"""

protocol += f"""\
Resuspend each sample (except for the 0:00 
timepoints, see table below) in {after} media:

- Pipet 1 mL of each day culture into a properly 
  labeled tube.

- Pellet at 16,000g for 30s.

- Discard supernatant.  One or two sharp downward 
  shakes is usually enough to get the last bit of 
  media out.

- Place the pellets in the 37°C block.

- Start a timer.

- Use a multichannel pipet to simultaneously 
  resuspend all samples for the same timepoint.

  - Do the lastest timepoints first and the 
    earliest timepoints last.

  - Aim for 0:30 between each timepoints.

─────────────────────────────────────────────────────
                           Switch    Pellet       Add
Sample    N  Timepoint      Media     Cells    TRIzol
─────────────────────────────────────────────────────
{sample:8s}  4      30:00
{sample:8s}  4      24:30
{sample:8s}  4      19:30
{sample:8s}  4      15:00
─────────────────────────────────────────────────────
{sample:8s}  4      11:00
{sample:8s}  4       7:30
{sample:8s}  4       4:30
{sample:8s}  4       2:00
─────────────────────────────────────────────────────
apo       4       0:00        N/A       N/A
holo      4       0:00        N/A       N/A
no GFP    1       0:00        N/A       N/A
─────────────────────────────────────────────────────
"""

protocol += f"""\
Stop each timepoint as appropriate:

- 1 minute before the desired timepoint:

  ───────────────────────────────────────
  Countdown  Task   
  ───────────────────────────────────────
       1:00  Load centrifuge.
       0:52  Pellet at 16,000g for 15s
       0:25  Decant supernatant; arrange
             diagonally in tube rack
       0:00  Add 1 mL TRIzol
  ───────────────────────────────────────
"""

protocol += f"""\
Store the cell extracts at 4°C overnight, if you 
don't want to continue all the way to end.
"""

protocol += f"""\
Finish the RNA extractions.

- Label 41 clean 1.5 mL tubes.

- Add 200 µL chloroform.

- Vortex vigorously.

- Centrifuge for 15 min at 20,000g and 4°C.

- Transfer 400 µL of the aqueous phase (top, not 
  pink) to a clean tube, taking care to avoid 
  transferring any of the organic phase.
"""

protocol += f"""\
Concentrate and purify the RNA by ethanol 
precipitation:

- Add 1 µL GlycoBlue (Invitrogen AM9516) to each 
  sample.

- Add 500 µL isopropanol.

- Incubate at room temperature for 10 min.

- Pellet for 20 min at 12,000g and 4°C.

- Carefully pipet off all supernatant.

- Resuspend pellet in 1 mL 70% EtOH.

- Vortex briefly

- Pellet for 5 min at 7,500g and 4°C.

- Carefully pipet off all supernatant.

- Air dry for 10 min.

- Resuspend RNA in 10 µL water.  

  - Pipet to mix, then incubate at 50°C with 
    intermittent gentle vortexing.
"""

protocol += f"""\
Measure the RNA concentration of each sample using 
the Nanodrop.  Expected yield: ~300±125 ng/µL.
"""

print(protocol)

# vim: tw=50
