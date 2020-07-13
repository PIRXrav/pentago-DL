#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

nb_iterarion = 5000
family_size = 10
learning_rate = 0.001

class Network:
    """ CNN """
    def __init__(self):
        self.D_in = 36   # input dimension
        self.N = 1       # batch size
        self.H = 100     # hidden dimension
        self.D_out = 36  # output dimension

        # Randomly initialize weights
        self.w1 = np.random.randn(self.D_in, self.H)
        self.w2 = np.random.randn(self.H, self.D_out)

        # in and out data
        self.x = 0
        self.y_pred = 0

    def forward(self, x):
        # Forward pass: compute predicted y
        self.x = x
        h = self.x.dot(self.w1)
        h_relu = np.maximum(h, 0)
        self.y_pred = h_relu.dot(self.w2)
        return self

    def loss(self, y):
        return np.square(self.y_pred - y).sum()

    def compute_score(self, x, y):
        return self.forward(x).loss(y)

    def derivate(self, learning_rate):
        div = Network()
        div.w1 = self.w1 + np.random.randn(self.D_in, self.H) * learning_rate
        div.w2 = self.w2 + np.random.randn(self.H, self.D_out) * learning_rate
        return div


# Create random input and output data
x = np.random.randn(1, 36)
y = np.random.randn(1, 36)

best_network = Network()  # random network

last_best_loss = float('inf')
losss = [0 for _ in range(nb_iterarion)]

for t in range(nb_iterarion):
    # create family
    family = [best_network.derivate(learning_rate) for _ in range(family_size)]
    # compute best network
    best_network = min(family, key=lambda net: net.forward(x).loss(y))
    # loss
    best_loss = best_network.loss(y)
    delta = last_best_loss - best_loss
    losss[t] = best_loss
    # debug
    print(f"[{t}/{nb_iterarion}]" +
          "score={:.5f}\t".format(best_loss) +
          ("\33[92m+" if delta > 0 else "\33[91m") + str(delta) + "\33[39m",
          end='\r')
    last_best_loss = best_loss

import matplotlib.pyplot as plt
plt.subplot(2, 2, 1)
plt.plot(range(nb_iterarion), losss, label="loss")
plt.xlabel("n")
plt.ylabel("loss")
plt.legend()
plt.subplot(2, 2, 2)
plt.plot(range(nb_iterarion - 1), - np.diff(np.array(losss)), label="gain")
plt.xlabel("n")
plt.ylabel("dloss/dn")
plt.legend()
plt.show()
