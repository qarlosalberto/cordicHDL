
# Integration

## Schemas

![Module ports](./images/cordic_sincos_engine.png)

## Port description table

| Port name | Type                  | Description    |
| --------- | ----------------------| -------------- |
| clk       | std_logic             | clock          |
| dv_in     | std_logic             | data valid in  |
| data_in   | Q2.17 format [-pi,pi] | Radians angle  |
| cos_out   | Q2.17 format          | cosine         |
| sin_out   | Q2.17 format          | sine           |
| dv_out    | std_logic             | data vaild out |

## Todo

- DSP48E1 in Xilinx 7 series allows 25 × 18 two’s-complement multiplier.
Reduce the size of the angle table to reduce the multipliers.

- Include reset.

- Reduce adder bits.

## Resources utilization

## Common errors
