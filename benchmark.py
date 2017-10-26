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

def exec_proc(args):
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    p.wait()
    return stdout.decode('utf')
    

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
        ('PacketMachine', 'task3', './bin/pm-task3'),
        ('libtins',       'task1', './bin/tins-task1'),
        ('libtins',       'task2', './bin/tins-task2'),
        ('libtins',       'task3', './bin/tins-task3'),
        ('GoPacket',      'task1', './bin/gopkt-task1'),
        ('GoPacket',      'task3', './bin/gopkt-task3'),
    ]

    for fpath in fpath_list:
        print('target: {}'.format(fpath))

        for lib_name, task_name, bpath in tasks:
            task_key = (lib_name, task_name, fpath)
            
            print(task_key, end=': ')
            sys.stdout.flush()

            if not os.path.exists(bpath):
                print('{} is not found, skip',format(bpath))
                continue
            
            for i in range(args.loop_num):
                micro_sec = int(exec_proc([bpath, fpath]).strip())
                results[task_key].append(micro_sec)
                
                print('.', end='')
                sys.stdout.flush()
                
            print('')
            
    print('done')

    res = collections.defaultdict(lambda: collections.defaultdict(dict))
    for (lib_name, task_name, fpath), ts_list in results.items():
        res[task_name][fpath][lib_name] = ts_list

    json.dump(res, open(args.output, 'w'))
    


if __name__ == '__main__': main()
