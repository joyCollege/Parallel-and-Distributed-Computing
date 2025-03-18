from mpi4py import MPI
import numpy as np
import pandas as pd
from src.genetic_algorithms_functions import calculate_fitness, \
    select_in_tournament, order_crossover, mutate, \
    generate_unique_population
from time import time

def mpi_fitness_worker(routes, distance_matrix, infeasible_penalty):
    """
    Function for MPI workers to evaluate fitness in parallel.
    Each MPI process receives a subset of routes and computes their fitness.
    """
    return np.array([calculate_fitness(route, distance_matrix, infeasible_penalty) for route in routes])

def mpi_genetic_algorithm():
    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()  # Process ID
    size = comm.Get_size()  # Total number of processes

    # Rank 0 loads data and broadcasts to all processes
    if rank == 0:
        startTime = time()

        # Load the distance matrix
        distance_matrix = pd.read_csv('./data/city_distances.csv').to_numpy()

        # Default Parameters
        num_nodes = distance_matrix.shape[0]
        population_size = 10000
        num_tournaments = 4
        tournament_size = 3
        mutation_rate = 0.1
        num_generations = 200
        infeasible_penalty = 1e6
        stagnation_limit = 5

        # Generate initial population
        np.random.seed(42)
        population = generate_unique_population(population_size, num_nodes)

        best_calculate_fitness = int(1e6)
        stagnation_counter = 0

    else:
        distance_matrix = None
        population = None
        num_generations = None
        infeasible_penalty = None

    # Broadcast shared variables
    distance_matrix = comm.bcast(distance_matrix, root=0)
    num_generations = comm.bcast(num_generations, root=0)
    infeasible_penalty = comm.bcast(infeasible_penalty, root=0)

    for generation in range(num_generations):
        # Scatter population among processes
        local_population = comm.scatter(np.array_split(population, size), root=0)

        # 🚀 **Parallel Fitness Evaluation using MPI**
        local_fitness_values = mpi_fitness_worker(local_population, distance_matrix, infeasible_penalty)

        # Gather fitness results back to rank 0
        fitness_values = comm.gather(local_fitness_values, root=0)

        if rank == 0:
            fitness_values = np.concatenate(fitness_values)

            # Stagnation Check
            current_best_calculate_fitness = np.min(fitness_values)
            if current_best_calculate_fitness < best_calculate_fitness:
                best_calculate_fitness = current_best_calculate_fitness
                stagnation_counter = 0
            else:
                stagnation_counter += 1

            # Regenerate population if stagnation limit is reached
            if stagnation_counter >= stagnation_limit:
                best_individual = population[np.argmin(fitness_values)]
                population = generate_unique_population(population_size - 1, num_nodes)
                population.append(best_individual)
                stagnation_counter = 0
                continue  

            # Selection, Crossover, and Mutation (Only on Rank 0)
            selected = select_in_tournament(population, fitness_values, num_tournaments, tournament_size)

            offspring = []
            for i in range(0, len(selected), 2):
                parent1, parent2 = selected[i], selected[i + 1]
                route1 = order_crossover(parent1[1:], parent2[1:])
                offspring.append([0] + route1)

            mutated_offspring = [mutate(route, mutation_rate) for route in offspring]

            # Replace worst individuals
            for i, idx in enumerate(np.argsort(fitness_values)[::-1][:len(mutated_offspring)]):
                population[idx] = mutated_offspring[i]

            # Ensure population uniqueness
            population = np.unique(np.array(population), axis=0).tolist()
            while len(population) < population_size:
                individual = [0] + list(np.random.permutation(np.arange(1, num_nodes)))
                population.append(individual)

    # Rank 0 prints the best solution
    if rank == 0:
        total_time = time() - startTime
        best_idx = np.argmin(fitness_values)
        best_solution = population[best_idx]

        print("\n=== MPI Genetic Algorithm Timing ===")
        print(f"Total Execution Time: {total_time:.2f} seconds")
        print(f"Best Solution: {best_solution}")
        print(f"Total Distance: {calculate_fitness(best_solution, distance_matrix, infeasible_penalty):,}")

        return total_time

# conda activate parallel
# mpirun -np 4 python mpi_genetic_algorithm.py
