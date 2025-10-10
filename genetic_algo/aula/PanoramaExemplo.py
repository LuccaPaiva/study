import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Definindo a função de fitness landscape
def fitness_function(x, y):
    return np.sin(x) * np.cos(y) + 1.5 * np.exp(-(x**2 + y**2) / 10)

# Criação dos valores de X e Y para o gráfico
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = fitness_function(X, Y)

# Configuração do gráfico 3D
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Gerando a superfície
ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')

# Configuração dos rótulos e título
ax.set_title("Gráfico 3D do Fitness Landscape")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Fitness")

# Exibindo o gráfico
plt.show()

