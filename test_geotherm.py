#!/usr/bin/python3
# coding: utf-8
"""
this is test_geotherm.py
"""
import os
import numpy as np
from geotherm import process_data
from geotherm import process_j
from geotherm import geot


def test_process_data():
    "this is test function of process_data"
    dftest = process_data('testbuilding')
    assert list(dftest.columns) == [
        'osm_id', 'name', 'type', 'geometry', 'coordpoints', 'surf', 'centro',
        'geot', 'valeurseuil'
    ]
    assert len(dftest) == 100


def test_process_j():
    "this is test function of process_j"
    dfo = process_data('testoccsol')
    dfb = process_data('testbuilding')
    yes = []
    temp, yes = process_j(dfo, dfb, 1, 2, yes)
    assert len(temp) > 0
    assert len(yes) == 0


def test_geot():
    "this is test function of geot"
    dfb = geot('testbuilding', 'testoccsol')
    os.remove('buildingeot')
    assert list(dfb.columns) == [
        'osm_id', 'name', 'type', 'geometry', 'coordpoints', 'surf', 'centro',
        'geot', 'valeurseuil'
    ]
    assert dfb['geot'].unique() == np.array(['no'])
