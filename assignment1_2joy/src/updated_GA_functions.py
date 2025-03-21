import numpy as np

def generate_unique_population(doneRoutes, population_size, num_nodes):
    """
    Generate a unique population of individuals for a genetic algorithm.

    Each individual in the population represents a route in a graph, where the first node is fixed (0) and the 
    remaining nodes are a permutation of the other nodes in the graph. This function ensures that all individuals
    in the population are unique.

    Parameters:
        - population_size (int): The desired size of the population.
        - num_nodes (int): The number of nodes in the graph, including the starting node.

    Returns:
        - list of lists: A list of unique individuals, where each individual is represented as a list of node indices.
    """
    population = set()
    while len(population) < population_size:
        individual = [0] + list(np.random.permutation(np.arange(1, num_nodes)))
        if individual not in doneRoutes:
            population.add(tuple(individual))
            doneRoutes.append(individual)
    return [list(ind) for ind in population]

def order_crossover(parent1, parent2, num_nodes):
    """
    Order crossover (OX) for permutations using circular filling.
    This function assumes that the fixed starting node (0) should not appear in the variable parts.
    It removes any 0's and then fills in any missing genes from the full set (1 to num_nodes-1).

    Parameters:
        - parent1 (list): The first parent's variable part.
        - parent2 (list): The second parent's variable part.
        - num_nodes (int): Total number of nodes (including the fixed starting node).

    Returns:
        - list: The offspring's variable part.
    """
    # Expected genes: 1 to num_nodes-1
    expected_genes = set(range(1, num_nodes))
    
    # Filter out any 0's if present
    parent1 = [gene for gene in parent1 if gene != 0]
    parent2 = [gene for gene in parent2 if gene != 0]
    
    # Ensure parent's variable parts contain all expected genes (if not, add missing ones)
    missing_from_p1 = list(expected_genes - set(parent1))
    missing_from_p2 = list(expected_genes - set(parent2))
    if missing_from_p1:
        parent1.extend(missing_from_p1)
    if missing_from_p2:
        parent2.extend(missing_from_p2)
    
    size = len(expected_genes)  # This should be num_nodes-1
    start, end = sorted(np.random.choice(range(size), 2, replace=False))
    offspring = [None] * size
    # Copy segment from parent1
    offspring[start:end+1] = parent1[start:end+1]
    
    pos = (end + 1) % size
    for gene in parent2:
        if gene not in offspring:
            offspring[pos] = gene
            pos = (pos + 1) % size

    # Fill any remaining positions with any missing genes
    missing = list(expected_genes - set(offspring))
    for i in range(size):
        if offspring[i] is None:
            if missing:
                offspring[i] = missing.pop(0)
            else:
                raise ValueError("Offspring not fully filled even after correction: " + str(offspring))
    
    if None in offspring:
        raise ValueError("Offspring not fully filled: " + str(offspring))
    
    return offspring