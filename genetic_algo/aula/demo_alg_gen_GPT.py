#Este código não mostra a função de fitness; o GPT enviou outro código que altera a apresentação do plt de fitness

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button


# Definição da função objetivo
def fitness_function(x):
    return x ** 2


# Inicialização da população
def initialize_population(size, x_min, x_max):
    return np.random.uniform(x_min, x_max, size)


# Avaliação do fitness
def evaluate_population(population):
    return fitness_function(population)


# Seleção por torneio
# def selection(population, fitness, k=2):
#     selected = []
#     for _ in range(len(population)):
#         ind = np.random.choice(len(population), k, replace=False)
#         best = ind[np.argmin(fitness[ind])]
#         selected.append(population[best])
#     return np.array(selected)
# Seleção por torneio ajustada para maximização
def selection(population, fitness, k=2):
    selected = []
    for _ in range(len(population)):
        ind = np.random.choice(len(population), k, replace=False)
        best = ind[np.argmax(fitness[ind])]  # Seleciona o com maior fitness
        selected.append(population[best])
    return np.array(selected)


# Crossover de um ponto
def crossover(parent1, parent2):
    alpha = np.random.rand()
    return alpha * parent1 + (1 - alpha) * parent2


# Mutação
def mutate(individual, x_min, x_max, mutation_rate=0.1):
    if np.random.rand() < mutation_rate:
        return individual + np.random.uniform(-1, 1) * (x_max - x_min) * 0.1
    return individual


# Evolução da população
def evolve_population(population, fitness, x_min, x_max):
    selected = selection(population, fitness)
    next_population = []
    for i in range(0, len(selected), 2):
        parent1, parent2 = selected[i], selected[(i + 1) % len(selected)]
        offspring1 = crossover(parent1, parent2)
        offspring2 = crossover(parent2, parent1)
        next_population.extend([mutate(offspring1, x_min, x_max), mutate(offspring2, x_min, x_max)])
    return np.array(next_population[:len(population)])


# Visualização
class GeneticAlgorithmVisualizer:
    def __init__(self, generations=20, pop_size=10, x_min=-10, x_max=10):
        self.generations = generations
        self.pop_size = pop_size
        self.x_min = x_min
        self.x_max = x_max
        self.current_generation = 0
        self.population = initialize_population(self.pop_size, self.x_min, self.x_max)
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(self.x_min, self.x_max)
        self.ax.set_ylim(0, fitness_function(self.x_max))
        self.scatter = self.ax.scatter(self.population, evaluate_population(self.population), c='blue',
                                       label='Indivíduos')
        self.ax.plot(np.linspace(self.x_min, self.x_max, 100),
                     fitness_function(np.linspace(self.x_min, self.x_max, 100)), 'r-', label='Fitness Function')
        self.ax.legend()

        self.button_ax = plt.axes([0.8, 0.01, 0.1, 0.05])
        self.button = Button(self.button_ax, 'Próxima Geração')
        self.button.on_clicked(self.next_generation)
        plt.show()

    def next_generation(self, event):
        if self.current_generation < self.generations:
            fitness = evaluate_population(self.population)
            self.population = evolve_population(self.population, fitness, self.x_min, self.x_max)
            self.scatter.set_offsets(np.c_[self.population, evaluate_population(self.population)])
            self.current_generation += 1
            self.ax.set_title(f'Geração {self.current_generation}')
            plt.draw()


# Executando a visualização do algoritmo genético
GeneticAlgorithmVisualizer(generations=20, pop_size=10, x_min=-10, x_max=10)
