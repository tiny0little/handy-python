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
start_line = 1
final_completed_table = []
final_active_table = []
plot_size = []
phase1 = []
phase1time = []
phase2 = []
phase2time = []
phase3 = []
phase3time = []
phase4 = []
phase4time = []
running_time_tab = []


def phase_time(_phase_number):
    _output = subprocess.getoutput(f"awk 'NR >= {start_line}' {log_file} | egrep 'Time for phase {_phase_number}' "
                                   " | tail -1").split("seconds.")
    if len(_output) > 1:
        _output = int(float(_output[0].split("=")[1].strip()))
        _min, _sec = divmod(_output, 60)
        _hours, _min = divmod(_min, 60)
        return f"{_hours:02d}:{_min:02d}"
    else:
        return ""


#
#
final_completed_table.append([f"{colorWHITEonGREEN}{colorBOLD}COMPLETED PLOTS{colorENDC}", "k", ""])
log_files = glob.glob(f"{log_location}/*.log")
for log_file in log_files:

    # checking if any completed plots in the logfile
    line1 = 1
    line2 = 1
    output = subprocess.getoutput(f"grep -n 'Total time' {log_file}").split("\n")
    for line in output:
        line2 = line.split(":")[0].strip()
        if line2.isnumeric():
            plot_size0 = subprocess.getoutput(f"awk 'NR <= {line2} && NR >= {line1}' {log_file} "
                                              "| egrep 'Plot size is'").split(":")[1].strip()
            total_time = int(float(subprocess.getoutput(f"awk 'NR <= {line2} && NR >= {line1}' {log_file} | egrep "
                                                        "'Total time' ").split("seconds.")[0].strip().split("=")[
                                       1].strip()))
            min0, sec0 = divmod(total_time, 60)
            hours0, min0 = divmod(min0, 60)
            final_completed_table.append([os.path.basename(log_file), plot_size0, f"{hours0:02d}:{min0:02d}"])

    #
    # starting line of current plot
    start_line = int(subprocess.getoutput(f"egrep -n 'Starting plotting progress into temporary' {log_file} "
                                          "| tail -1").split(":")[0].strip())

    start_time = parse(subprocess.getoutput(f"awk 'NR >= {start_line}' {log_file} | egrep "
                                            "'Starting phase 1/4: Forward Propagation' "
                                            "| tail -1").split("...")[1].strip())
    running_time = relativedelta(datetime.now(), start_time)
    output = subprocess.getoutput(f"awk 'NR >= {start_line}' {log_file} | egrep 'Plot size is'")
    plot_size.append(output.split(":")[1].strip())

    #
    #
    output = subprocess.getoutput(f"awk 'NR >= {start_line}' {log_file} | egrep 'Computing table' | wc -l")
    if int(output) > 0:
        output1 = ""
        for i in range(int(output)): output1 += f"{i + 1},"
        phase1.append(output1[:-1])
    else:
        phase1.append("")

    #
    #
    phase1time.append(phase_time(1))

    #
    #
    output = subprocess.getoutput(f"awk 'NR >= {start_line}' {log_file} | egrep 'Backpropagating on table' | wc -l")
    if int(output) > 0:
        output1 = ""
        for i in range(int(output)): output1 += f"{7 - i},"
        if output1[-2:] == "2,": output1 += "1,"
        phase2.append(output1[:-1])
    else:
        phase2.append("")

    #
    #
    phase2time.append(phase_time(2))

    #
    #
    output = subprocess.getoutput(f"awk 'NR >= {start_line}' {log_file} | egrep 'Compressing tables' | wc -l")
    if int(output) > 0:
        output1 = ""
        for i in range(int(output)): output1 += f"{1 + i},"
        phase3.append(output1[:-1])
    else:
        phase3.append("")

    #
    #
    phase3time.append(phase_time(3))

    #
    #
    output = subprocess.getoutput(f"awk 'NR >= {start_line}' {log_file} | egrep 'Starting phase 4/4' | wc -l")
    if int(output) > 0:
        phase4.append(".")
    else:
        phase4.append("")

    #
    #
    phase4time.append(phase_time(4))

    #
    #
    running_time_tab.append(f"{running_time.days * 24 + running_time.hours:02d}:{running_time.minutes:02d}")

final_active_table.append([f"{colorWHITEonBLUE}{colorBOLD}RUNNING PLOTS{colorENDC}", "k", "p1", "p1 time", "p2", "p2 time", "p3", "p3 time", "p4", "p4 time", "runtime"])
for i in range(len(log_files)):
    final_active_table.append([os.path.basename(log_files[i]), plot_size[i], phase1[i], phase1time[i],
                               phase2[i], phase2time[i], phase3[i], phase3time[i], phase4[i], phase4time[i],
                               running_time_tab[i]])

tab_align = ['left', 'left', 'right']
print(tabulate(final_completed_table, colalign=tab_align, headers="firstrow", tablefmt="pretty"))
print()
tab_align = ['left', 'left', 'right', 'left', 'right', 'left', 'right', 'left', 'right', 'left', 'left']
print(tabulate(final_active_table, colalign=tab_align, headers="firstrow", tablefmt="pretty"))
