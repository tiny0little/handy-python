#!/usr/bin/python3

import subprocess
from halo import Halo
import time

blockchain_src = '/home/user/src'
timeout_cmd = 'timeout 5'
blockchain_list = []

str0 = f"cd {blockchain_src} && ls | grep blockchain | sort"
if int(subprocess.getoutput(f"{str0} | wc -l")) > 0:
    tmp_list = subprocess.getoutput(f"{str0}").split('\n')
    for tmp0 in tmp_list:
        blockchain_list.append([tmp0.split('-')[0], tmp0])
else:
    print('ERROR: no blockchain directories found')
    exit()

for blockchain0 in blockchain_list:
    path = f'{blockchain_src}/{blockchain0[1]}'

    str0 = f"cd {path} && . ./activate && {timeout_cmd} {blockchain0[0]} start wallet-only"
    with Halo(text=f'starting {blockchain0[0]} wallet', color='white'):
        subprocess.getoutput(str0)

    fingerprints = []
    str0 = f"cd {path} && . ./activate && {timeout_cmd} {blockchain0[0]} keys show | grep Fingerprint"
    with Halo(text=f'getting fingerprints for {blockchain0[0]}', color='white'):
        tmp0 = subprocess.getoutput(str0).split('\n')
        for tmp1 in tmp0: fingerprints.append(tmp1.split(':')[1].strip())

    for fingerprint in fingerprints:

        str0 = f"cd {path} && . ./activate && {timeout_cmd} {blockchain0[0]} wallet show -f {fingerprint}"
        with Halo(text=f'waiting for {blockchain0[0]}/{fingerprint} wallet to sync', color='white'):
            while int(subprocess.getoutput(f'{str0} | grep "Sync status: Synced" | wc -l')) != 1: time.sleep(30)

        str0 = f"cd {path} && . ./activate && {timeout_cmd} {blockchain0[0]} wallet show -f {fingerprint}"
        with Halo(text=f'getting balance of {blockchain0[0]}/{fingerprint} wallet', color='white'):
            str1 = subprocess.getoutput(f'{str0} | grep Spendable | head -1').split(':')[1].split('(')[0].strip()
        print(f'{blockchain0[0]}/{fingerprint}: {str1}')

    str0 = f"cd {path} && . ./activate && {timeout_cmd} {blockchain0[0]} stop wallet-only"
    with Halo(text=f'stopping {blockchain0[0]} wallet', color='white'):
        subprocess.getoutput(str0)
