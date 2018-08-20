#!/usr/bin/env python3

"""\
Return the directory name that best matches the given abbreviation.  If there 
are multiple matches, return the most recent.  If no abbreviation is given, 
just return the most recent directory period.

Usage:
    parse_abbrev [<abbrev>] [options]

Options:
    --cwd <directory>
        The directory to interpret the abbreviation in relation to.  By default 
        the is the notebook root.
        
    --doc-path
        Print the path to the main notebook document.  The default is to just 
        print the path to the notebook directory.

    --abs-path
        Print the absolute path to the directory.  The default is to just 
        print the path relative to the root of the notebook.
    
"""

from pathlib import Path
from fnmatch import fnmatch

def parse_abbrev(abbrev, cwd=None):
    root = Path(__file__).parent.parent

    if cwd and not root.samefile(cwd):
        return Path(cwd)

    matches = [
            p for p in root.iterdir()
            if p.is_dir() and fnmatch(str(p), f'{8*"[0-9]"}_*{abbrev}*')
    ]
    if not matches:
        raise ValueError(f"No experiments matching '{abbrev}'")
    return sorted(matches)[-1]

if __name__ == '__main__':
    import docopt
    args = docopt.docopt(__doc__)
    abbrev = args['<abbrev>'] or ''

    path = parse_abbrev(abbrev, args['--cwd'])

    if args['--abs-path']:
        path.resolve()

    #if args['--rel-path']:



    if args['--doc-path']:
        path = path / f'{path.name[9:]}.rst'

    print(path)



