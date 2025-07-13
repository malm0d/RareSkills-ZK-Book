from scipy.interpolate import lagrange

x_values = [1, 2, 3, 4]
y_values = [4, 8, 2, 1]

print(lagrange(x_values, y_values))
# Output:
#     3      2
# 2.5 x - 20 x + 46.5 x - 25
#
# (i.e. 2.5x^3 - 20x^2 + 46.5x - 25)