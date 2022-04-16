#!/usr/bin/python3
# coding: utf-8
"""
this is geotherm.py
"""
import argparse
import scipy.spatial
import pandas as pd
import numpy as np
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
    dfproc['geot'] = 'no'
    dfproc['valeurseuil'] = 3 * ((dfproc['surf'] / 3.141592653589793)**(1 / 2))
    return dfproc


def process_j(dfo, dfb, i, j, yes):
    "process dfb and dfo in geot function to append 'oui' if distance to occsol is low"
    compteur = 0
    temp = []
    for point in dfo.loc[j, 'coordpoints']:
        dist = Planning.distancepoint([dfb.loc[i, 'centro'], point])
        temp.append(dist)
    for dist in temp:
        if dist < dfb.loc[i, 'valeurseuil']:
            compteur += 1
    if compteur >= 2 and dfo.loc[j, 'surf'] >= 1.5 * dfb.loc[i, 'surf']:
        # on enleve du potentiel à hypothese 1:1.5
        dfo.loc[j, 'surf'] -= 1.5 * dfb.loc[i, 'surf']
        dfb.loc[i, 'geot'] = 'yes'
        yes.append('yes')
    return temp, yes


def geot(building, occsol):
    "return building with 'oui' on buildings with gardens"
    dfb = process_data(building)
    dfo = process_data(occsol)

    index = 0
    end = len(dfb)
    yes = []
    for i in range(len(dfb)):
        known_xy = np.stack(dfo['centro'].values)
        tree = scipy.spatial.cKDTree(known_xy)
        query_xy = np.stack(dfb.loc[i, 'centro'])
        # pylint: disable=unused-variable
        distances, indices = tree.query(query_xy, k=5)
        for j in indices:  # 5 premiers polygones triés par distance croissante
            process_j(dfo, dfb, i, j, yes)
        index += 1
        print(f'avancement : {index}/{end}')
    dfb.to_csv('buildingeot', sep='#', index=False)
    return dfb

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='python geotherm.py -b building.csv -o occsol.csv')
    parser.add_argument(
        '-b',
        '--building',
        required=True,
        metavar='building.csv',
        type=str,
        help='building csvfile to process')
    parser.add_argument(
        '-o',
        '--occsol',
        required=True,
        metavar='occsol.csv',
        type=str,
        help='land coverage.csv to process')
    args = vars(parser.parse_args())
    geot(args['building'], args['occsol'])
