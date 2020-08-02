#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 15:17:26 2020

@author: abhash
"""

import csv
import numpy as np
from sklearn.datasets import load_digits
import os


reader = csv.reader(open("Skin_NonSkin.txt"), delimiter="\t")

dataset = []
for row in reader:
    dataset.append(row)

dataset = np.array(dataset)
np.random.shuffle(dataset)

X = dataset[:,:-1]
X = X.astype(np.float)
y = dataset[:,-1]
y = y.astype(np.int)
#print(X)
#print(y)
#print(type(X[0][0]))
#print(type(y[0]))

digits = load_digits()  # using sklearn's MNIST dataset
X1, y1 = digits.data, digits.target

#print(X1)
#print(y1)
#print(type(X1[0][0]))
#print(type(y1[0]))