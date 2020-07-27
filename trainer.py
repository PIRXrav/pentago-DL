#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
network trainer with genetic
"""

import matplotlib.pyplot as plt
import numpy as np
from network_pentago import NetworkPentago
from itertools import product, combinations, chain

class Trainer():
    """ Trainer class """
    def __init__(self, initial_network, witness_tab=None):
        """ init """
        # network
        self.network = initial_network
        #witness
        self.witness_tab = witness_tab
        self.score = 0  # nb win vs witness
        # output
        self.winrates = []

    def iter(self, family_size, learning_rate):
        """ exec 1 step """
        # create family
        derivation = [self.network.derivate(learning_rate)
                      for _ in range(family_size)]
        randomnw = [] # [NetworkPentago() for _ in range(family_size)]

        family = derivation + randomnw
        # play games:
        for nw_tup in product(family, self.witness_tab):
            nw_tup[0].play(nw_tup[1])

        # compute best network
        self.network = max(family, key=lambda net: net.winrate())
        if self.network in derivation:
            print("From derivation")
        else:
            print("From random")
        # check evolution with witness

        if self.witness_tab is not None:
            self.score = 0
            for witness in self.witness_tab:
                break
                self.score += (self.network.play(witness)) == self.network
        # losspython
        self.winrates.append(self.network.winrate())
        # debug
        self.iter_debug()
        # reset scores
        for network in chain(self.witness_tab, [self.network]):
            network.reset_score()

    def iter_debug(self):
        """ iter debug """
        try:
            loss = self.winrates[-1]
            last_loss = self.winrates[-2]
            delta = last_loss - loss
            print(f"[{len(self.winrates)}]" +
                  "score={:.5f}\t".format(loss) +
                  ("\33[92m" if delta < 0 else "\33[91m")+str(delta)+"\33[39m",
                  end='\n')
        except:
            pass

    def plot_loss(self):
        """ display winrate evolution """
        plt.subplot(2, 2, 1)
        plt.plot(self.winrates, label="winrate")
        plt.xlabel("n")
        plt.ylabel("winrate")
        plt.legend()
        plt.subplot(2, 2, 2)
        plt.plot(- np.diff(np.array(self.winrates)), label="gain")
        plt.xlabel("n")
        plt.ylabel("dwinrate/dn")
        plt.legend()
        plt.show()


if __name__ == '__main__':

    family_size = 10
    learning_rate = 0.01
    nb_iterarion = 100

    witnesss = [NetworkPentago() for _ in range(10)]
    best = NetworkPentago()
    trainer = Trainer(best, witnesss)
    for _ in range(nb_iterarion):
        trainer.iter(family_size, learning_rate)
        print('Trainer score: ', trainer.score)
    trainer.plot_loss()
