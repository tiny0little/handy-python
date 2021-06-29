#!/usr/bin/python3

import subprocess
import argparse
from halo import Halo
import pathlib
import datetime
import time
import pandas as pd
from tabulate import tabulate

#
#

colorGREEN = '\033[92m'
colorYELLOW = '\033[93m'
colorRED = '\033[91m'
colorENDC = '\033[0m'
colorBOLD = '\033[1m'
colorWHITEonPURPLE = '\33[45m'
colorWHITEonGREEN = '\33[42m'
colorWHITEonBLUE = '\33[44m'
colorWHITEonRED = '\33[41m'

#
#

tabu_table = []
dates_df = pd.DataFrame(columns=['year', 'mon', 'day'])
plots_df = pd.DataFrame(columns=['year', 'mon', 'day', 'file_name'])

parser = argparse.ArgumentParser(description="counting how many CHIA plots made per day")
parser.add_argument("-f", "--files", help="show plot files or not (default: %(default)s)",
                    default=1, type=int, choices=[0, 1])
parser.add_argument("-d", "--days", help="show number of last days (default: %(default)s)",
                    default=3, type=int)
parser.add_argument("-r", "--remove", help="remove zero size plots", action="store_true")
args = parser.parse_args()

#
#

with Halo(color='white'):
    small_plots = subprocess.getoutput("find /media/ -path '*CHIA*' -name 'plot*plot' -size -99G  2> /dev/null") \
        .split("\n")
    if small_plots[0] == '': small_plots.pop()

    plots0 = subprocess.getoutput("find /media/ -path '*CHIA*' -name 'plot*plot' -exec ls {} \; 2> /dev/null") \
        .split("\n")

    for plot in plots0:
        fname = pathlib.Path(plot.strip())
        year = datetime.datetime.fromtimestamp(fname.stat().st_mtime).year
        mon = datetime.datetime.fromtimestamp(fname.stat().st_mtime).month
        day = datetime.datetime.fromtimestamp(fname.stat().st_mtime).day
        dates_df = dates_df.append({'year': year, 'mon': mon, 'day': day}, ignore_index=True)
        plots_df = plots_df.append({'file_name': plot.strip(), 'year': year, 'mon': mon, 'day': day}, ignore_index=True)

    dates_df = dates_df.drop_duplicates()
    dates_df = dates_df.sort_values(by=['year', 'mon', 'day'])
    dates_df = dates_df.iloc[-args.days:, :]

#
#


for index0, row0 in dates_df.iterrows():
    if args.files: tabu_table = []

    date0 = f"{row0['year']}-{row0['mon']:02.0f}-{row0['day']:02.0f}"
    files0 = plots_df.loc[
        (plots_df['year'] == row0['year']) &
        (plots_df['mon'] == row0['mon']) &
        (plots_df['day'] == row0['day'])]
    plots0 = f"{files0['file_name'].count()}"

    file_size = 0
    for index1, row1 in files0.iterrows():
        fname = pathlib.Path(row1['file_name'])
        file_size += fname.stat().st_size
    file_size *= 1e-12
    total_size0 = f"{file_size:.1f} TB"

    tabu_table.append([date0, plots0, total_size0])
    if args.files:
        row0 = ['left', 'left', 'left']
        print(tabulate(tabu_table, headers=['date', 'total plots', 'total size'], colalign=row0, tablefmt='pretty'))

    #
    #

    if args.files:
        tabu_table = []
        for index1, row1 in files0.iterrows():
            fname = pathlib.Path(row1['file_name'])
            plot_finish_time = fname.stat().st_mtime
            tmp0 = row1['file_name'].split('plot-')[1].split('-')[1:-1]
            tmp1 = f"{tmp0[0]}-{tmp0[1]}-{tmp0[2]} {tmp0[3]}:{tmp0[4]}"
            plot_start_time = time.mktime(datetime.datetime.strptime(tmp1, "%Y-%m-%d %H:%M").timetuple())
            plot_time_in_sec = plot_finish_time - plot_start_time
            min0, sec0 = divmod(plot_time_in_sec, 60)
            hour0, min0 = divmod(min0, 60)
            tabu_table.append(
                [row1['file_name'], f"{fname.stat().st_size * 9.31323e-10:0.1f}GiB", f"{hour0:02.0f}h{min0:02.0f}m"])

        row0 = ['left', 'left', 'left']
        print(tabulate(tabu_table, colalign=row0, tablefmt='pretty'))

if not args.files:
    row0 = ['left', 'left', 'left']
    print(tabulate(tabu_table, headers=['date', 'plots', 'size'], colalign=row0, tablefmt='pretty'))


# plots with errors
if len(small_plots) > 0:
    tabu_table = []
    for plot in small_plots:
        fname = pathlib.Path(plot.strip())
        tabu_table.append(
            [f"{colorWHITEonRED}{colorBOLD}{plot}{colorENDC}", f"{fname.stat().st_size * 9.31323e-10:0.1f}GiB"])

    row0 = ['left', 'left']
    print(tabulate(tabu_table, headers=['plots with wrong file size', ''], colalign=row0, tablefmt='pretty'))

#
if args.remove:
    subprocess.getoutput("find /media/ -path '*CHIA*' -name 'plot*plot' -empty -delete")
