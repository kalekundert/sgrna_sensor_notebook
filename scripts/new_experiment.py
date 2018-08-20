#!/usr/bin/env python3

"""
Create a new file where you can keep notes on this experiment.

Usage:
    new_experiment.py <title>...

The current date will be prepended to the name of the new file, and the file 
will be preloaded with the given title.
"""

def find_notebook_dir():
    from pathlib import Path
    return Path('.')

def main():
    import re
    import docopt
    from datetime import datetime
    from sh import gvim

    class Sanitizer: #
        def __getitem__(self, ord): #
            char = chr(ord)
            if char.isalnum(): return char.lower()
            if char in ' _-': return '_'

    args = docopt.docopt(__doc__)
    date = datetime.today().strftime('%Y%m%d')
    title = ' '.join(args['<title>'])
    slug = title.translate(Sanitizer())

    dir = find_notebook_dir()
    rst = dir / f'{date}_{slug}' / f'{slug}.rst'
    index = dir / 'index.rst'

    if rst.parent.exists():
        print("Experiment already exists, not overwriting.")
        raise SystemExit
    else:
        rst.parent.mkdir()

    with rst.open('w') as file:
        file.write(f"""\
{'*' * len(title)}
{title}
{'*' * len(title)}
\n
""")

    with index.open('a') as file:
        file.write(f'   {rst.relative_to(dir)}\n')

    gvim('-c', 'startinsert', '+', rst)

if __name__ == '__main__':
    main()





