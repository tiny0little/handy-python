#!/usr/bin/python3.8

import glob
import subprocess
from dateutil.parser import *
from dateutil.relativedelta import relativedelta
from datetime import *
from tabulate import tabulate
import os

colorGREEN = '\033[92m'
colorYELLOW = '\033[93m'
colorRED = '\033[91m'
colorENDC = '\033[0m'
colorBOLD = '\033[1m'
colorWHITEonPURPLE = '\33[45m'
colorWHITEonGREEN = '\33[42m'
colorWHITEonBLUE = '\33[44m'
colorWHITEonRED = '\33[41m'

log_location = "/home/user/.chia/mainnet/plotter"
final_completed_table = []
final_active_table = []

def get_phase_time(_phase_number, _log_file, _start_line, _end_line):
    _output0 = subprocess.getoutput(
        f"awk 'NR >= {_start_line} && NR <= {_end_line}' {_log_file} | egrep 'Time for phase {_phase_number}' "
        " | tail -1").split("seconds.")
    _output1 = ""
    if len(_output0) > 1:
        _output0 = int(float(_output0[0].split("=")[1].strip()))
        _min, _sec = divmod(_output0, 60)
        _hours, _min = divmod(_min, 60)
        _output1 = f"{_hours:02d}h{_min:02d}m"
    return _output1


def get_phase_progress(_phase_number, _log_file, _start_line, _end_line):
    _search_text = "zzzzzzzzzzzzzzzzz"
    if _phase_number == 1: _search_text = "Computing table"
    if _phase_number == 2: _search_text = "Backpropagating on table"
    if _phase_number == 3: _search_text = "Compressing tables"
    if _phase_number == 4: _search_text = "Starting phase 4/4"
    _output0 = int(subprocess.getoutput(
        f"awk 'NR >= {_start_line} && NR <= {_end_line}' {_log_file} | egrep '{_search_text}' | wc -l"))
    _output1 = ""
    if _output0 > 0:
        for _i in range(int(_output0)): _output1 += "#"
        for _i in range(6 - int(_output0)): _output1 += "."
    return _output1


def get_total_time(_log_file, _start_line, _end_line):
    _output = int(float(subprocess.getoutput(f"awk 'NR >= {_start_line} && NR <= {_end_line}' {_log_file} "
                                             "| egrep 'Total time' ").split("seconds.")[0].strip().split(
        "=")[1].strip()))
    _min, _sec = divmod(_output, 60)
    _hours, _min = divmod(_min, 60)
    return f"{_hours:02d}h{_min:02d}m"


def get_plot_size(_log_file, _start_line, _end_line):
    _output = subprocess.getoutput(f"awk 'NR >= {_start_line} && NR <= {_end_line}' {_log_file} "
                                   "| egrep 'Plot size is'").split(":")[1].strip()
    return _output


#
#
final_completed_table.append(
    [f"{colorWHITEonGREEN}{colorBOLD}COMPLETED PLOTS{colorENDC}", "k", "p1 time", "p2 time", "p3 time", "p4 time",
     "total time"])
final_active_table.append([f"{colorWHITEonBLUE}{colorBOLD}RUNNING PLOTS{colorENDC}", "k", "p1", "p1 time",
                           "p2", "p2 time", "p3", "p3 time", "p4", "p4 time", "runtime"])
log_files = glob.glob(f"{log_location}/*.log")
for log_file in log_files:

    start_line = 1
    end_line = 1

    # checking if any completed plots in the logfile
    output = subprocess.getoutput(f"grep -n 'Total time' {log_file}").split("\n")
    for line in output:
        end_line0 = line.split(":")[0].strip()
        if end_line0.isnumeric():
            end_line = int(end_line0)
            final_completed_table.append(
                [os.path.basename(log_file), get_plot_size(log_file, start_line, end_line),
                 get_phase_time(1, log_file, start_line, end_line),
                 get_phase_time(2, log_file, start_line, end_line),
                 get_phase_time(3, log_file, start_line, end_line),
                 get_phase_time(4, log_file, start_line, end_line),
                 get_total_time(log_file, start_line, end_line)])

        start_line = end_line + 1

    #
    # processing currently running plot
    start_line = int(subprocess.getoutput(f"egrep -n 'Starting plotting progress into temporary' {log_file} "
                                          "| tail -1").split(":")[0].strip())
    end_line = int(subprocess.getoutput(f"cat {log_file} | wc -l").strip())

    start_time = parse(subprocess.getoutput(f"awk 'NR >= {start_line}' {log_file} | egrep "
                                            "'Starting phase 1/4: Forward Propagation' "
                                            "| tail -1").split("...")[1].strip())
    running_time = relativedelta(datetime.now(), start_time)

    final_active_table.append([os.path.basename(log_file), get_plot_size(log_file, start_line, end_line),
                               get_phase_progress(1, log_file, start_line, end_line),
                               get_phase_time(1, log_file, start_line, end_line),
                               get_phase_progress(2, log_file, start_line, end_line),
                               get_phase_time(2, log_file, start_line, end_line),
                               get_phase_progress(3, log_file, start_line, end_line),
                               get_phase_time(3, log_file, start_line, end_line),
                               get_phase_progress(4, log_file, start_line, end_line),
                               get_phase_time(4, log_file, start_line, end_line),
                               f"{running_time.days * 24 + running_time.hours:02d}h{running_time.minutes:02d}m"
                               ])


tab_align = ['left', 'left', 'center', 'center', 'center', 'center', 'center']
print(tabulate(final_completed_table, colalign=tab_align, headers="firstrow", tablefmt="pretty"))

tab_align = ['left', 'left', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center', 'center']
print(tabulate(final_active_table, colalign=tab_align, headers="firstrow", tablefmt="pretty"))
