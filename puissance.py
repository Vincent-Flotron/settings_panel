# bin/python3

import gamma_formula as gf


valsx = [3, 2, 1.5, 1.3, 1.2, 1, 0.8, 0.5, 0.4, 0.33, 0.3, 0.27, 0.25, 0.2, 0.18, 0.15, 0.135, 0.12, 0.1, 0.09]
valsy = [0.34, 0.5, 0.67, 0.77, 0.84, 1, 1.3, 2, 2.5, 3, 3.4, 3.7, 4, 5, 5.6, 6.7, 7.5, 8.4, 10, 11]

# for x in vals:
  # print(f"{1.006238 * pow(x,-0.99829837)} = {1.006238} * {x}^{-0.99829837}")

for x, y in zip(valsx, valsy):
  print(f"'{y}' '{x}'")
  print(f"'{gf.apply(x)}' '{gf.reverse(y)}'")
  print("-")
  
