import numpy as np
import matplotlib.pyplot as plt
from GTO_TTT import gto

x = np.linspace(0, 1, 100)
y = -x**2

# plt.plot(y)
# plt.show()

returns = [0,1,0, -1]
print(returns)
a = np.random.rand(len(returns))
print(a)
inlay = np.array(returns)-a
print(inlay)
index = np.argsort(inlay)
print(index)
print()
print(np.random.rand(len([3,3,3]))/100)