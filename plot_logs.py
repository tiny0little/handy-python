#!/usr/bin/python3.8

import glob
import subprocess
from dateutil.parser import *
from dateutil.relativedelta import relativedelta
from datetime import *
from tabulate import tabulate
import os
import argparse
from operator import itemgetter
from halo import Halo
from pathlib import Path

log_location = str(Path.home()) + "/.chia/mainnet/plotter"
final_completed_table = []
final_running_table = []


def is_new_plotter(_log_file: str) -> bool:
    _output0 = int(subprocess.getoutput(f"cat {_log_file} | egrep 'Multi-threaded pipelined Chia k32 plotter' | wc -l"))
    return _output0 > 0


def get_time(_phase: int, _log_file: str, _start_line: int, _end_line: int) -> str:
    _result = ''
    if is_new_plotter(_log_file):
        _output0 = subprocess.getoutput(
            f"awk 'NR >= {_start_line} && NR <= {_end_line}' {_log_file} | egrep 'Phase {_phase} took' | tail -1").\
            split("sec")
    else:
        if _phase < 100:
            _search_str = f"Time for phase {_phase}"
        else:
            _search_str = "Copy time"
        _output0 = subprocess.getoutput(
            f"awk 'NR >= {_start_line} && NR <= {_end_line}' {_log_file} | egrep '{_search_str}' | tail -1"). \
            split("seconds.")

    if len(_output0) > 1:
        _output0 = int(float(_output0[0].split("=")[1].strip()))
        _min, _sec = divmod(_output0, 60)
        _hours, _min = divmod(_min, 60)
        _result = f"{_hours:02d}h{_min:02d}m"
    return _result


# adds two times
def get_time2(_str1: str, _str2: str, _log_file: str, _start_line: int, _end_line: int) -> str:
    if is_new_plotter(_log_file):
        _result = 'u'
    else:
        _output1 = subprocess.getoutput(
            f"awk 'NR >= {_start_line} && NR <= {_end_line}' {_log_file} | egrep '{_str1}' | tail -1").split("seconds.")
        _output2 = subprocess.getoutput(
            f"awk 'NR >= {_start_line} && NR <= {_end_line}' {_log_file} | egrep '{_str2}' | tail -1").split("seconds.")
        _result = ""
        if len(_output1) > 1 and len(_output2) > 1:
            _output0 = int(float(_output1[0].split("=")[1].strip())) + int(float(_output2[0].split("=")[1].strip()))
            _min, _sec = divmod(_output0, 60)
            _hours, _min = divmod(_min, 60)
            _result = f"{_hours:02d}h{_min:02d}m"
    return _result


def get_phase_progress(phase: int, _steps: int, _log_file, _start_line: int, _end_line: int) -> str:
    _result = ''
    if is_new_plotter(_log_file):
        _output0 = int(subprocess.getoutput(
            f"awk 'NR >= {_start_line} && NR <= {_end_line}' {_log_file} | egrep '[[P{phase}]]' | wc -l"))
        if _output0 > 0:
            for _i in range(int(_output0)): _result += "#"
            for _i in range(_steps - int(_output0)): _result += "."
    else:
        if phase == 1: _search_text = "Computing table"
        if phase == 2: _search_text = "Backpropagating on table"
        if phase == 3: _search_text = "Compressing tables"
        if phase == 4: _search_text = "Starting phase 4/4"
        _output0 = int(subprocess.getoutput(
            f"awk 'NR >= {_start_line} && NR <= {_end_line}' {_log_file} | egrep '{_search_text}' | wc -l"))
        if _output0 > 0:
            for _i in range(int(_output0)): _result += "#"
            for _i in range(_steps - int(_output0)): _result += "."
    return _result


def get_plot_size(_log_file: str, _start_line: int, _end_line: int) -> str:
    _result = '??'
    if is_new_plotter(_log_file):
        _result = '32'
    else:
        _str = f"awk 'NR >= {_start_line} && NR <= {_end_line}' {_log_file} | egrep 'Plot size is'"
        if int(subprocess.getoutput(f"{_str} | wc -l")) > 0:
            _result = subprocess.getoutput(f"{_str}").split(":")[1].strip()
    return _result


def get_buckets(_log_file: str, _start_line: int, _end_line: int) -> str:
    _result = '??'
    if is_new_plotter(_log_file):
        _str = f"awk 'NR >= {_start_line} && NR <= {_end_line}' {_log_file} | egrep 'Number of Buckets'"
        if int(subprocess.getoutput(f"{_str} | wc -l")) > 0:
            _result = subprocess.getoutput(f"{_str}").split("(")[1].split(")")[0].strip()
    else:
        _str = f"awk 'NR >= {_start_line} && NR <= {_end_line}' {_log_file} | egrep 'Using [0-9]+ buckets'"
        if int(subprocess.getoutput(f"{_str} | wc -l")) > 0:
            _result = subprocess.getoutput(f"{_str}").split("Using")[1].split("buckets")[0].strip()
    return _result


