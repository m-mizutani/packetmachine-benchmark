#!/usr/bin/env python

import argparse
import subprocess
import os

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
    args = psr.parse_args()
    
    fpath_list = get_test_data_path()
    tasks = [
        ('PacketMachine', 'task1', './bin/pm-task1'),
        ('PacketMachine', 'task2', './bin/pm-task2'),
        ('libtins',       'task1', './bin/tins-task1'),
        ('libtins',       'task2', './bin/tins-task2'),
    ]

    for fpath in fpath_list:
        for task, task_name, bpath in tasks:
            for i in range(args.loop_num):
                p = subprocess.Popen([bpath, fpath], stdout=subprocess.PIPE)
                stdout, stderr = p.communicate()
                p.wait()
                print(stdout)
            
    print('done')

if __name__ == '__main__': main()
