import bitstring as bt
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

import numpy as np
import math

def xqnInt2f(arr,mode,iSize,fSize):
    arrf = []
    for x in arr:
        intPart = x >> fSize
        step = 1.0/2**fSize
        decPart = (x & (2**fSize-1))*step
        arrf.append(intPart + decPart)
    return arrf

def f2xqnDecimal(arr,mode,iSize,fSize):
    arrXQNdecimal, arrXQNbit = f2xqn(arr,mode,iSize,fSize)
    return arrXQNdecimal

def f2xqnBit(arr,mode,iSize,fSize):
    arrXQNdecimal, arrXQNbit = f2xqn(arr,mode,iSize,fSize)
    return arrXQNbit

def f2xqnROM(arr,mode,iSize,fSize):
    arrXQNbit = f2xqnBit(arr,mode,iSize,fSize)
    if(len(arr)>0):
        bits2rom(arrXQNbit,mode,len(arr),1+iSize+fSize)
    else:
        print(arrBit[0].bin)

#float to bits: (signed/unsigned,integer part size, decimal part size)
def f2xqn(arr,mode,iSize,fSize):
    arrBit = []
    arrDec = []
    if (iSize == 0):
        for i in range(0, len(arr)):
            dec = int(arr[i]*(2**fSize))
            arrDec.append( dec )
            arrBit.append( bt.BitArray("int:"+str(fSize+1)+"="+str(dec)) )
    else:
        for i in range(0, len(arr)):
            dec,integ = math.modf(arr[i])
            dec   = int(dec*(2**fSize))
            integ = int(integ)

            completeNumber = integ*(2**fSize) + dec
            numberBits = bt.BitArray( "int:"+str(iSize+fSize+1)+"="+str(completeNumber) )

            arrDec.append( completeNumber )
            arrBit.append( numberBits )

    return arrDec, arrBit


def bits2rom(barr,mode,sizeMem, sizeWord):
    strType = "type rom_type is array (0 to " + str(sizeMem-1) + ") of std_logic_vector(" + str(sizeWord-1) + " downto 0);\n"
    strDef    = "constant ROM : rom_type := (\n"
    strDefRom = "  "
    for i in range(0,len(barr)):
        if (i == len(barr)-1):
            strDefRom = strDefRom + '"' + barr[i].bin + '"\n'
        else:
            strDefRom = strDefRom + '"' + barr[i].bin + '",'
    strDefEnd = ");\n\n"

    strRom = strType + strDef + strDefRom + strDefEnd

    print(strRom)
    return strRom