def get_threads(_log_file: str, _start_line: int, _end_line: int) -> str:
    _result = '??'
    if is_new_plotter(_log_file):
        _str = f"awk 'NR >= {_start_line} && NR <= {_end_line}' {_log_file} | egrep 'Number of Threads'"
        if int(subprocess.getoutput(f"{_str} | wc -l")) > 0:
            _result = subprocess.getoutput(f"{_str}").split(":")[1].strip()
    else:
        _str = f"awk 'NR >= {_start_line} && NR <= {_end_line}' {_log_file} | egrep 'Using [0-9]+ threads'"
        if int(subprocess.getoutput(f"{_str} | wc -l")) > 0:
            _result = subprocess.getoutput(f"{_str}").split("Using")[1].split("threads")[0].strip()
    return _result


def get_buffer_size(_log_file: str, _start_line: int, _end_line: int) -> str:
    _result = '-'
    if is_new_plotter(_log_file):
        pass
    else:
        _str = f"awk 'NR >= {_start_line} && NR <= {_end_line}' {_log_file} | egrep 'Buffer size is: [0-9]+MiB'"
        if int(subprocess.getoutput(f"{_str} | wc -l")) > 0:
            _result = subprocess.getoutput(f"{_str}").split("is:")[1].split("MiB")[0].strip()
    return _result


def get_temp_dir(_log_file: str, _start_line: int, _end_line: int) -> str:
    _result = '??'
    if is_new_plotter(_log_file):
        _str = f"awk 'NR >= {_start_line} && NR <= {_end_line}' {_log_file} | egrep 'Working Directory' | head -1"
        if int(subprocess.getoutput(f"{_str} | wc -l")) > 0:
            _result = subprocess.getoutput(f"{_str}").split(":")[1].strip()
    else:
        _str = f"awk 'NR >= {_start_line} && NR <= {_end_line}' {_log_file} | egrep 'progress into temporary dirs'"
        if int(subprocess.getoutput(f"{_str} | wc -l")) > 0:
            _result = subprocess.getoutput(f"{_str}").split(":")[1].strip()
            _result = _result.split("and")[0].strip() + "/"
    return _result


def get_final_dir(_log_file: str, _start_line: int, _end_line: int) -> str:
    _output = "??"
    _str = f"awk 'NR >= {_start_line} && NR <= {_end_line}' {_log_file} | egrep 'Copied final file from'"
    if int(subprocess.getoutput(f"{_str} | wc -l")) > 0:
        _output = subprocess.getoutput(f"{_str}").split(" to ")[1].strip()
        _output = _output.split("/plot-k")[0].strip()[1:] + "/"
    return _output


#
#
parser = argparse.ArgumentParser(description="plot logs analyzer")
parser.add_argument("-d", "--dir", default=f"{log_location}", help=f"location of plot logs (default: %(default)s)")
parser.add_argument("-l", "--log_file", default="*", help=f"log file name pattern (default: %(default)s)")
parser.add_argument("-cp", "--completed_plots", action="store_true", help="show completed plots")
parser.add_argument("-s", "--sort", choices=['plot', 'p', 'time', 't'], nargs='?', default='time', const='time',
                    help="which column used for sorting the table? (default: %(default)s)")
parser.add_argument("-nc", "--nocolor", help="do not use colors", action="store_true")
parser.add_argument("-t", "--tabfmt",
                    choices=["plain", "simple", "github", "grid", "fancy_grid", "pipe", "orgtbl", "presto",
                             "pretty", "psql", "rst", "tsv"
                             ], nargs='?', default='pretty', const='pretty',
                    help="table format")

args = parser.parse_args()

log_location = args.dir

#
#
if args.nocolor:
    colorENDC = ''
    colorBOLD = ''
    colorWHITEonGREEN = ''
    colorWHITEonBLUE = ''
else:
    colorENDC = '\033[0m'
    colorBOLD = '\033[1m'
    colorWHITEonGREEN = '\33[42m'
    colorWHITEonBLUE = '\33[44m'

final_completed_table.append(
    [f"{colorWHITEonGREEN}{colorBOLD}COMPLETED PLOTS{colorENDC}", "temp", "final", "k", "buckets",
     "buffer", "threads", "p1 time", "p2 time", "p3 time", "p4 time", "cp time", "total"])
