from .simulation import init_del_loma_smol
from .simulation_manager import SimulationManager
from .simulation.interventions import *
import numpy as np
from copy import deepcopy
import multiprocessing


def simulation_worker(x):
    simulation = SimulationManager()
    return simulation.run_simulation(*x)


def fitness(X):
    return -np.sum(X[7, :, :])


def frick(a, b):  # <= NSFW >_>
    return a + b


if __name__ == '__main__':
    N = 5
    generations = 2
    simulation = SimulationManager()
    pool = multiprocessing.Pool(processes=4)
    # Create initial state
    initial_state = init_del_loma_smol()
    initial_state[7, 150, 150] = 1
    available_resources = {
        'bulldozer': 30
    }
    # Come up with intervention plans
    population = [[
        BullDozedFireLine(
            (150 + np.random.randint(60) - 30,
             150 + np.random.randint(60) - 30),
            (150 + np.random.randint(60) - 30,
             150 + np.random.randint(60) - 30)
        ),
    ] for i in range(N)]
    # THE CIRCLE OF LIFE
    for generation in range(generations):
        # Test intervention plans
        final_states = [
            pool.map(simulation_worker,
                     [
                         (
                             deepcopy(initial_state),
                             deepcopy(available_resources),
                             deepcopy(plan),
                             30, False
                         )
                         for i in range(3)
                     ]
                     )
            for plan in population
        ]
        # Evaluate the final states
        final_scores = [(i, np.mean([fitness(state) for state in states]))
                        for i, states in enumerate(final_states)]
        # Generate rankings
        final_score_rankings = sorted(
            final_scores,
            key=lambda x: x[1],
            reverse=True
        )
        # Cull the bottom 50% and discard the fitnesses
        survivors = final_score_rankings[:int(len(final_score_rankings) / 2)]
        survivors = [population[i] for i, fitness in survivors]
        # Make the fittest breed
        new_population = deepcopy(survivors)
        for i in range(N - len(survivors)):
            a, b = np.random.choice(len(survivors), 2)
            new_population.append(frick(survivors[a], survivors[b]))
        population = new_population

    # Test intervention plans
    final_states = [
        simulation.run_simulation(
            deepcopy(initial_state),
            deepcopy(available_resources),
            deepcopy(plan),
            steps=30,
            visualise=False
        )
        for plan in population
    ]
    # Evaluate the final states
    final_scores = [(i, fitness(state))
                    for i, state in enumerate(final_states)]
    # Generate rankings
    final_score_rankings = sorted(
        final_scores,
        key=lambda x: x[1],
        reverse=True
    )
    # Get the best one
    best_plan = final_score_rankings[0][0]

    simulation.run_simulation(
        deepcopy(initial_state),
        deepcopy(available_resources),
        [],
        steps=30,
        visualise=True
    )

    simulation.run_simulation(
        deepcopy(initial_state),
        deepcopy(available_resources),
        deepcopy(population[best_plan]),
        steps=30,
        visualise=True
    )
