from opensimplex import OpenSimplex
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import json
import random

class Game:
    def __init__(self):
        self.masterseed = random.randint(0, 1000000000000)
        self.perm_gen = self.permutation_generator(self.masterseed, 10)
        self.next_permutation = next(self.perm_gen)

    def __init__(self, masterseed):
        self.masterseed = masterseed
        self.perm_gen = self.permutation_generator(self.masterseed, 10)
        self.next_permutation = next(self.perm_gen)

    def __init__(jsonpath):
        pass

    def permutation_generator(master_seed, size):
        np.random.seed(master_seed)
        while True:
            yield np.random.permutation(size)

    def get_next_permutation(self):
        self.next_permutation = next(self.perm_gen)
        return self.next_permutation