import matplotlib.pyplot as plt
import numpy as np

# Crear datos para una espiral
theta = np.linspace(0, 4 * np.pi, 100)
z = np.linspace(0, 1, 100)
r = z**2 + 1
x = r * np.sin(theta)
y = r * np.cos(theta)

# Crear la gráfica en 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z, color='purple')

# Mostrar la gráfica
plt.show()