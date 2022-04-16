#!/usr/bin/python3
# coding: utf-8
"""
this is stations.py
"""
import argparse
import pandas as pd
import numpy as np
import scipy.spatial
from planning import Planning


def process_data(csv):
    "process csv to a dataframe and returns it"
    dfproc = pd.read_csv(csv, sep="#")
    dfproc = dfproc.astype('string')
    dfproc = dfproc.drop(len(dfproc) - 1)

    def coord(row):
        row['coordpoints'] = Planning.deccoord(row['geometry'])
        print(row)
        return row

    def surf(row):
        row['surf'] = Planning.fonction(row['coordpoints'])
        print(row)
        return row

    def centro(row):
        row['centro'] = Planning.centroide(row['coordpoints'])
        print(row)
        return row

    dfproc = dfproc.apply(coord, axis=1)
    dfproc = dfproc.apply(surf, axis=1)
    dfproc = dfproc.apply(centro, axis=1)
    return dfproc


def p2g(stationscsv, occsol):
    'return stationscsv with "oui" on stations accepting renewables'
    dfstations = process_data(stationscsv)
    dfstations['p2g'] = 'no'
    dfocs = process_data(occsol)
    index = 0
    end = len(dfstations)
    for i in range(len(dfstations)):
        known_xy = np.stack(dfocs['centro'].values)
        tree = scipy.spatial.cKDTree(known_xy)
        query_xy = np.stack(dfstations.loc[i, 'centro'])
        # pylint: disable=unused-variable
        distances, indices = tree.query(query_xy, k=10)
        for j in indices:
            dist = Planning.distancepoint(
                (dfstations.loc[i, 'centro'], dfocs.loc[j, 'centro']))
            if dfocs.loc[j, 'surf'] >= 12000 and dist <= 1000:
                dfstations.loc[i, 'p2g'] = "yes"
        index += 1
        print(f"avancement : {occsol} {index}/{end}")
    dfstations.to_csv(f'{stationscsv}p2g', sep='#', index=False)
    return dfstations

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='python stations.py -s stations.csv -o occsol.csv')
    parser.add_argument(
        '-s',
        '--stations',
        required=True,
        metavar='stations.csv',
        type=str,
        help='stations csvfile to process')
    parser.add_argument(
        '-o',
        '--occsol',
        required=True,
        metavar='occsol.csv',
        type=str,
        help='land coverage.csv to process')
    args = vars(parser.parse_args())
    p2g(args['stations'], args['occsol'])
