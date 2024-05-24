#! bin/python3

# gamma_lin.py
# ------------


def apply(x):
  return 1.006238 * pow(x,-0.99829837)
  
def reverse(y):
  return pow(y/1.006238, 1/-0.99829837) 


# print(f"{1.006238 * pow(x,-0.99829837)} = {1.006238} * {x}^{-0.99829837}")
