-------------------------------------------------------
--! @file  cordic_top_pkg.vhd
--! @brief Core package
--! @todo
--! @defgroup cordic
-------------------------------------------------------

--! Standard library.
library ieee;
--! Logic elements.
use ieee.std_logic_1164.all;
--! arithmetic functions.
use ieee.numeric_std.all;

--! @brief   package
--! @details package of cordic
--! @ingroup cordic

package cordic_sincos_engine_pkg is

  component cordic_sincos_engine is
  port (
    clk     : in  std_logic;
    dv_in   : in  std_logic;
    data_in : in  std_logic_vector (19 downto 0);
    cos_out : out std_logic_vector (19 downto 0);
    sin_out : out std_logic_vector (19 downto 0);
    dv_out  : out std_logic
  );
  end component;

end package;
