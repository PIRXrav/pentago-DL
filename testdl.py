#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from network import Network

nb_iterarion = 2000
family_size = 10
learning_rate = 0.001

# Create random input and output data
x = np.random.randn(1, 36)
y = np.random.randn(1, 36)

best_network = Network([36] + [36] * 3 + [36])  # random network

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

print(best_network)
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
