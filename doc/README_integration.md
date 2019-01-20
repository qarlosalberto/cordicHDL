
# Integration

## Schemas

![Module ports](./images/cordic_top.png)

## Mode 1: sin cos

| Port name  | Type                  | Description    |
| ---------- | ----------------------| -------------- |
| clk        | std_logic             | clock          |
| dv_in      | std_logic             | data valid in  |
| data_0_in  | Q2.17 format [-pi,pi] | Radians angle  |
| data_1_in  | --                    | --             |
| data_0_out | Q2.17 format          | sine           |
| data_1_out | Q2.17 format          | cosine         |
| dv_out     | std_logic             | data vaild out |


## Todo

- Include reset.

## Resources utilization

## Common errors
