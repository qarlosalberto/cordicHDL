-- Copyright 2018 Carlos Alberto Ruiz Naranjo
-- carlosruiznaranjo@gmail.com
--
-- This file is part of cordicHDL.
--
-- cordicHDL is free software: you can redistribute it and/or modify
-- it under the terms of the GNU General Public License as published by
-- the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
--
-- cordicHDL is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with cordicHDL.  If not, see <https://www.gnu.org/licenses/>.

--! Librería estándar.
library ieee;
--! Elementos lógicos.
use ieee.std_logic_1164.all;
--! Funciones aritméticas.
use ieee.numeric_std.all;
--
library std;
use std.textio.all;
--
library cordic_top_lib;
use cordic_top_lib.cordic_top_pkg.all;
-- vunit
library vunit_lib;
context vunit_lib.vunit_context;
-- use vunit_lib.array_pkg.all;
-- use vunit_lib.lang.all;
-- use vunit_lib.string_ops.all;
-- use vunit_lib.dictionary.all;
-- use vunit_lib.path.all;
-- use vunit_lib.log_types_pkg.all;
-- use vunit_lib.log_special_types_pkg.all;
-- use vunit_lib.log_pkg.all;
-- use vunit_lib.check_types_pkg.all;
-- use vunit_lib.check_special_types_pkg.all;
-- use vunit_lib.check_pkg.all;
-- use vunit_lib.run_types_pkg.all;
-- use vunit_lib.run_special_types_pkg.all;
-- use vunit_lib.run_base_pkg.all;
-- use vunit_lib.run_pkg.all;
use vunit_lib.array_pkg.all;
use vunit_lib.integer_array_pkg.all;

entity cordic_top_tb is
  --vunit
  generic (
    nameTest   : string := "";
    tb_path    : string := "./";
    runner_cfg : string
  );
end;

architecture bench of cordic_top_tb is
  -- clock period
  constant clk_period      : time := 5 ns;
  -- Signal ports
  signal clk     : std_logic;
  signal dv_in   : std_logic;
  signal data_0_in : std_logic_vector (19 downto 0);
  signal data_1_in : std_logic_vector (19 downto 0);
  signal data_1_out : std_logic_vector (19 downto 0);
  signal data_0_out : std_logic_vector (19 downto 0);
  signal dv_out  : std_logic;
  -- Generics
  --
  signal    start_input : boolean := false;
  signal    end_input   : boolean := false;
  constant c_SIZE_INPUT : integer := 20;

  shared variable data_inputs : array_t;

begin
  -- Instance
  cordic_top_i : cordic_top
  port map (
    clk        => clk,
    dv_in      => dv_in,
    data_0_in  => data_0_in,
    data_1_in  => data_1_in,
    data_0_out => data_0_out,
    data_1_out => data_1_out,
    dv_out     => dv_out
  );

  -- test_runner_watchdog(runner, 30 us);

  main : process
  begin
    test_runner_setup(runner, runner_cfg);
    while test_suite loop
      if run("test_0") then
      -- elsif run("test_0") then
        logger_init(display_format => verbose);
        --
        wait for clk_period*5;
        start_input <= true;
        --
        wait for clk_period*1;
        --
        wait until (end_input = true);
        wait for clk_period*30;
        --
        test_runner_cleanup(runner);
      end if;
    end loop;
  end process;

  input : process
  begin
    dv_in <= '0';
    data_inputs.load_csv(tb_path & "test_input" & nameTest & ".csv");
    wait until (start_input = true);
    wait until (rising_edge(clk));
    -- Inputs
    for i in 0 to data_inputs.length-1 loop
      dv_in    <= '1';
      data_0_in  <= std_logic_vector(to_signed(data_inputs.get(i),c_SIZE_INPUT));
      wait until (rising_edge(clk));
    end loop;
    end_input <= true;
  end process;

  output : process
    variable sin_outputs : array_t;
    variable sin_out_int : integer;
    variable cos_outputs : array_t;
    variable cos_out_int : integer;
  begin
    wait until (dv_out = '1' and rising_edge(clk));
    sin_outputs.init(length => data_inputs.length,
                    bit_width => c_SIZE_INPUT,
                    is_signed => true);
    cos_outputs.init(length => data_inputs.length,
                    bit_width => c_SIZE_INPUT,
                    is_signed => true);
    -- Inputs
    for i in 0 to data_inputs.length-1 loop
      sin_out_int := to_integer(signed(data_0_out));
      sin_outputs.set(i,sin_out_int);
      --
      cos_out_int := to_integer(signed(data_1_out));
      cos_outputs.set(i,cos_out_int);
      wait for 1*clk_period;
    end loop;
    sin_outputs.save_csv(tb_path & "sin_vhdl" & nameTest &".csv");
    cos_outputs.save_csv(tb_path & "cos_vhdl" & nameTest &".csv");
  end process;

  clk_process :process
  begin
    clk <= '1';
    wait for clk_period/2;
    clk <= '0';
    wait for clk_period/2;
  end process;

end;