final_running_table.append(
    [f"{colorWHITEonBLUE}{colorBOLD}RUNNING PLOTS{colorENDC}", "temp", "k", "buckets", "buffer", "threads", "p1",
     "p1 time", "p2", "p2 time", "p3", "p3 time", "p4", "p4 time", "runtime"])
log_files = glob.glob(f"{log_location}/*{args.log_file}*log")

with Halo(color='white'):
    for log_file in log_files:

        start_line = 1
        end_line = 1

        #
        # processing completed plots
        #
        if args.completed_plots:
            output = subprocess.getoutput(f"grep -n 'Copy time' {log_file}").split("\n")
            for line in output:
                end_line0 = line.split(":")[0].strip()
                if end_line0.isnumeric():
                    end_line = int(end_line0)
                    final_completed_table.append(
                        [os.path.basename(log_file), get_temp_dir(log_file, start_line, end_line),
                         get_final_dir(log_file, start_line, end_line),
                         get_plot_size(log_file, start_line, end_line),
                         get_buckets(log_file, start_line, end_line),
                         get_buffer_size(log_file, start_line, end_line),
                         get_threads(log_file, start_line, end_line),
                         get_time(1, log_file, start_line, end_line),
                         get_time(2, log_file, start_line, end_line),
                         get_time(3, log_file, start_line, end_line),
                         get_time(4, log_file, start_line, end_line),
                         get_time(101, log_file, start_line, end_line),
                         get_time2("Total time", "Copy time", log_file, start_line, end_line)])

                start_line = end_line + 1

        #
        # processing currently running plot
        #
        # start_line
        str0 = f"egrep -n 'Starting plotting progress into temporary' {log_file} | tail -1"
        if int(subprocess.getoutput(f"{str0} | wc -l")) > 0:
            start_line = int(subprocess.getoutput(f"{str0}").split(":")[0].strip())
        else:
            start_line = 1

        #
        # end_line
        end_line = int(subprocess.getoutput(f"cat {log_file} | wc -l").strip())

        #
        # start_tine of current plot
        str0 = f"awk 'NR >= {start_line}' {log_file} | egrep 'Starting phase 1/4: Forward Propagation' | tail -1"
        if int(subprocess.getoutput(f"{str0} | wc -l")) > 0:
            start_time = parse(subprocess.getoutput(f"{str0}").split("...")[1].strip())
        else:
            start_time = datetime.now()

        running_time = relativedelta(datetime.now(), start_time)

        final_running_table.append([os.path.basename(log_file), get_temp_dir(log_file, start_line, end_line),
                                    get_plot_size(log_file, start_line, end_line),
                                    get_buckets(log_file, start_line, end_line),
                                    get_buffer_size(log_file, start_line, end_line),
                                    get_threads(log_file, start_line, end_line),
                                    get_phase_progress(1, 7, log_file, start_line, end_line),
                                    get_time(1, log_file, start_line, end_line),
                                    get_phase_progress(2, 6, log_file, start_line, end_line),
                                    get_time(2, log_file, start_line, end_line),
                                    get_phase_progress(3, 6, log_file, start_line, end_line),
                                    get_time(3, log_file, start_line, end_line),
                                    get_phase_progress(4, 1, log_file, start_line, end_line),
                                    get_time(4, log_file, start_line, end_line),
                                    f"{running_time.days * 24 + running_time.hours:02d}h{running_time.minutes:02d}m"
                                    ])

# print()

if len(final_completed_table) > 1 and args.completed_plots:
    if args.sort[0] == 'p': final_completed_table[1:] = sorted(final_completed_table[1:], key=itemgetter(1))
    if args.sort[0] == 't': final_completed_table[1:] = sorted(final_completed_table[1:], key=itemgetter(-1))
    tab_align = ['left', 'left', 'left', 'left', 'left', 'left', 'left', 'center', 'center', 'center', 'center',
                 'center', 'center']
    print(tabulate(final_completed_table, colalign=tab_align, headers="firstrow", tablefmt=args.tabfmt))

if len(final_running_table) > 1:
    if args.sort[0] == 'p': final_running_table[1:] = sorted(final_running_table[1:], key=itemgetter(1))
    if args.sort[0] == 't': final_running_table[1:] = sorted(final_running_table[1:], key=itemgetter(-1))
    tab_align = ['left', 'left', 'left', 'left', 'left', 'left', 'center', 'center', 'center', 'center', 'center',
                 'center', 'center', 'center', 'center']
    print(tabulate(final_running_table, colalign=tab_align, headers="firstrow", tablefmt=args.tabfmt))
