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

log_location = "/home/user/.chia/mainnet/plotter"
final_completed_table = []
final_running_table = []


def get_time(_str: str, _log_file: str, _start_line: int, _end_line: int) -> str:
    _output0 = subprocess.getoutput(
        f"awk 'NR >= {_start_line} && NR <= {_end_line}' {_log_file} | egrep '{_str}' | tail -1").split("seconds.")
    _output1 = ""
    if len(_output0) > 1:
        _output0 = int(float(_output0[0].split("=")[1].strip()))
        _min, _sec = divmod(_output0, 60)
        _hours, _min = divmod(_min, 60)
        _output1 = f"{_hours:02d}h{_min:02d}m"
    return _output1


# adds two times
def get_time2(_str1: str, _str2: str, _log_file: str, _start_line: int, _end_line: int) -> str:
    _output1 = subprocess.getoutput(
        f"awk 'NR >= {_start_line} && NR <= {_end_line}' {_log_file} | egrep '{_str1}' | tail -1").split("seconds.")
    _output2 = subprocess.getoutput(
        f"awk 'NR >= {_start_line} && NR <= {_end_line}' {_log_file} | egrep '{_str2}' | tail -1").split("seconds.")
    _final_output = ""
    if len(_output1) > 1 and len(_output2) > 1:
        _output0 = int(float(_output1[0].split("=")[1].strip())) + int(float(_output2[0].split("=")[1].strip()))
        _min, _sec = divmod(_output0, 60)
        _hours, _min = divmod(_min, 60)
        _final_output = f"{_hours:02d}h{_min:02d}m"
    return _final_output


def get_phase_progress(_search_text: str, _steps: int, _log_file, _start_line: int, _end_line: int) -> str:
    _output0 = int(subprocess.getoutput(
        f"awk 'NR >= {_start_line} && NR <= {_end_line}' {_log_file} | egrep '{_search_text}' | wc -l"))
    _output1 = ""
    if _output0 > 0:
        for _i in range(int(_output0)): _output1 += "#"
        for _i in range(_steps - int(_output0)): _output1 += "."
    return _output1


def get_plot_size(_log_file: str, _start_line: int, _end_line: int) -> str:
    _output = "??"
    _str = f"awk 'NR >= {_start_line} && NR <= {_end_line}' {_log_file} | egrep 'Plot size is'"
    if int(subprocess.getoutput(f"{_str} | wc -l")) > 0:
        _output = subprocess.getoutput(f"{_str}").split(":")[1].strip()
    return _output


def get_buckets(_log_file: str, _start_line: int, _end_line: int) -> str:
    _output = "??"
    _str = f"awk 'NR >= {_start_line} && NR <= {_end_line}' {_log_file} | egrep 'Using [0-9]+ buckets'"
    if int(subprocess.getoutput(f"{_str} | wc -l")) > 0:
        _output = subprocess.getoutput(f"{_str}").split("Using")[1].split("buckets")[0].strip()
    return _output


def get_buffer_size(_log_file: str, _start_line: int, _end_line: int) -> str:
    _output = "??"
    _str = f"awk 'NR >= {_start_line} && NR <= {_end_line}' {_log_file} | egrep 'Buffer size is: [0-9]+MiB'"
    if int(subprocess.getoutput(f"{_str} | wc -l")) > 0:
        _output = subprocess.getoutput(f"{_str}").split("is:")[1].split("MiB")[0].strip()
    return _output


def get_temp_dir(_log_file: str, _start_line: int, _end_line: int) -> str:
    _output = "??"
    _str = f"awk 'NR >= {_start_line} && NR <= {_end_line}' {_log_file} | egrep 'progress into temporary dirs'"
    if int(subprocess.getoutput(f"{_str} | wc -l")) > 0:
        _output = subprocess.getoutput(f"{_str}").split(":")[1].strip()
        _output = _output.split("and")[0].strip() + "/"
    return _output


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
parser.add_argument("-d", "--dir", help=f"location of plot logs. default {log_location}")
parser.add_argument("-s", "--sort", choices=['plot', 'time'], nargs='?', default='plot', const='plot',
                    help="which column used for sorting the table? (default: %(default)s)")
parser.add_argument("-nc", "--nocolor", help="do not use colors", action="store_true")
args = parser.parse_args()

if args.dir is not None: log_location = args.dir

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
     "buffer", "p1 time", "p2 time", "p3 time", "p4 time", "cp time", "total"])
final_running_table.append(
    [f"{colorWHITEonBLUE}{colorBOLD}RUNNING PLOTS{colorENDC}", "temp", "k", "buckets", "buffer", "p1",
     "p1 time", "p2", "p2 time", "p3", "p3 time", "p4", "p4 time", "runtime"])
log_files = glob.glob(f"{log_location}/*log")

for log_file in log_files:

    start_line = 1
    end_line = 1

    #
    # processing completed plots
    #
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
                 get_time('Time for phase 1', log_file, start_line, end_line),
                 get_time('Time for phase 2', log_file, start_line, end_line),
                 get_time('Time for phase 3', log_file, start_line, end_line),
                 get_time('Time for phase 4', log_file, start_line, end_line),
                 get_time("Copy time", log_file, start_line, end_line),
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
                                get_phase_progress("Computing table", 7, log_file, start_line, end_line),
                                get_time('Time for phase 1', log_file, start_line, end_line),
                                get_phase_progress("Backpropagating on table", 6, log_file, start_line, end_line),
                                get_time('Time for phase 2', log_file, start_line, end_line),
                                get_phase_progress("Compressing tables", 6, log_file, start_line, end_line),
                                get_time('Time for phase 3', log_file, start_line, end_line),
                                get_phase_progress("Starting phase 4/4", 1, log_file, start_line, end_line),
                                get_time('Time for phase 4', log_file, start_line, end_line),
                                f"{running_time.days * 24 + running_time.hours:02d}h{running_time.minutes:02d}m"
                                ])

if len(final_completed_table) > 1:
    if args.sort == 'plot': final_completed_table[1:] = sorted(final_completed_table[1:], key=itemgetter(1))
    if args.sort == 'time': final_completed_table[1:] = sorted(final_completed_table[1:], key=itemgetter(-1))
    tab_align = ['left', 'left', 'left', 'left', 'left', 'left', 'center', 'center', 'center', 'center',
                 'center', 'center']
    print(tabulate(final_completed_table, colalign=tab_align, headers="firstrow", tablefmt="pretty"))

if len(final_running_table) > 1:
    if args.sort == 'plot': final_running_table[1:] = sorted(final_running_table[1:], key=itemgetter(1))
    if args.sort == 'time': final_running_table[1:] = sorted(final_running_table[1:], key=itemgetter(-1))
    tab_align = ['left', 'left', 'left', 'left', 'left', 'center', 'center', 'center', 'center', 'center',
                 'center', 'center', 'center', 'center']
    print(tabulate(final_running_table, colalign=tab_align, headers="firstrow", tablefmt="pretty"))
