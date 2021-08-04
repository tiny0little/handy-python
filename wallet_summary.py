#!/usr/bin/python3

import subprocess
from halo import Halo
import time
import argparse
from tabulate import tabulate

colorENDC = '\033[0m'
colorBOLD = '\033[1m'
colorWHITEonPURPLE = '\33[45m'
colorWHITEonGREEN = '\33[42m'
colorWHITEonBLUE = '\33[44m'

blockchain_src = '/home/user/src'
timeout_cmd = 'timeout 5'
blockchain_list = []
tabula = []

parser = argparse.ArgumentParser(description="crypto wallets")
parser.add_argument("-c", "--crypto", type=str, help="part of the name of cryptocurrency")
parser.add_argument("-v", "--verbose", action="store_true", help="show more")
args = parser.parse_args()


def crypto_service(blockchain: str, cmd: str, service: str, halo: bool):
    blockchain_name = blockchain.split('-')[0].strip()
    blockchain_path = f'{blockchain_src}/{blockchain}'

    str0 = f"cd {blockchain_path} && . ./activate && {timeout_cmd} {blockchain_name} {cmd} {service}"
    if halo:
        with Halo(text=f'{cmd}ing {blockchain_name} {service}', color='white'):
            subprocess.getoutput(str0)
    else:
        subprocess.getoutput(str0)


def farm_state(blockchain: str, grep: str, info: str) -> str:
    blockchain_name = blockchain.split('-')[0].strip()
    blockchain_path = f'{blockchain_src}/{blockchain}'

    str0 = f"cd {blockchain_path} && . ./activate && {timeout_cmd} {blockchain_name} " \
           f" farm summary 2> /dev/null | grep '{grep}'"
    with Halo(text=info, color='white'): result = subprocess.getoutput(str0).split(':')[1].strip()
    return result


def time_converter(s: str) -> str:
    s = s.replace(' and', '')
    s = s.replace(' minutes', 'm')
    s = s.replace(' minute', 'm')
    s = s.replace(' hours', 'h')
    s = s.replace(' hour', 'h')
    s = s.replace(' days', 'd')
    s = s.replace(' day', 'd')
    s = s.replace(' ', '')
    return s


def space_converter(s: str) -> str:
    unit = s.split(' ')[1].strip()
    num = s.split(' ')[0].strip()
    return f'{float(num):.0f}{unit}'


str0 = f'cd {blockchain_src} && ls | egrep blockchain | sort '
if args.crypto is not None: str0 += f" | egrep '{args.crypto}'"
if int(subprocess.getoutput(f"{str0} | wc -l")) > 0: blockchain_list = subprocess.getoutput(f"{str0}").split('\n')

tabula_rows = [[], [], [], []]
for blockchain0 in blockchain_list:
    blockchain_path = f'{blockchain_src}/{blockchain0}'
    blockchain_name = blockchain0.split('-')[0].strip()

    crypto_service(blockchain0, 'start', 'wallet-only -r', True)
    if blockchain_name != 'chia': crypto_service(blockchain0, 'start', 'farmer-no-wallet', True)
    time.sleep(30)

    fingerprints = []
    str0 = f"cd {blockchain_path} && . ./activate && {timeout_cmd} {blockchain_name} keys show | grep Fingerprint"
    with Halo(text=f'getting fingerprints for {blockchain_name}', color='white'):
        tmp0 = subprocess.getoutput(str0).split('\n')
        for tmp1 in tmp0: fingerprints.append(tmp1.split(':')[1].strip())

    for fingerprint in fingerprints:

        str0 = f"cd {blockchain_path} && . ./activate && {timeout_cmd} {blockchain_name} wallet show -f {fingerprint}"
        counter = 0
        with Halo(text=f'waiting for {blockchain_name}/{fingerprint} wallet to sync', color='white'):
            while int(subprocess.getoutput(f'{str0} | grep "Sync status: Synced" | wc -l')) != 1:
                time.sleep(120)
                counter += 1
                if counter > 2:
                    crypto_service(blockchain0, 'start', 'wallet-only -r', False)
                    counter = 0

        with Halo(text=f'getting balance of {blockchain_name}/{fingerprint} wallet', color='white'):
            str1 = subprocess.getoutput(f'{str0} | grep Spendable | head -1').split(':')[1].split('(')[0].strip()
            str1 = str1.split(' ')[0].strip()
        if float(str1) > 1:
            str1 = f'{float(str1):.0f}'
        else:
            str1 = f'{float(str1):.4f}'
        if args.verbose: print(f'{colorWHITEonPURPLE}{blockchain_name}/{fingerprint}{colorENDC}: {str1}')

        tabula_rows[0].append(f'{blockchain_name}')
        tabula_rows[1].append(f'{str1}')

    tmp0 = farm_state(blockchain0, 'Expected time to win', f'getting expected time to win for {blockchain_name}')
    tmp0 = time_converter(tmp0)
    if args.verbose: print(f'expected time to win: {tmp0}')
    for _ in range(len(fingerprints)): tabula_rows[2].append(f'{tmp0}')

    tmp0 = farm_state(blockchain0, 'Estimated network space', f'getting expected time to win for {blockchain_name}')
    tmp0 = space_converter(tmp0)
    if args.verbose: print(f'network space: {tmp0}')
    for _ in range(len(fingerprints)): tabula_rows[3].append(f'{tmp0}')

    crypto_service(blockchain0, 'stop', 'wallet-only', True)
    if args.verbose: print()

for row in tabula_rows: tabula.append(row)
tab_align = []
for _ in range(len(tabula[0])): tab_align.append('left')

print(tabulate(tabula, headers="firstrow", colalign=tab_align, tablefmt="pretty"))
