#!/usr/bin/env python3

import subprocess
import os
import shutil


def main():

    n_cores = 20
    run_time = 5 * 60
    top_dir = '/fastdata/bop15hjb/colony_speed/'
    data_file = 'uts_salmon.dat'
    colony = 'colony2p.ifort.impi2015.out'

    os.chdir(top_dir)

    print('n_cores', 'iterations', 'run_time', 'iterations_per_second', sep=',')

    for i in range(1, n_cores+1):

        run_dir = '{}{}_core_run/'.format(top_dir, i)
        os.mkdir(run_dir)
        shutil.copy(top_dir + data_file, run_dir)
        shutil.copy(top_dir + colony, run_dir)
        os.chdir(run_dir)

        colony_cmd = 'mpirun -np {} ./colony2p.ifort.impi2015.out IFN:uts_salmon.dat &> colony.log.txt'.format(i)

        try:
            subprocess.call(colony_cmd, shell=True, timeout=run_time)
        except subprocess.TimeoutExpired:
            pass

        # get iterations
        grep = "grep Itr= colony.log.txt | tail -n1 | cut -d ',' -f 3 | cut -d '=' -f 2"
        itr = subprocess.Popen(grep, shell=True, stdout=subprocess.PIPE).communicate()[0].decode().split('\n')[0]
        it_ps = int(itr) / run_time

        print(i, itr, run_time, it_ps, sep=',')

        os.chdir(top_dir)


if __name__ == '__main__':
    main()
