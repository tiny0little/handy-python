#!/usr/bin/python3

import subprocess
from halo import Halo
import time
from typing import List

blockchain_src = '/home/user/src'
timeout_cmd = 'timeout 5'
blockchain_list = []


def wallet_service(blockchain: str, cmd: str):
    blockchain_name = blockchain.split('-')[0].strip()
    blockchain_path = f'{blockchain_src}/{blockchain}'

    str0 = f"cd {blockchain_path} && . ./activate && {timeout_cmd} {blockchain_name} {cmd} wallet-only"
    with Halo(text=f'{blockchain_name} wallet - {cmd}', color='white'): subprocess.getoutput(str0)


def farm_state(blockchain: str, info: str, cmd: str) -> str:
    blockchain_name = blockchain.split('-')[0].strip()
    blockchain_path = f'{blockchain_src}/{blockchain}'

    str0 = f"cd {blockchain_path} && . ./activate && {timeout_cmd} {blockchain_name} " \
           f" farm summary 2> /dev/null | grep '{cmd}'"
    with Halo(text=info, color='white'): result = subprocess.getoutput(str0).split(':')[1].strip()
    return result


str0 = f"cd {blockchain_src} && ls | grep blockchain | sort"
if int(subprocess.getoutput(f"{str0} | wc -l")) > 0: blockchain_list = subprocess.getoutput(f"{str0}").split('\n')

for blockchain0 in blockchain_list:
    blockchain_path = f'{blockchain_src}/{blockchain0}'
    blockchain_name = blockchain0.split('-')[0].strip()

    wallet_service(blockchain0, 'start')

    fingerprints = []
    str0 = f"cd {blockchain_path} && . ./activate && {timeout_cmd} {blockchain_name} keys show | grep Fingerprint"
    with Halo(text=f'getting fingerprints for {blockchain_name}', color='white'):
        tmp0 = subprocess.getoutput(str0).split('\n')
        for tmp1 in tmp0: fingerprints.append(tmp1.split(':')[1].strip())

    for fingerprint in fingerprints:

        str0 = f"cd {blockchain_path} && . ./activate && {timeout_cmd} {blockchain_name} wallet show -f {fingerprint}"
        with Halo(text=f'waiting for {blockchain_name}/{fingerprint} wallet to sync', color='white'):
            while int(subprocess.getoutput(f'{str0} | grep "Sync status: Synced" | wc -l')) != 1: time.sleep(30)

        # str0 = f"cd {blockchain_path} && . ./activate && {timeout_cmd} {blockchain_name} wallet show -f {fingerprint}"
        with Halo(text=f'getting balance of {blockchain_name}/{fingerprint} wallet', color='white'):
            str1 = subprocess.getoutput(f'{str0} | grep Spendable | head -1').split(':')[1].split('(')[0].strip()
        print(f'{blockchain_name}/{fingerprint}: {str1}')

    tmp0 = farm_state(blockchain0, f'getting expected time to win for {blockchain_name}', 'Expected time to win')
    print(f'{blockchain_name} expected time to win: {tmp0}')

    tmp0 = farm_state(blockchain0, f'getting expected time to win for {blockchain_name}', 'Estimated network space')
    print(f'{blockchain_name} network space: {tmp0}')

    wallet_service(blockchain0, 'stop')
    print()
