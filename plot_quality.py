#!/usr/bin/python3.8

import sqlite3
import argparse
import subprocess
import pathlib
from halo import Halo

plot_location = '/media'

#

parser = argparse.ArgumentParser(description="CHIA plots quality manager")
parser.add_argument("-s", "--scan", help="scan for new plots and update the database", action="store_true")
parser.add_argument("-u", "--update", type=int, help="update quality of new plots in the database."
                                                     " specify number of plots to process")
parser.add_argument("-q", "--quality", type=int, help="show plots with specified or less quality")
parser.add_argument("-d", "--dir", default=f"{plot_location}", help=f"root directory of plots (default: %(default)s)")
args = parser.parse_args()

#

con = sqlite3.connect('plot_quality.db')
cur = con.cursor()
cur.execute('CREATE TABLE if not exists plots (name TEXT, quality INTEGER, UNIQUE(name))')

if args.scan:
    with Halo(text='scanning', color='white'):
        plots0 = subprocess.getoutput(
            f"find {args.dir} -path '*CHIA*' -name 'plot*plot' -exec ls {{}} \; 2> /dev/null").split("\n")

        for plot in plots0:
            fname = pathlib.Path(plot.strip())
            cur.execute(f"INSERT OR IGNORE INTO plots VALUES('{fname.name}', -1)")

#

if args.update is not None:
    for i in range(1, args.update + 1):
        cur.execute(f"SELECT name FROM plots WHERE quality<0 LIMIT 1")
        current_plot_name = cur.fetchone()[0]
        with Halo(text=f"processing plot {i} - {current_plot_name}", color='white'):
            str0 = f"cd ~/src/chia-blockchain/ && . ./activate && chia plots check -g {current_plot_name} 2>&1 " \
                   f" | egrep 'Proofs'"
            out0 = subprocess.getoutput(f"{str0}").split('Proofs')[1].strip().split('/')[0].strip()
            if out0.isnumeric():
                cur.execute(f"UPDATE plots SET quality={out0} WHERE name='{current_plot_name}'")
                con.commit()
            else:
                print('ERROR: output of `chia plots check` can`t be processed')

    print('---')

#

if args.quality is not None:
    cur.execute(f"SELECT quality, name FROM plots WHERE (quality>0) and (quality<{args.quality}) ORDER BY quality ASC")
    for row in cur.fetchall():
        print(f"{row[0]} {row[1]}")

    print('---')

#

cur.execute(f"SELECT count(*) FROM plots")
print(f"total number of plots in the database:  {cur.fetchone()[0]}")
cur.execute(f"SELECT count(*) FROM plots WHERE quality>0")
print(f"number of plots with processed quality: {cur.fetchone()[0]}")

con.commit()
con.close()
