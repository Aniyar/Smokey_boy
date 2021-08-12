from .simulation import init_del_loma_smol
from .simulation_manager import SimulationManager
from .simulation.interventions import *
import numpy as np
from copy import deepcopy

def fitness(X):
    return -np.sum(X[7, :, :])

if __name__ == '__main__':
    N = 3
    simulation = SimulationManager()
    # Create initial state
    initial_state = init_del_loma_smol()
    initial_state[7, 150, 150] = 1
    available_resources = {
        'bulldozer': 3
    }
    # Come up with intervention plans
    intervention_plans = [[
        BullDozedFireLine(
            (150 + np.random.randint(30) - 15, 150 + np.random.randint(30) - 15),
            (150 + np.random.randint(30) - 15, 150 + np.random.randint(30) - 15)
        ),
    ] for i in range(N)]
    # Test intervention plans
    final_states = [
        simulation.run_simulation(deepcopy(initial_state), deepcopy(available_resources), plan, steps=30, visualise=True)
        for plan in intervention_plans
    ]
    # Evaluate the final states
    final_scores = [fitness(state) for state in final_states]
    best, worst = np.argmax(final_scores), np.argmin(final_scores)
    print(best, worst)
    simulation.run_simulation(deepcopy(initial_state), deepcopy(available_resources), intervention_plans[best], steps=30, visualise=True)
    simulation.run_simulation(deepcopy(initial_state), deepcopy(available_resources), intervention_plans[worst], steps=30, visualise=True)