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
    fl_a = a[0]
    fl_b = b[0]
    a_start_x = fl_a.start[0]
    a_start_y = fl_a.start[1]
    a_end_x = fl_a.end[0]
    a_end_y = fl_a.end[1]
    b_start_x = fl_b.start[0]
    b_start_y = fl_b.start[1]
    b_end_x = fl_b.end[0]
    b_end_y = fl_b.end[1]
    fl_a.start = (int((a_start_x + b_start_x) / 2), int((a_start_y + b_start_y) / 2))
    fl_a.end = (int((a_end_x + b_end_x) / 2), int((a_end_y + b_end_y) / 2))
    return [fl_a]

def mutate(a):
    fl_a = a[0]
    a_start_x = fl_a.start[0]
    a_start_y = fl_a.start[1]
    a_end_x = fl_a.end[0]
    a_end_y = fl_a.end[1]
    new_start_x = a_start_x + np.random.randint(20) - 10
    new_start_y = a_start_y + np.random.randint(20) - 10
    new_end_x = a_end_x + np.random.randint(40) - 20
    new_end_y = a_end_y + np.random.randint(40) - 20
    new_start_x = np.clip(new_start_x, 0, 198)
    new_start_y = np.clip(new_start_y, 0, 198)
    new_end_x = np.clip(new_end_x, 0, 198)
    new_end_y = np.clip(new_end_y, 0, 198)
    fl_a.start = (new_start_x, new_start_y)
    fl_a.end = (new_end_x, new_end_y)
    return a

if __name__ == '__main__':
    N = 10
    generations = 1
    pool = multiprocessing.Pool(processes=7)
    # Create initial state
    initial_state = init_del_loma_smol()
    initial_state[7, 150, 150] = 1
    available_resources = {
        'bulldozer': 30
    }
    # Come up with intervention plans
    population = [[
        BullDozedFireLine(
            (130 + np.random.randint(50), 150 - np.random.randint(30) - 15),
            (180 + np.random.randint(30) - 15, 150 - np.random.randint(30) )
        ),
    ] for i in range(N)]
    #slope of good fire line =
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
                         for i in range(7)
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
        new_population = []
        for i in range(N):
            a, b = np.random.choice(len(survivors), 2)
            new_individual = frick(survivors[a], survivors[b])
            # Randomly mutate
            if np.random.random() < 0.5:
                new_individual = mutate(new_individual)
            new_population.append(new_individual)
        population = new_population

    # Test intervention plans
    simulation = SimulationManager()
    final_states = [
        pool.map(simulation_worker,
                    [
                        (
                            deepcopy(initial_state),
                            deepcopy(available_resources),
                            deepcopy(plan),
                            30, False
                        )
                        for i in range(7)
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
    print(final_score_rankings)
    # Get the best one
    best_plan = final_score_rankings[0][0]

    simulation.run_simulation(
        deepcopy(initial_state),
        deepcopy(available_resources),
        [],
        steps=50,
        visualise=True
    )

    simulation.run_simulation(
        deepcopy(initial_state),
        deepcopy(available_resources),
        deepcopy(population[best_plan]),
        steps=50,
        visualise=True
    )

    best_plan = final_score_rankings[1][0]
    simulation.run_simulation(
        deepcopy(initial_state),
        deepcopy(available_resources),
        deepcopy(population[best_plan]),
        steps=50,
        visualise=True
    )

    best_plan = final_score_rankings[2][0]
    simulation.run_simulation(
        deepcopy(initial_state),
        deepcopy(available_resources),
        deepcopy(population[best_plan]),
        steps=50,
        visualise=True
    )

