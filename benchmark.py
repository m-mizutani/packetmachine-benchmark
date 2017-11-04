#!/usr/bin/env python

import argparse
import subprocess
import os
import collections
import sys
import json
import platform
import psutil

def get_test_data_path():
    meta_fname = 'test_data_path.txt'
    if not os.path.exists(meta_fname):
        raise Exception('metafile "{0}" does not exist'.format(meta_fname))

    fpath_list = open(meta_fname, 'rt').read().strip().split('\n')
    for fpath in fpath_list:
        if not os.path.exists(meta_fname):
            raise Exception('test data file "{}" does not exist'.format(fpath))

    return fpath_list

def exec_proc(args):
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    p.wait()
    return stdout.decode('utf')


def benchmark(fpath_list, tasks, loop_num):
    results = collections.defaultdict(list)

    for fpath in fpath_list:
        print('target: {}'.format(fpath))

        for lib_name, task_name, bpath in tasks:
            task_key = (lib_name, task_name, fpath)
            
            print(task_key, end=': ')
            sys.stdout.flush()

            if not os.path.exists(bpath):
                print('{} is not found, skip',format(bpath))
                continue
            
            for i in range(loop_num):
                micro_sec = int(exec_proc([bpath, fpath]).strip())
                results[task_key].append(micro_sec)
                
                print('.', end='')
                sys.stdout.flush()
                
            print('')
            
    print('done')

    return results


def measure_basis(fpath_list, loop_num):
    os_info = os.uname()
    results = {
        'os': {
            'sysname': os_info.sysname,
            'release': os_info.release,
        },
        'cpu': {
            'freq': psutil.cpu_freq().current,
            'count': psutil.cpu_count(),
        },
        'memory': psutil.virtual_memory().total,
    }

    dataset = collections.defaultdict(lambda: {'read': [], 'count': 0, 'size': 0})
    for fpath in fpath_list:
        df_name = os.path.basename(fpath)
        for i in range(loop_num):
            lines = exec_proc(['./bin/readpcap', fpath]).split('\n')
            print(lines)
            dataset[df_name]['read'].append(int(lines[0]))
            dataset[df_name]['count'] = int(lines[1])
            dataset[df_name]['size'] = int(lines[2])

        dataset[df_name]['elapsed'] = min(dataset[df_name]['read'])

    results['dataset'] = dataset
    return results

def main():
    psr = argparse.ArgumentParser()
    psr.add_argument('-n', '--loop-num', type=int, default=5)
    psr.add_argument('-o', '--output', default='results.json')
    psr.add_argument('-b', '--base', default='base.json')
    args = psr.parse_args()

    tasks = [
        ('PacketMachine', 'task1', './bin/pm-task1'),
        ('PacketMachine', 'task2', './bin/pm-task2'),
        ('PacketMachine', 'task3', './bin/pm-task3'),
        ('libtins',       'task1', './bin/tins-task1'),
        ('libtins',       'task2', './bin/tins-task2'),
        ('libtins',       'task3', './bin/tins-task3'),
        ('GoPacket',      'task1', './bin/gopkt-task1'),
        ('GoPacket',      'task3', './bin/gopkt-task3'),
    ]
    fpath_list = get_test_data_path()
    base = measure_basis(fpath_list, args.loop_num)
    json.dump(base, open(args.base, 'w'))
              
    results = benchmark(fpath_list, tasks, args.loop_num)

    res = collections.defaultdict(lambda: collections.defaultdict(dict))
    for (lib_name, task_name, fpath), ts_list in results.items():
        df_name = os.path.basename(fpath)
        res[task_name][df_name][lib_name] = ts_list

    json.dump(res, open(args.output, 'w'))
    


if __name__ == '__main__': main()
