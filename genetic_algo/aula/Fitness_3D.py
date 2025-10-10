import random
import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms
from mpl_toolkits.mplot3d import Axes3D  # Import necessário para gráficos 3D


# Definindo o fitness landscape (landscape de fitness) como uma função bidimensional
def fitness_function(individual):
    x, y = individual
    # Uma função com vários picos (exemplo: combinação de sin e cos)
    return np.sin(x) * np.cos(y) + 1.5 * np.exp(-(x ** 2 + y ** 2) / 10),


# Configuração da DEAP para um problema de maximização
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, -5, 5)  # Define o range para x e y
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=2)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Operadores genéticos
toolbox.register("evaluate", fitness_function)
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)


# Função para visualização do fitness landscape e dos indivíduos
# def plot_fitness_landscape(population, gen):
#     x = np.linspace(-5, 5, 100)
#     y = np.linspace(-5, 5, 100)
#     X, Y = np.meshgrid(x, y)
#     Z = fitness_function([X, Y])[0]
#
#     plt.figure(figsize=(10, 6))
#     plt.contourf(X, Y, Z, levels=20, cmap="viridis")
#     plt.colorbar()
#
#     # Mostrando os indivíduos da população
#     individuals = np.array([ind[:] for ind in population])
#     plt.scatter(individuals[:, 0], individuals[:, 1], c="red", label="Indivíduos", s=30)
#     plt.title(f"Fitness Landscape - Geração {gen}")
#     plt.xlabel("X")
#     plt.ylabel("Y")
#     plt.legend()
#     plt.show()
def plot_fitness_landscape(population, gen):
        x = np.linspace(-5, 5, 100)
        y = np.linspace(-5, 5, 100)
        X, Y = np.meshgrid(x, y)
        Z = fitness_function([X, Y])[0]  # Avaliação do fitness landscape

        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')

        # Plota o fitness landscape como uma superfície 3D
        ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.7, edgecolor='none')

        # Extrai as coordenadas e valores de fitness da população
        individuals = np.array([ind[:] for ind in population])
        fitness_values = [ind.fitness.values[0] for ind in population]

        # Plota os indivíduos como pontos vermelhos na superfície
        ax.scatter(individuals[:, 0], individuals[:, 1], fitness_values, color="red", label="Indivíduos", s=30)

        ax.set_title(f"Fitness Landscape - Geração {gen}")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Fitness")
        ax.legend()
        plt.show()

# Algoritmo Genético
def main():
    random.seed(42)
    pop = toolbox.population(n=50)
    generations = 20
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("max", np.max)

    for gen in range(1, generations + 1):
        # Seleção, cruzamento e mutação
        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < 0.7:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < 0.2:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Avaliação dos fitnesses dos novos indivíduos
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        pop[:] = offspring

        # Estatísticas e visualização
        record = stats.compile(pop)
        print(f"Geração {gen} - Fitness Máximo: {record['max']:.4f}, Fitness Médio: {record['avg']:.4f}")

        # Função para visualização do fitness landscape e dos indivíduos em 3D


    plot_fitness_landscape(pop, gen)
    


if __name__ == "__main__":
    main()
