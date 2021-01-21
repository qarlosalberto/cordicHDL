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

from os.path import join , dirname, abspath
import subprocess
import sys
from vunit.sim_if.ghdl import GHDLInterface
from vunit.sim_if.factory import SIMULATOR_FACTORY
from vunit   import VUnit, VUnitCLI
import numpy as np
import math
sys.path.append("./models")
import utilsNumbers

##############################################################################
##############################################################################
##############################################################################

#pre_check func
def make_pre_check(g_SIZE_INPUT,g_SIZE_OUTPUT,NUM_TESTS,str_MODE):
  """
  Before test.
  """
  if (str_MODE == "sincos"):
      inputs0 = (np.random.random_sample(NUM_TESTS)-0.5)*2*math.pi
      inputs1 = (np.random.random_sample(NUM_TESTS)-0.5)*2*math.pi
  elif (str_MODE == "arctgmag"):
      inputs0 = np.random.random_sample(NUM_TESTS)
      inputs1 = np.random.random_sample(NUM_TESTS)

  inputs0XQN = utilsNumbers.f2xqnDecimal(inputs0,"signed",2,17)
  inputs1XQN = utilsNumbers.f2xqnDecimal(inputs1,"signed",2,17)
  np.savetxt('test_input_0_' + str_MODE + '.csv', inputs0XQN, delimiter=',',fmt='%1d')
  np.savetxt('test_input_1_' + str_MODE + '.csv', inputs1XQN, delimiter=',',fmt='%1d')

#post_check func
def make_post_check(str_MODE):
  """
  After test.
  """
  def post_check(output_path):
    #VHDL
    out0VHDL = utilsNumbers.xqnInt2f( np.loadtxt("out0_vhdl_"+ str_MODE +".csv",dtype=int,delimiter=','),"signed",2,17)
    out1VHDL = utilsNumbers.xqnInt2f( np.loadtxt("out1_vhdl_"+ str_MODE +".csv",dtype=int,delimiter=','),"signed",2,17)
    #Python
    out0Python = np.zeros(len(out0VHDL))
    out1Python = np.zeros(len(out0VHDL))
    if (str_MODE == "sincos"):
        input0  = utilsNumbers.xqnInt2f( np.loadtxt("test_input_0_sincos.csv",dtype=int,delimiter=','),"signed",2,17)
        input1  = utilsNumbers.xqnInt2f( np.loadtxt("test_input_1_sincos.csv",dtype=int,delimiter=','),"signed",2,17)
        out0Python = np.sin(input0)
        out1Python = np.cos(input0)
    elif (str_MODE == "arctgmag"):
        input0  = utilsNumbers.xqnInt2f( np.loadtxt("test_input_0_arctgmag.csv",dtype=int,delimiter=','),"signed",2,17)
        input1  = utilsNumbers.xqnInt2f( np.loadtxt("test_input_1_arctgmag.csv",dtype=int,delimiter=','),"signed",2,17)
        # arctg(y/x)
        out0Python = np.arctan(np.divide(input1,input0))
        for i in range(0,len(input0)):
            # sqrt(x*x + y*y)
            out1Python[i] = math.sqrt(input0[i]*input0[i] + input1[i]*input1[i])

    #Checks
    checkOut0 = np.allclose(out0Python,out0VHDL,atol=0.001)
    checkOut1 = np.allclose(out1Python,out1VHDL,atol=0.001)
    checkOut1 = True

    check    = False
    if (checkOut0==True and checkOut1==True):
        check = True
        print("All ok :)")
    else:
        print("Fail :(")

    return check
  return post_check

##############################################################################
##############################################################################
##############################################################################

#Check GHDL backend.
code_coverage=0
if( GHDLInterface.determine_backend("")=="gcc" or  GHDLInterface.determine_backend("")=="GCC"):
  code_coverage=1
else:
  code_coverage=0

