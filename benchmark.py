#!/usr/bin/env python

import argparse
import subprocess
import os
import collections
import sys
import json

def get_test_data_path():
    meta_fname = 'test_data_path.txt'
    if not os.path.exists(meta_fname):
        raise Exception('metafile "{0}" does not exist'.format(meta_fname))

    fpath_list = open(meta_fname, 'rt').read().strip().split('\n')
    for fpath in fpath_list:
        if not os.path.exists(meta_fname):
            raise Exception('test data file "{}" does not exist'.format(fpath))

    return fpath_list

def main():
    psr = argparse.ArgumentParser()
    psr.add_argument('-n', '--loop-num', type=int, default=5)
    psr.add_argument('-o', '--output', default='results.json')
    args = psr.parse_args()

    results = collections.defaultdict(list)
    
    fpath_list = get_test_data_path()
    tasks = [
        ('PacketMachine', 'task1', './bin/pm-task1'),
        ('PacketMachine', 'task2', './bin/pm-task2'),
        ('libtins',       'task1', './bin/tins-task1'),
        ('libtins',       'task2', './bin/tins-task2'),
        ('GoPacket',      'task1', './bin/gopkt-task1'),
    ]

    for fpath in fpath_list:
        for task_key in tasks:
            lib_name, task_name, bpath = task_key
            
            print(task_key, end=': ')
            sys.stdout.flush()
            
            for i in range(args.loop_num):
                p = subprocess.Popen([bpath, fpath], stdout=subprocess.PIPE)
                stdout, stderr = p.communicate()
                p.wait()
                micro_sec = int(stdout.decode('utf').strip())
                results[task_key].append(micro_sec)
                
                print('.', end='')
                sys.stdout.flush()
                
            print('')
            
    print('done')

    res = collections.defaultdict(dict)
    for (lib_name, task_name, bpath), ts_list in results.items():
        res[task_name][lib_name] = ts_list

    json.dump(res, open(args.output, 'w'))
    


if __name__ == '__main__': main()
