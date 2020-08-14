from mpi4py import MPI
from os.path import abspath, dirname, join
import numpy as np
import pandas as pd
import pyinform as pi


def partition(xs, n):
    """
    Partition a list `xs` into `n` (almost) uniform partitions
    """
    N, M = len(xs) // n, len(xs) % n
    L = M * (N + 1)
    return [xs[i:i + N + 1] for i in range(0, L, N + 1)] + \
        [xs[L + i:L + i + N] for i in range(0, len(xs) - L, N)]


def flatten(xs):
    """
    Flatten a list of lists into a single list
    """
    ys = []
    for x in xs:
        ys += x
    return ys


def sig_mutual_info(xs, ys, alpha=0.05, nperm=1000):
    """
    Compute the mutual information between `xs` and `ys` using a permutation
    test to assess statistical significance.

    :param xs: first variable
    :param ys: second variable
    :param alpha: significance level
    :param nperm: number of permutations
    :return:
    """
    rng = np.random.default_rng()

    gt = pi.mutual_info(xs, ys)

    count = 0
    for _ in range(nperm):
        rng.shuffle(ys)
        count += (gt <= pi.mutual_info(xs, ys))

    p = count / (nperm + 1)

    return gt if p < alpha else 0.0


def evaluate(data, cellids_subset):
    cellids = data.cellid.unique()

    mi = []
    for i in cellids_subset:
        x = list(data[data.cellid == i].S)
        for j in cellids:
            y = list(data[data.cellid == j].S)
            value = sig_mutual_info(x, y, nperm=100)
            mi.append({'source': i, 'target': j, 'value': value})
    return mi


def root(comm):
    rank = comm.Get_rank()

    fname = join(dirname(abspath(__file__)), "..", "data", "series.csv")
    data = pd.read_csv(fname)

    cellids = list(data.cellid.unique())

    data = comm.bcast(data)

    cellids_subset = comm.scatter(partition(cellids, comm.Get_size()))
    mi = evaluate(data, cellids_subset)
    mi = comm.gather(mi)
    mi = flatten(mi)

    df = pd.DataFrame(mi)
    df.sort_values(['source', 'target'], inplace=True)
    print(df)


def worker(comm):
    rank = comm.Get_rank()

    data = comm.bcast(None)

    cellids_subset = comm.scatter(None)
    mi = evaluate(data, cellids_subset)
    mi = comm.gather(mi)


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        root(comm)
    else:
        worker(comm)


if __name__ == '__main__':
    main()