#Check simulator.
print("=============================================")
simulator_class = SIMULATOR_FACTORY.select_simulator()
simname = simulator_class.name
print(simname)
if (simname == "modelsim"):
  f= open("modelsim.do","w+")
  f.write("add wave * \nlog -r /*\nvcd file\nvcd add -r /*\n")
  f.close()
print("=============================================")

##############################################################################
##############################################################################
##############################################################################

#VUnit instance.
ui = VUnit.from_argv()

##############################################################################
##############################################################################
##############################################################################

#Add array pkg.
ui.add_array_util()

#Add module sources.
cordic_top_lib = ui.add_library("cordic_top_lib")
cordic_top_lib.add_source_files("../src/cordic_sincos_engine.vhd")
cordic_top_lib.add_source_files("../src/cordic_arctg_mag_engine.vhd")
cordic_top_lib.add_source_files("../src/cordic_engines_pkg.vhd")
cordic_top_lib.add_source_files("../src/cordic_top.vhd")
cordic_top_lib.add_source_files("../src/cordic_top_pkg.vhd")

#Add tb sources.
cordic_top_tb_lib = ui.add_library("cordic_top_tb_lib")
cordic_top_tb_lib.add_source_files("cordic_top_tb.vhd")

#func precheck
tb_generated = cordic_top_tb_lib.entity("cordic_top_tb")

g_SIZE_INPUT  = 20
g_SIZE_OUTPUT = 20
NUM_TESTS     = 500
g_MODE        = [1,2]
str_MODE      = ["sincos","arctgmag"]
tb_path       = "./"

for test in tb_generated.get_tests():
    for i in range(0,len(g_MODE)):
        test.add_config(name=str_MODE[i],
        pre_config=make_pre_check(g_SIZE_INPUT,g_SIZE_OUTPUT,NUM_TESTS,str_MODE[i]),
        generics=dict(nameTest=str_MODE[i],g_MODE=g_MODE[i],tb_path=tb_path),
        post_check=make_post_check(str_MODE[i]))

##############################################################################
##############################################################################
##############################################################################

#GHDL parameters.
if(code_coverage==1):
  cordic_top_lib.add_compile_option   ("ghdl.flags"     , [ "-fexplicit","--no-vital-checks","-frelaxed-rules","-fprofile-arcs","-ftest-coverage","-fpsl"])
  cordic_top_tb_lib.add_compile_option("ghdl.flags"     , [ "-fexplicit","--no-vital-checks","-frelaxed-rules","-fprofile-arcs","-ftest-coverage","-fpsl"])
  ui.set_sim_option("ghdl.elab_flags"      , ["-fexplicit","--no-vital-checks","-frelaxed-rules","-Wl,-lgcov","-fpsl"])
else:
  cordic_top_lib.add_compile_option   ("ghdl.flags"     , ["-fexplicit","--no-vital-checks","-frelaxed-rules","-fpsl"])
  cordic_top_tb_lib.add_compile_option("ghdl.flags"     , ["-fexplicit","--no-vital-checks","-frelaxed-rules","-fpsl"])
  ui.set_sim_option("ghdl.elab_flags"      , ["-fexplicit","--no-vital-checks","-frelaxed-rules","-fpsl"])

ui.set_sim_option("modelsim.init_files.after_load" ,["modelsim.do"])
ui.set_sim_option("disable_ieee_warnings", True)
ui.set_sim_option("ghdl.sim_flags", ["--psl-report=./psl_coverage.json"])


#Run tests.
try:
  ui.main()
except SystemExit as exc:
  all_ok = exc.code == 0

#Code coverage.
if all_ok:
  if(code_coverage==1):
    subprocess.call(["lcov", "--capture", "--directory", "cordic_sincos_engine.gcda", "--output-file",  "code_0.info" ])
    subprocess.call(["lcov", "--capture", "--directory", "cordic_arctg_mag_engine.gcda", "--output-file",  "code_1.info" ])
    subprocess.call(["genhtml","code_0.info","code_1.info","--output-directory", "html"])
  else:
    print("OK")
    exit(0)
else:
  exit(1)
