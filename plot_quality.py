#!/usr/bin/python3.8

import sqlite3
from contextlib import closing
import argparse
import subprocess
import pathlib
from halo import Halo

plot_location = '/media'
tmp_file = '/tmp/plot_quality.tmp'
db_fname = '/home/user/src/handy-tools/plot_quality.db'

#

parser = argparse.ArgumentParser(description="CHIA plots quality manager")
parser.add_argument("-s", "--scan", help="scan for new plots and update the database", action="store_true")
parser.add_argument("-i", "--integrity", help="validate integrity of the database", action="store_true")
parser.add_argument("-u", "--update", type=int, help="update quality of new plots in the database."
                                                     " specify the number of plots to process")
parser.add_argument("-q", "--quality", type=int, help="show plots with specified or less quality")
parser.add_argument("-t", "--top", type=int, help="show top N quality plots")
parser.add_argument("-p", "--plot", type=str, help="show plots by pattern")
parser.add_argument("-d", "--dir", default=f"{plot_location}", help=f"root directory of plots (default: %(default)s)")
parser.add_argument("-r", "--remove", help="remove plot from the database by provided pattern")

args = parser.parse_args()

#

with closing(sqlite3.connect(db_fname)) as con, con, closing(con.cursor()) as cur:
    cur.execute('CREATE TABLE if not exists plots (name TEXT, quality INTEGER, UNIQUE(name))')

if args.scan:
    with Halo(text='scanning', color='white'):
        plots0 = subprocess.getoutput(
            f"find {args.dir} -path '*CHIA*' -name 'plot*plot' -size +99G -exec ls {{}} \; 2> /dev/null").split("\n")

        with closing(sqlite3.connect(db_fname)) as con, con, closing(con.cursor()) as cur:
            for plot in plots0:
                fname = pathlib.Path(plot.strip())
                if len(fname.name) > 77: cur.execute(f"INSERT OR IGNORE INTO plots VALUES('{fname.name}', -1)")

#

if args.integrity:
    with closing(sqlite3.connect(db_fname)) as con, con, closing(con.cursor()) as cur:
        cur.execute(
            f"SELECT name FROM plots")
        plots = cur.fetchall()

    for fname in plots:
        with Halo(text=f"processing {fname[0]}", color='white'):
            str0 = f"find {args.dir} -path '*CHIA*' -name '{fname[0]}' -size +99G -exec ls {{}} \; 2> /dev/null | wc -l"
            if subprocess.getoutput(str0) != '1':
                print()
                print(f"{fname[0]} does not exist")

#

if args.update is not None:
    update_count = args.update
    if update_count == 0:
        with closing(sqlite3.connect(db_fname)) as con, con, closing(con.cursor()) as cur:
            cur.execute(f"SELECT count(*) FROM plots WHERE quality<0")
            update_count = cur.fetchone()[0]

    print_warning = False
    for i in range(1, update_count + 1):
        print_error = False
        sql0 = "SELECT name FROM plots WHERE quality<0 LIMIT 1"
        with closing(sqlite3.connect(db_fname)) as con, con, closing(con.cursor()) as cur:
            cur.execute(sql0)
            if cur.fetchone() is not None:
                cur.execute(sql0)
                current_plot_name = cur.fetchone()[0]
                with Halo(text=f"processing plot {i} - {current_plot_name}", color='white'):
                    str0 = f"cd ~/src/chia-blockchain/ && . ./activate && chia plots check " \
                           f"-g {current_plot_name} 2>&1 | egrep 'Proofs' > {tmp_file}"
                    subprocess.getoutput(f"{str0}")
                    out0 = subprocess.getoutput(f"cat {tmp_file} | egrep Proofs | wc -l")
                    if int(out0) > 0:
                        out0 = subprocess.getoutput(f"cat {tmp_file}").split('Proofs')[1].strip().split('/')[0].strip()
                        if out0.isnumeric():
                            cur.execute(f"UPDATE plots SET quality={out0} WHERE name='{current_plot_name}'")
                        else:
                            print_error = True
                    else:
                        print_error = True
                    if print_error: print(' ERROR: output of `chia plots check` can`t be processed')
                    subprocess.getoutput(f"rm {tmp_file}")
            else:
                print_warning = True
    if print_warning: print(' WARNING: no more plots to process')

#

if args.quality is not None:
    with closing(sqlite3.connect(db_fname)) as con, con, closing(con.cursor()) as cur:
        cur.execute(
            f"SELECT quality, name FROM plots WHERE (quality>0) and (quality<={args.quality}) ORDER BY quality ASC")
        for row in cur.fetchall():
            print(f"{row[0]} {row[1]}")

    print('---')

#

if args.top is not None:
    with closing(sqlite3.connect(db_fname)) as con, con, closing(con.cursor()) as cur:
        cur.execute(
            f"SELECT quality, name FROM plots ORDER BY quality DESC LIMIT {args.top}")
        for row in cur.fetchall():
            print(f"{row[0]} {row[1]}")

    print('---')

#

if args.plot is not None:
    with closing(sqlite3.connect(db_fname)) as con, con, closing(con.cursor()) as cur:
        cur.execute(
            f"SELECT quality, name FROM plots WHERE name LIKE '%{args.plot}%' ORDER BY quality DESC LIMIT 25")
        for row in cur.fetchall():
            print(f"{row[0]} {row[1]}")

    print('---')

#

if args.remove is not None:
    with closing(sqlite3.connect(db_fname)) as con, con, closing(con.cursor()) as cur:
        cur.execute(f"DELETE FROM plots WHERE name LIKE '%{args.remove}%'")

#

with closing(sqlite3.connect(db_fname)) as con, con, closing(con.cursor()) as cur:
    cur.execute(f"SELECT count(*) FROM plots")
    print(f"total number of plots in the database:  {cur.fetchone()[0]}")
    cur.execute(f"SELECT count(*) FROM plots WHERE quality<0")
    print(f"number of plots needs to be processed:  {cur.fetchone()[0]}")
