# -*- coding: utf-8 -*-
# Copyright 2018 Carlos Alberto Ruiz Naranjo
# carlosruiznaranjo@gmail.com
#
# This file is part of cordicHDL.
#
# cordicHDL is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# cordicHDL is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with cordicHDL.  If not, see <https://www.gnu.org/licenses/>.

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
