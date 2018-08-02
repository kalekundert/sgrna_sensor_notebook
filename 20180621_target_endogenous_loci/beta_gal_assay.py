#!/usr/bin/env python3

"""\
Assay β-galactosidase activity in cells.

Usage:
    beta_gal_assay.py [<num_reactions>]

Arguments:
    <num_reactions>
        The number of reactions to setup, counting blanks.  The default is 50:
        (1 blank + 2 controls + 2 ligRNAs) × 5 guides × 2 conditions.
"""

import docopt
import dirty_water
from dirty_water import with_extra, round_to_pipet

args = docopt.docopt(__doc__)
p = dirty_water.Protocol()
n = eval(args['<num_reactions>'] or '50')

p += f"""\
Make overnight cultures for all strains being 
tested.
"""

lb2 = with_extra(n/2)
lb = with_extra(2*lb2)
theo = round_to_pipet(1000 * lb2 / 30)

p += f"""\
Start the day cultures:

- Prepare {lb2} mL each of apo and holo media:
  
  - {round_to_pipet(lb - 13/1000 * lb - lb/30)} mL LB
  - {lb} µL 100 mg/mL carbenicillin (Carb)
  - {lb} µL 34 mg/mL chloramphenicol (Chlor)
  - {10*lb} µL 100 µg/mL anhydroteracycline (ATc)
  - {lb} µL 1M IPTG

  - Split into 2 {round_to_pipet(lb2 - lb2/30)} mL portions.
  - Add {theo} µL LB or 30 mM theophylline (in LB) 
    to the apo and holo portions, respectively.

- For each reaction, inoculate 1 mL media with 4 
  µL overnight culture.  Also prepare 1 mL media 
  with no cells, as a blank.
"""

p += f"""\
Grow at 37°C until OD600 reaches 0.5−1.0 (~6h30)
"""

ws = 150 * n
p += f"""\
Start the β-galactosidase assay:

- Prepare {ws} µL of Working solution (WS):
  - {ws//2} µL Y-PER
  - {ws//2} µL 2x β-galactosidase assay buffer.
  - Aliquot 140 µL into PCR strip-tubes.

- Aliquot 100 µL of each culture into a clear 
  plate.

- Measure OD600.  Dilute as necessary to ensure 
  that has well has OD600 > 0.2 (plate reader path 
  length).

- Add 100 µL WS to each reaction and mix well.

  WS is very soapy, so you need to take care to 
  avoid getting bubbles in the wells.  Reverse 
  pipet to add the WS in the first place, then mix 
  very carefully.  Pop any bubbles with a hot 
  needle.
"""

p += f"""\
Measure A420 every 5 min for 2h.  

It's probably unnecessary, but I have the spectro- 
photometer shake the plate for 20s before each 
measurement to ensure good mixing.
"""

print(p)

# vim: tw=50
