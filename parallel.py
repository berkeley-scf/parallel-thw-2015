#!/usr/bin/python

## @knitr python-mp

import multiprocessing as mp
import numpy as np

nCores = 4

nSmp = 10000000
m = 40
def f(input):
    np.random.seed(input[0])
    return np.mean(np.random.normal(0, 1, input[1]))

# create list of tuples to iterate over, since
# Pool.map() does not support multiple arguments
inputs = [(i, nSmp) for i in xrange(m)]
inputs[0:2]
pool = mp.Pool(processes = nCores)
results = pool.map(f, inputs)
print(results)


## @knitr python-mp-manualDispatch

# set up a shared object to store results
result_queue = mp.Queue()
def f(i, n, out):
    np.random.seed(i)
    # return both index and result as tuple to show how to do that
    out.put((i, np.mean(np.random.normal(0, 1, n))))
    

jobs = [] # list of processes
nProc = nCores # don't have more processes than cores available
for i in range(nCores): 
    p = mp.Process(target = f, args = (i, nSmp, result_queue))
    jobs.append(p)
    p.start()

# wait for results...
for p in jobs:
    p.join() 

results = [result_queue.get() for i in range(nCores)]


print(results)

## @knitr python-pp

import numpy
import pp

nCores = 4

job_server = pp.Server(ncpus = nCores, secret = 'mysecretphrase')
# set 'secret' to some passphrase (you need to set it but 
#   what it is should not be crucial)
job_server.get_ncpus()

nSmp = 10000000
m = 40
def f(i, n):
    numpy.random.seed(i)
    return (i, numpy.mean(numpy.random.normal(0, 1, n)))

# create list of tuples to iterate over
inputs = [(i, nSmp) for i in xrange(m)]
# submit and run jobs
jobs = [job_server.submit(f, invalue, modules = ('numpy',)) for invalue in inputs]
# jobs = [job_server.submit(f, invalue, modules = ('numpy',)) 
#    for invalue in inputs]
# collect results (will have to wait for longer tasks to finish)
results = [job() for job in jobs]
print(results)
job_server.destroy()


## @knitr python-mpi

from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD

# simple print out Rank & Size
id = comm.Get_rank()
print "Of ", comm.Get_size() , " workers, I am number " , id, "."

def f(id, n):
    np.random.seed(id)
    return np.mean(np.random.normal(0, 1, n))

n = 1000000
result = f(id, n)


output = comm.gather(result, root = 0)

if id == 0:
    print output
