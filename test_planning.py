#!/usr/bin/python3
# coding: utf-8
"""
this is test_planning.py
"""
from planning import Planning


def test_isdigitpoint():
    "test of isdigitpoint function"
    planning = Planning()
    assert planning.isdigitpoint('8') == 1
    assert planning.isdigitpoint('.') == 1
    assert planning.isdigitpoint('-') == 1
    assert planning.isdigitpoint('a') == 0


def test_deccoord():
    "test of deccoord function"
    planning = Planning()
    assert planning.deccoord('POINT (290225.2699306086 1843146.0906546437)'
                             ) == ((290225.2699306086, 1843146.0906546437), )
    assert planning.deccoord(
        'POLYGON ((510786.4962177546 1817685.9314593724, 510790.71072088345 1817685.3160891854, 510791.9470301377 1817692.4214629498, 510787.81372920994 1817693.035697252, 510786.4962177546 1817685.9314593724))'
    ) == ((510786.4962177546, 1817685.9314593724),
          (510790.71072088345, 1817685.3160891854), (510791.9470301377,
                                                     1817692.4214629498),
          (510787.81372920994, 1817693.035697252), (510786.4962177546,
                                                    1817685.9314593724))
    assert planning.deccoord(
        'LINESTRING (391234.6474115489 1859681.5432677385, 391197.1101810548 1859520.811951668)'
    ) == ((391234.6474115489, 1859681.5432677385), (391197.1101810548,
                                                    1859520.811951668))


def test_valeursabs():
    "test of valeursabs function"
    planning = Planning()
    assert planning.valeursabs(-1) == 1
    assert planning.valeursabs(-20) == 20


def test_distancepoint():
    "test of distancepoint function"
    planning = Planning()
    assert planning.distancepoint(((1, 1), (2, 2))) == 1.4142135623730951


def test_centroide():
    "test of centroide function"
    planning = Planning()
    assert planning.centroide(((0, 0), (0, 1), (1, 1), (1, 0))) == (0.5, 0.5)


def test_surf():
    "test of surf function"
    planning = Planning()
    assert planning.surf([[1, 1], [1.5, 2], [2, 1]]) == 0.5


def test_dedans():
    "test of dedans function"
    planning = Planning()
    assert planning.dedans([1.2, 1.2], [[[1, 1], [1.5, 2], [2, 1]]]) == 1


def test_indexdist():
    "test of indexdist function"
    planning = Planning()
    assert planning.indexdist(
        [0, 1], [[0, 0], [0.5, 0], [1, 0], [1, 1], [2, 2]]) == [[0, 0], [1, 1],
                                                                [0.5, 0],
                                                                [1, 0], [2, 2]]


def test_fonction():
    "test of fonction function"
    planning = Planning()
    assert planning.fonction([[0, 2], [1, 1], [2, 2]]) == 1.0


def test_minmaxt():
    "test of minmaxt function"
    planning = Planning()
    assert planning.minmaxt([[[0, 2], [1, 1], [2, 2]], [[0, 1], [4, 4],
                                                        [0, 3]]]) == [[0, 4],
                                                                      [1, 4]]


def test_secantlll():
    "test of secantlll function"
    planning = Planning()
    assert planning.secantlll([[1, 1], [5, 5]], [[0, 1], [4, 4], [0, 3]],
                              3) == 1


def test_secant():
    "test of secant function"
    planning = Planning()
    assert planning.secant([[1, 1], [5, 5]], [[0, 1], [6, 1]]) == 1
    assert planning.secant([[1, 1], [5, 5]], [[0, 1], [6, 7]]) == 0
