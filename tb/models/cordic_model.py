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

import math
import numpy as np

class Cordic :
  def __init__(self,resolution) :
    self.resolution = resolution
    angulos=[]
    c=1.0
    p=1.0
    for i in xrange(resolution) :
      a=math.atan(p)
      c*=math.cos(a)
      p/=2.0
      angulos.append(a)
    self.c=c
    self.angulos=angulos

  def sincos(self,angulo) :
    ############################################################################
    ############################  ADAPTER ######################################
    ############################################################################
    signoCoseno = 1
    if   (angulo > math.pi/2.0):
        angulo = math.pi - angulo
        signoCoseno = -1
    elif (angulo < -math.pi/2.0):
        angulo = -math.pi - angulo
        signoCoseno = -1
    ############################################################################
    ##############################  CORDIC #####################################
    ############################################################################
    x,y=(1.0,0.0)
    p=1.0
    a=0

    arrX = np.zeros(self.resolution+1)
    arrY = np.zeros(self.resolution+1)
    arrP = np.zeros(self.resolution+1)
    arrA = np.zeros(self.resolution+1)

    arrX[0] = 1.0
    arrY[0] = 0.0
    arrP[0] = 1.0
    arrA[0] = 0

    for i in range(1,self.resolution+1):
      if arrA[i-1] < angulo :
        arrX[i] = arrX[i-1] - arrY[i-1]/arrP[i-1]
        arrY[i] = arrY[i-1] + arrX[i-1]/arrP[i-1]
        arrA[i] = arrA[i-1] + self.angulos[i-1]
      else :
        arrX[i] = arrX[i-1] + arrY[i-1]/arrP[i-1]
        arrY[i] = arrY[i-1] - arrX[i-1]/arrP[i-1]
        arrA[i] = arrA[i-1] - self.angulos[i-1]
      arrP[i]= arrP[i-1]*2

    sin = arrY[self.resolution-1]*self.c
    cos = arrX[self.resolution-1]*self.c
    ############################################################################
    ##############################  ADAPTER ####################################
    ############################################################################
    sin = sin
    cos = signoCoseno*cos
    return (sin,cos)

  def testInput(self):
    print "******** init ********"
    c = Cordic(16)

    while(True):
        angle = float(raw_input('Input:'))
        sin, cos = c.sincos(angle)
        print( "Seno: " + str(sin) + " Coseno: " + str(cos))
