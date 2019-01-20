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
from vunit.ghdl_interface import GHDLInterface
from vunit.simulator_factory import SIMULATOR_FACTORY
from vunit   import VUnit, VUnitCLI
import numpy as np
import math
sys.path.append("./models")
import utilsNumbers

##############################################################################
##############################################################################
##############################################################################

#pre_check func
def make_pre_check(g_SIZE_INPUT,g_SIZE_OUTPUT,NUM_TESTS,g_MODE):
  print("+++++++++++++++++++++++++++")
  """
  Before test.
  """
  inputs0 = (np.random.random_sample(NUM_TESTS)-0.5)*2*math.pi
  inputs1 = (np.random.random_sample(NUM_TESTS)-0.5)*2*math.pi
  inputs0XQN = utilsNumbers.f2xqnDecimal(inputs0,"signed",2,17)
  inputs1XQN = utilsNumbers.f2xqnDecimal(inputs1,"signed",2,17)
  np.savetxt('test_input_0.csv', inputs0XQN, delimiter=',',fmt='%1d')
  np.savetxt('test_input_1.csv', inputs1XQN, delimiter=',',fmt='%1d')

#post_check func
def make_post_check(g_MODE):
  """
  After test.
  """
  def post_check(output_path):
    inputs  = utilsNumbers.xqnInt2f( np.loadtxt("test_input_0.csv",dtype=int,delimiter=','),"signed",2,17)
    sinVHDL = utilsNumbers.xqnInt2f( np.loadtxt("sin_vhdl.csv",dtype=int,delimiter=','),"signed",2,17)
    cosVHDL = utilsNumbers.xqnInt2f( np.loadtxt("cos_vhdl.csv",dtype=int,delimiter=','),"signed",2,17)

    sinPython = np.sin(inputs)
    cosPython = np.cos(inputs)

    checkSin = np.allclose(sinPython,sinVHDL,atol=0.001)
    checkCos = np.allclose(cosPython,cosVHDL,atol=0.001)
    check    = False

    if (checkSin==True and checkCos==True):
        check = True
    else:
        print("Fail.")

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
print "============================================="
simulator_class = SIMULATOR_FACTORY.select_simulator()
simname = simulator_class.name
print simname
if (simname == "modelsim"):
  f= open("modelsim.do","w+")
  f.write("add wave * \nlog -r /*\nvcd file\nvcd add -r /*\n")
  f.close()
print "============================================="

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
NUM_TESTS     = 1000
g_MODE        = 1
tb_path        = "./"

for test in tb_generated.get_tests():
    test.add_config(name="prueba",pre_config=make_pre_check(g_SIZE_INPUT,g_SIZE_OUTPUT,NUM_TESTS,g_MODE),
    generics=dict(g_MODE=g_MODE,tb_path=tb_path),
    post_check=make_post_check(g_MODE))


##############################################################################
##############################################################################
##############################################################################

#GHDL parameters.
if(code_coverage==1):
  cordic_top_lib.add_compile_option   ("ghdl.flags"     , [ "-fexplicit","--no-vital-checks","-frelaxed-rules","-fprofile-arcs","-ftest-coverage"])
  cordic_top_tb_lib.add_compile_option("ghdl.flags"     , [ "-fexplicit","--no-vital-checks","-frelaxed-rules","-fprofile-arcs","-ftest-coverage"])
  ui.set_sim_option("ghdl.elab_flags"      , ["-fexplicit","--no-vital-checks","-frelaxed-rules","-Wl,-lgcov"])
  ui.set_sim_option("modelsim.init_files.after_load" ,["modelsim.do"])
  ui.set_sim_option("disable_ieee_warnings", True)
else:
  cordic_top_lib.add_compile_option   ("ghdl.flags"     , ["-fexplicit","--no-vital-checks","-frelaxed-rules"])
  cordic_top_tb_lib.add_compile_option("ghdl.flags"     , ["-fexplicit","--no-vital-checks","-frelaxed-rules"])
  ui.set_sim_option("ghdl.elab_flags"      , ["-fexplicit","--no-vital-checks","-frelaxed-rules"])
  ui.set_sim_option("modelsim.init_files.after_load" ,["modelsim.do"])
  ui.set_sim_option("disable_ieee_warnings", True)

#Run tests.
try:
  ui.main()
except SystemExit as exc:
  all_ok = exc.code == 0

#Code coverage.
if all_ok:
  if(code_coverage==1):
    subprocess.call(["lcov", "--capture", "--directory", "cordic_sincos_engine.gcda", "--output-file",  "code_0.info" ])
    subprocess.call(["lcov", "--capture", "--directory", "cordic_sincos_engine_pkg.gcda", "--output-file",  "code_1.info" ])
    subprocess.call(["genhtml","code_0.info","code_1.info","--output-directory", "html"])
  else:
    print("OK")
    exit(0)
else:
  exit(1)
