from os.path import abspath, dirname, join
import numpy as np
import pandas as pd
import pyinform as pi


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


def main():
    fname = join(dirname(abspath(__file__)), "..", "data", "series.csv")
    data = pd.read_csv(fname)

    cellids = data.cellid.unique()

    mi = []
    for i in cellids:
        x = list(data[data.cellid == i].S)
        for j in cellids:
            y = list(data[data.cellid == j].S)
            value = sig_mutual_info(x, y, nperm=100)
            mi.append({'source': i, 'target': j, 'value': value})

    print(pd.DataFrame(mi))


if __name__ == '__main__':
    main()
