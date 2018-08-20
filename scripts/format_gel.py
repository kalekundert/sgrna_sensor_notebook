#!/usr/bin/env python3

"""\
Format a gel for inclusion in the lab notebook.  In particular, this means 
converting it from a *.tif to a *.png, inverting it's colors, and giving you a 
chance to crop it.
Usage:
    format_gel.py [<gel>] [options]

Arguments:
    <gel>
        The path to an gel image, relative to the data/gels directory.

Options:
    -f --force
        Overwrite any existing image.
"""

import docopt

args = docopt.docopt(__doc__)
