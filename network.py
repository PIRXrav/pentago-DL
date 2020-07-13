#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IA network
"""

from copy import deepcopy
import numpy as np
from more_itertools import windowed


class Network:
    """ DFF """
    def __init__(self, dims):
        """ init """
        assert len(dims) >= 2
        # dimentions
        self.dims = dims
        # Randomly initialize weights
        self.wtab = [np.random.randn(*ll) for ll in windowed(dims, 2)]
        # out data
        self.y_pred = 0

    def forward(self, x):
        """ Forward pass: compute predicted y """
        current = x
        for i, weights in enumerate(self.wtab):
            layerh = current.dot(weights)
            if i != len(self.dims):
                # ReLU
                current = np.maximum(layerh, 0)
                # signe doux :
                # current = layerh / ( np.abs(layerh) + 1 )
                # Unité de rectification linéaire douce (SoftPlus)
                # current = np.log2(np.exp(layerh) + 1)
                # Fonction gaussienne
                # current = np.exp(-layerh * layerh)
        self.y_pred = current
        return self

    def loss(self, y):
        """ calc err """
        return np.square(self.y_pred - y).sum()

    def compute_score(self, x, y):
        """ forward(x).loss(y) """
        return self.forward(x).loss(y)

    def derivate(self, learning_rate):
        """ derivate network with rng """
        div = deepcopy(self)
        for i in range(len(div.dims) - 1):
            div.wtab[i] += np.random.randn(*div.wtab[i].shape) * learning_rate
        return div

    def __repr__(self):
        return '<network ' + '-X-'.join(map(str, self.dims)) + '>'

    def __str__(self):
        return self.__repr__()
