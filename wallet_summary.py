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


def crypto_service(blockchain: str, service: str, cmd: str):
    blockchain_name = blockchain.split('-')[0].strip()
    blockchain_path = f'{blockchain_src}/{blockchain}'

    str0 = f"cd {blockchain_path} && . ./activate && {timeout_cmd} {blockchain_name} {cmd} {service}"
    with Halo(text=f'{cmd}ing {blockchain_name} {service}', color='white'): subprocess.getoutput(str0)


def farm_state(blockchain: str, info: str, cmd: str) -> str:
    blockchain_name = blockchain.split('-')[0].strip()
    blockchain_path = f'{blockchain_src}/{blockchain}'

    str0 = f"cd {blockchain_path} && . ./activate && {timeout_cmd} {blockchain_name} " \
           f" farm summary 2> /dev/null | grep '{cmd}'"
    with Halo(text=info, color='white'): result = subprocess.getoutput(str0).split(':')[1].strip()
    return result


str0 = f'cd {blockchain_src} && ls | egrep blockchain | sort '
if args.crypto is not None: str0 += f" | egrep '{args.crypto}'"
if int(subprocess.getoutput(f"{str0} | wc -l")) > 0: blockchain_list = subprocess.getoutput(f"{str0}").split('\n')

tabula_row1 = []
tabula_row2 = []
for blockchain0 in blockchain_list:
    blockchain_path = f'{blockchain_src}/{blockchain0}'
    blockchain_name = blockchain0.split('-')[0].strip()

    crypto_service(blockchain0, 'node', 'start')
    crypto_service(blockchain0, 'wallet-only', 'start')
    if blockchain_name != 'chia': crypto_service(blockchain0, 'farmer-no-wallet', 'start')

    fingerprints = []
    str0 = f"cd {blockchain_path} && . ./activate && {timeout_cmd} {blockchain_name} keys show | grep Fingerprint"
    with Halo(text=f'getting fingerprints for {blockchain_name}', color='white'):
        tmp0 = subprocess.getoutput(str0).split('\n')
        for tmp1 in tmp0: fingerprints.append(tmp1.split(':')[1].strip())

    for fingerprint in fingerprints:

        str0 = f"cd {blockchain_path} && . ./activate && {timeout_cmd} {blockchain_name} wallet show -f {fingerprint}"
        with Halo(text=f'waiting for {blockchain_name}/{fingerprint} wallet to sync', color='white'):
            while int(subprocess.getoutput(f'{str0} | grep "Sync status: Synced" | wc -l')) != 1: time.sleep(30)
        with Halo(text=f'getting balance of {blockchain_name}/{fingerprint} wallet', color='white'):
            str1 = subprocess.getoutput(f'{str0} | grep Spendable | head -1').split(':')[1].split('(')[0].strip()
            str1 = str1.split(' ')[0].strip()
        if args.verbose: print(f'{colorWHITEonPURPLE}{blockchain_name}/{fingerprint}{colorENDC}: {str1}')

        tabula_row1.append(f'{blockchain_name}')
        tabula_row2.append(f'{str1}')

    tmp0 = farm_state(blockchain0, f'getting expected time to win for {blockchain_name}', 'Expected time to win')
    if args.verbose: print(f'expected time to win: {tmp0}')

    tmp0 = farm_state(blockchain0, f'getting expected time to win for {blockchain_name}', 'Estimated network space')
    if args.verbose: print(f'network space: {tmp0}')

    crypto_service(blockchain0, 'wallet-only', 'stop')
    if args.verbose: print()

tabula.append(tabula_row1)
tabula.append(tabula_row2)
print(tabulate(tabula, headers="firstrow", tablefmt="pretty"))
