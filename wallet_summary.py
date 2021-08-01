#!/usr/bin/python3

import argparse
import subprocess
from halo import Halo
import time

blockchain_src = '/home/user/src'
blockchain_list = []

parser = argparse.ArgumentParser(description="CHIA forks wallets ")
parser.add_argument("-s", "--show", help="show all wallets", action="store_true")
args = parser.parse_args()

str0 = f"cd {blockchain_src} && ls | grep blockchain | sort"
if int(subprocess.getoutput(f"{str0} | wc -l")) > 0:
    tmp_list = subprocess.getoutput(f"{str0}").split('\n')
    for tmp0 in tmp_list:
        blockchain_list.append([tmp0.split('-')[0], tmp0])
else:
    print('ERROR: no blockchain directories found')
    exit()


if args.show:
    for blockchain0 in blockchain_list:
        if blockchain0[0] == 'chaingreen': continue

        str0 = f"cd {blockchain_src}/{blockchain0[1]} && . ./activate && {blockchain0[0]} start wallet-only"
        with Halo(text=f'starting {blockchain0[0]} wallet', color='white'):
            subprocess.getoutput(str0)

        if blockchain0[0] == 'chia':
            str0 = f"cd {blockchain_src}/{blockchain0[1]} && . ./activate && {blockchain0[0]} wallet show -f 911097432"
            with Halo(text=f'waiting for {blockchain0[0]} 911097432 wallet to sync', color='white'):
                while int(subprocess.getoutput(f'{str0} | grep "Sync status: Synced" | wc -l')) != 1: time.sleep(60)

            str0 = f"cd {blockchain_src}/{blockchain0[1]} && . ./activate && {blockchain0[0]} wallet show f 911097432"
            with Halo(text=f'getting balance of {blockchain0[0]} wallet', color='white'):
                str1 = subprocess.getoutput(f'{str0} | grep Spendable | head -1').split(':')[1].split('(')[0].strip()
            print(f'{blockchain0[0]}: {str1}')

            str0 = f"cd {blockchain_src}/{blockchain0[1]} && . ./activate && {blockchain0[0]} wallet show -f 2876418895"
            with Halo(text=f'waiting for {blockchain0[0]} 2876418895 wallet to sync', color='white'):
                while int(subprocess.getoutput(f'{str0} | grep "Sync status: Synced" | wc -l')) != 1: time.sleep(60)

            str0 = f"cd {blockchain_src}/{blockchain0[1]} && . ./activate && {blockchain0[0]} wallet show f 2876418895"
            with Halo(text=f'getting balance of {blockchain0[0]} wallet', color='white'):
                str1 = subprocess.getoutput(f'{str0} | grep Spendable | head -1').split(':')[1].split('(')[0].strip()
            print(f'{blockchain0[0]}: {str1}')

        else:
            str0 = f"cd {blockchain_src}/{blockchain0[1]} && . ./activate && {blockchain0[0]} wallet show"
            with Halo(text=f'waiting for {blockchain0[0]} wallet to sync', color='white'):
                while int(subprocess.getoutput(f'{str0} | grep "Sync status: Synced" | wc -l')) != 1: time.sleep(60)

            str0 = f"cd {blockchain_src}/{blockchain0[1]} && . ./activate && {blockchain0[0]} wallet show"
            with Halo(text=f'getting balance of {blockchain0[0]} wallet', color='white'):
                str1 = subprocess.getoutput(f'{str0} | grep Spendable | head -1').split(':')[1].split('(')[0].strip()
            print(f'{blockchain0[0]}: {str1}')

        str0 = f"cd {blockchain_src}/{blockchain0[1]} && . ./activate && {blockchain0[0]} stop wallet-only"
        with Halo(text=f'stopping {blockchain0[0]} wallet', color='white'):
            subprocess.getoutput(str0)
