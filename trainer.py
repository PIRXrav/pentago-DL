#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
network trainer with genetic
"""

import matplotlib.pyplot as plt
import numpy as np
from network import Network


class Trainer():
    """ Trainer class """
    def __init__(self, initial_network):
        """ init """
        self.network = initial_network
        # output
        self.losss = []

    def iter(self, family_size, learning_rate, x, y):
        """ exec 1 step """
        # create family
        family = [self.network.derivate(learning_rate)
                  for _ in range(family_size)]
        # compute best network
        self.network = min(family, key=lambda net: net.forward(x).loss(y))
        # loss
        self.losss.append(self.network.loss(y))
        # debug
        self.iter_debug()

    def iter_debug(self):
        """ iter debug """
        try:
            loss = self.losss[-1]
            last_loss = self.losss[-2]
            delta = last_loss - loss
            print(f"[{len(self.losss)}]" +
                  "score={:.5f}\t".format(loss) +
                  ("\33[92m+" if delta > 0 else "\33[91m")+str(delta)+"\33[39m",
                  end='\n')
        except:
            pass

    def plot_loss(self):
        """ display loss evolution """
        plt.subplot(2, 2, 1)
        plt.plot(self.losss, label="loss")
        plt.xlabel("n")
        plt.ylabel("loss")
        plt.legend()
        plt.subplot(2, 2, 2)
        plt.plot(- np.diff(np.array(self.losss)), label="gain")
        plt.xlabel("n")
        plt.ylabel("dloss/dn")
        plt.legend()
        plt.show()


if __name__ == '__main__':
    # Create random input and output data
    x = np.random.randn(1, 36)
    y = np.random.randn(1, 36)

    family_size = 10
    learning_rate = 0.001
    nb_iterarion = 2000

    trainer = Trainer(Network([36] + [36] * 3 + [36]))
    for _ in range(nb_iterarion):
        trainer.iter(family_size, learning_rate, x, y)
    trainer.plot_loss()
