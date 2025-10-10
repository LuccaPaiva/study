# Based on https://towardsdatascience.com/an-introduction-to-genetic-algorithms-the-concept-of-biological-evolution-in-optimization-fc96e78fa6db/
# By Julian Blank
# Define pop_size, n_gen;

import numpy as np
import os
from scipy.spatial.distance import cdist

import matplotlib.animation as animation
import matplotlib.pyplot as plt
# PSEUDO CODE
# P = initialize(pop_size)
# evaluate(P)
# for k in (1, .., n_gen)
#     parents = selection(P)
#     O = mutation(crossover(parents))
#     evaluate(O)
#     M = merge(P, O)
#     P = survival(M)
# endfor


def to_int(x) -> int:
    return (x * [128, 64, 32, 16, 8, 4, 2, 1]).sum()


def evaluate(x):
    return np.sin(to_int(x) / 256 * np.pi)


def initialize():
    return np.random.choice([0, 1], size=8)


def select(n_matings, n_parents):
    return np.random.randint(0, n_matings, (n_matings, n_parents))


def crossover(parent_a, parent_b):
    rnd = np.random.choice([False, True], size=8)

    offspring = np.empty(8, dtype=np.bool)
    offspring[rnd] = parent_a[rnd]
    offspring[~rnd] = parent_b[~rnd]
    return offspring


def mutate(o):
    rnd = np.random.random(8) < 0.125

    mut = o.copy()
    mut[rnd] = ~mut[rnd]
    return mut


def survival(f, n_survivors):
    return np.argsort(-f)[:n_survivors]


def eliminate_duplicates(X):
    D = cdist(X, X)
    D[np.triu_indices(len(X))] = np.inf
    return np.all(D > 1e-32, axis=1)


def create_plt(x: int, y: float):
    xpoints = np.arange(1, 255)
    ypoints = np.array(np.sin(xpoints * np.pi / 256))

    plt.plot(xpoints, ypoints, linestyle="dotted")
    plt.plot(x, y, "o")
    plt.show()


def run_evolution(pop_size=5, n_gen=15, seed=1):
    np.random.seed(seed)

    # Inicialização
    X = np.array([initialize() for _ in range(pop_size)])
    F = np.array([evaluate(x) for x in X])

    best_y_hist = [np.max(F)]
    avr_y_hist = [np.mean(F)]
    best_x_hist = [to_int(X[np.argmax(F)])]
    avr_x_hist = [np.mean([to_int(x) for x in X])]

    # Loop principal
    for k in range(n_gen):
        parents = select(pop_size, 2)
        _X = np.array([mutate(crossover(X[a], X[b])) for a, b in parents])
        _F = np.array([evaluate(x) for x in _X])

        # Junta população e descendentes
        X, F = np.vstack([X, _X]), np.concatenate([F, _F])

        # Elimina duplicados
        I = eliminate_duplicates(X)
        X, F = X[I], F[I]

        # Seleciona sobreviventes
        I = survival(F, pop_size)
        X, F = X[I], F[I]

        # Atualiza históricos
        best_idx = np.argmax(F)
        best_x = to_int(X[best_idx])
        best_y = F[best_idx]
        avr_x = np.mean([to_int(x) for x in X])
        avr_y = np.mean(F)

        best_x_hist.append(best_x)
        best_y_hist.append(best_y)
        avr_x_hist.append(avr_x)
        avr_y_hist.append(avr_y)

        print(f"Geração {k + 1:2d} | Melhor: {best_y:.4f} {X[0]}| Média: {avr_y:.4f}")

    return best_x_hist, best_y_hist, avr_x_hist, avr_y_hist


