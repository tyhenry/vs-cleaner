#!/usr/bin/env python

import argparse
import os
import shutil
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument('dir_path', type=Path)

p = parser.parse_args()
d = p.dir_path.resolve()

if d.exists():
    print(f'\nsearching for .vs* dirs inside "{d}"...')
    results = sorted(d.glob('**/.vs*'))
    if len(results) > 0:

        mb = 0.0
        print('found:\n-------------------------------------------------------------------------')
        for result in results:
            sz = sum(f.stat().st_size for f in result.glob('**/*') if f.is_file() )
            sz_mb = sz / (1024 * 1024.0)
            mb = mb + sz_mb
            print(f'{sz_mb:.2f} mb:\t{result}')
        print('-------------------------------------------------------------------------')
        print(f'total (mb): {mb:.2f}')

        while True:
            confirm = input('delete all? (y/n)').lower()
            if confirm == 'y' or confirm == 'yes':
                for result in results:
                    if result.is_dir():
                        try:
                            shutil.rmtree(result)
                        except Exception as e:
                            print(f'error deleting "{result}", skipping - exception:\n\t{e}')
                break
            elif confirm == 'n' or confirm == 'no':
                print('leaving .vs* dirs in place')
                break

    else:
        print('no .vs* dirs found')

else:
    print(f'error: directory not found: "{d}", aborting')


