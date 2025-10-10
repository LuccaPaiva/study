import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button


# Função de fitness com duas gaussianas
def fitness_function(x):
    A1, mu1, sigma1 = 50, 2, 0.5  # Pico mais alto
    A2, mu2, sigma2 = 45, 5, 1.0  # Pico mais baixo
    gauss1 = A1 * np.exp(-((x - mu1) ** 2) / (2 * sigma1 ** 2))
    gauss2 = A2 * np.exp(-((x - mu2) ** 2) / (2 * sigma2 ** 2))
    return gauss1 + gauss2


# Inicialização da população
def initialize_population(size, x_min, x_max):
    return np.random.uniform(x_min, x_max, size)


# Avaliação do fitness
def evaluate_population(population):
    return fitness_function(population)


# Seleção por roleta (favorece o melhor, mas mantém diversidade)
def selection(population, fitness):
    fitness_sum = np.sum(fitness)
    probabilities = fitness / fitness_sum
    selected_indices = np.random.choice(len(population), size=len(population), p=probabilities)
    return population[selected_indices]


# Crossover uniforme
def crossover(parent1, parent2):
    return np.random.choice([parent1, parent2], size=1, p=[0.5, 0.5])[0]


# Mutação adaptativa
def mutate(individual, x_min, x_max, mutation_rate=0.1):
    if np.random.rand() < mutation_rate:
        perturbation = np.random.normal(0, 0.1 * (x_max - x_min))
        return np.clip(individual + perturbation, x_min, x_max)
    return individual


# Evolução da população
def evolve_population(population, x_min, x_max):
    fitness = evaluate_population(population)
    selected = selection(population, fitness)
    next_population = []
    for i in range(0, len(selected), 2):
        parent1, parent2 = selected[i], selected[(i + 1) % len(selected)]
        offspring1 = mutate(crossover(parent1, parent2), x_min, x_max)
        offspring2 = mutate(crossover(parent2, parent1), x_min, x_max)
        next_population.extend([offspring1, offspring2])
    return np.array(next_population[:len(population)])


# Visualização
class GeneticAlgorithmVisualizer:
    def __init__(self, generations=20, pop_size=10, x_min=0, x_max=7):
        self.generations = generations
        self.pop_size = pop_size
        self.x_min = x_min
        self.x_max = x_max
        self.current_generation = 0
        self.population = initialize_population(self.pop_size, self.x_min, self.x_max)
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(self.x_min, self.x_max)
        self.ax.set_ylim(0, 60)  # Ajuste para o máximo da função
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
            self.population = evolve_population(self.population, self.x_min, self.x_max)
            self.scatter.set_offsets(np.c_[self.population, evaluate_population(self.population)])
            self.current_generation += 1
            self.ax.set_title(f'Geração {self.current_generation}')
            plt.draw()


# Executando a visualização do algoritmo genético
GeneticAlgorithmVisualizer(generations=20, pop_size=20, x_min=0, x_max=7)
