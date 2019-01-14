# -*- coding: utf-8 -*-
import cordic_model as cm
import numpy as np
import math

NUM_TESTS = 10000
RESOLUTION_ANG_TABLE = 16
#Random test input
inputs = (np.random.random_sample(NUM_TESTS)-0.5)*2*math.pi
sinModel = np.zeros(NUM_TESTS)
cosModel = np.zeros(NUM_TESTS)
#sin-cos python
sinPython = np.sin(inputs)
cosPython = np.cos(inputs)
#sin-cos model
sincosCordic = cm.Cordic(RESOLUTION_ANG_TABLE)
for i in range(0,NUM_TESTS):
    sinModel[i], cosModel[i] = sincosCordic.sincos(inputs[i])
#Checks
checkSin = np.allclose(sinPython,sinModel,atol=0.001)
checkCos = np.allclose(cosPython,cosModel,atol=0.001)

if (checkSin and checkCos == True):
    print("All Ok! :)")
else:
    print("Fail :()")
