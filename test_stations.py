#!/usr/bin/python3
# coding: utf-8
"""
this is test_stations.py
"""
import os
import numpy as np
from stations import process_data
from stations import p2g


def test_process_data():
    "this is test function of process_data"
    dftest = process_data('testbuilding')
    assert list(dftest.columns) == [
        'osm_id', 'name', 'type', 'geometry', 'coordpoints', 'surf', 'centro'
    ]
    assert len(dftest) == 100


def test_p2g():
    "this is test function of p2g"
    dftest = p2g('testcarfuel', 'testoccsol')
    assert list(dftest.columns) == [
        'osm_id', 'name', 'type', 'geometry', 'coordpoints', 'surf', 'centro',
        'p2g'
    ]
    assert len(dftest) == 100
    assert dftest['p2g'].unique() == np.array(['no'])
    os.remove('testcarfuelp2g')