def create_animation(best_y_hist, avr_y_hist, n_gen, save_path=None):
    fig, ax = plt.subplots()
    ax.set_xlim(0, n_gen)
    ax.set_ylim(min(avr_y_hist) - 0.1, 1.1)
    ax.set_xlabel("Geração")
    ax.set_ylabel("Valor da Função")
    ax.set_title("Evolução do Melhor e da Média da População")

    (line_best,) = ax.plot([], [], "r-", label="Melhor indivíduo")
    (line_mean,) = ax.plot([], [], "b--", label="Média da população")
    ax.legend()

    def init():
        line_best.set_data([], [])
        line_mean.set_data([], [])
        return line_best, line_mean

    def update(frame):
        generations = np.arange(frame + 1)
        line_best.set_data(generations, best_y_hist[: frame + 1])
        line_mean.set_data(generations, avr_y_hist[: frame + 1])
        return line_best, line_mean

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=len(best_y_hist),
        init_func=init,
        blit=True,
        interval=600,
        repeat=False,
    )

    plt.show()

    if save_path:
        ani.save(save_path, writer="pillow", fps=2)
        print(f"Animação salva em: {save_path}")


def create_function_animation(
    best_x_hist, best_y_hist, avr_x_hist, avr_y_hist, save_path=None, interval=600
):
    """
    Mostra f(x)=sin(x*pi/256) e os pontos (melhor e média) para cada geração.
    Corrige o problema: passa listas/arrays para set_data() e para de animar após salvar.
    """
    if len(best_x_hist) == 0:
        raise ValueError("Histórico vazio: nada para animar.")

    xpoints = np.arange(0, 256)
    ypoints = np.sin(xpoints * np.pi / 256)

    fig, ax = plt.subplots()
    ax.plot(xpoints, ypoints, "k--", label="f(x) = sin(x·π/256)")
    ax.set_xlim(0, 256)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("x (inteiro codificado)")
    ax.set_ylabel("f(x)")
    ax.set_title("Evolução sobre a Função f(x)")

    (point_best,) = ax.plot([], [], "ro", label="Melhor indivíduo")
    (point_mean,) = ax.plot([], [], "bo", label="Média da população")
    ax.legend()

    def init():
        point_best.set_data([], [])
        point_mean.set_data([], [])
        return point_best, point_mean

    def update(frame):
        # Atenção: set_data exige sequência, mesmo para 1 ponto -> usamos listas
        bx = best_x_hist[frame]
        by = best_y_hist[frame]
        mx = avr_x_hist[frame]
        my = avr_y_hist[frame]

        point_best.set_data([bx], [by])  # fix: passar sequências
        point_mean.set_data([mx], [my])  # fix: passar sequências

        ax.set_title(f"Evolução sobre f(x) — Geração {frame}")
        return point_best, point_mean

    # blit=False costuma ser mais compatível com salvamento via Pillow
    ani = animation.FuncAnimation(
        fig,
        update,
        frames=len(best_x_hist),
        init_func=init,
        blit=False,
        interval=interval,
        repeat=False,
    )

    # Se for salvar: cria diretório, salva e para o event loop de animação para evitar chamadas extras
    if save_path:
        os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
        writer = animation.PillowWriter(
            fps=1000 // interval if interval < 1000 else 1
        )  # fps razoável
        ani.save(save_path, writer=writer)
        print(f"Animação salva em: {save_path}")

        # evita que o timer do matplotlib continue chamando `update` após o salvamento
        if hasattr(ani, "event_source") and ani.event_source:
            try:
                ani.event_source.stop()
            except Exception:
                pass

    # Mostra a figura (se quiser executar apenas salvar sem abrir, remova plt.show())
    plt.show()

    return ani


if __name__ == "__main__":
    pop_size = 5
    n_gen = 15

    best_x_hist, best_y_hist, avr_x_hist, avr_y_hist = run_evolution(pop_size, n_gen)

    create_animation(
        best_y_hist, avr_y_hist, n_gen, save_path="genetic_algo/media/evolucao.gif"
    )

    create_function_animation(
        best_x_hist,
        best_y_hist,
        avr_x_hist,
        avr_y_hist,
        save_path="genetic_algo/media/evolucao_funcao.gif",
    )
