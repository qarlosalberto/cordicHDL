
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

## Other considerations


## Resources utilization

## Common errors
