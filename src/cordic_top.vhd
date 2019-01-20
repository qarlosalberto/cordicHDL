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

-------------------------------------------------------
--! @file  cordic_sincos_engine.vhd
--! @brief sum calculation
--! @todo reset
--! @todo reduce bits r2_ang
--! @todo reduce bits r1_input
--! @defgroup cordic
-------------------------------------------------------

--! Standard library.
library ieee;
--! Logic elements.
use ieee.std_logic_1164.all;
--! arithmetic functions.
use ieee.numeric_std.all;
--! cordic sincos
use work.cordic_sincos_engine_pkg.all;


--! @brief   implementation
--! @details implementation of cordic
--! @ingroup cordic

entity cordic_top is
  generic (
    g_MODE : integer := 1
  );
  port (
    clk        : in  std_logic;
    dv_in      : in  std_logic;
    data_0_in  : in  std_logic_vector (19 downto 0);
    data_1_in  : in  std_logic_vector (19 downto 0);
    data_0_out : out std_logic_vector (19 downto 0);
    data_1_out : out std_logic_vector (19 downto 0);
    dv_out     : out std_logic
  );
end cordic_top;

architecture rtl of cordic_top is

begin

  sincos : if g_MODE = 1 generate
    cordic_sincos_engine_i : cordic_sincos_engine
    port map (
      clk     => clk,
      dv_in   => dv_in,
      data_in => data_0_in,
      sin_out => data_0_out,
      cos_out => data_1_out,
      dv_out  => dv_out
    );
  end generate sincos;

end rtl;
