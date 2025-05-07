# In[0]: imports
from pathlib import Path
import sys
root = Path(__file__).parent.parent.parent.resolve()
sys.path.append(str(root))
from tsp import TSP
import numpy as np
import itertools
import math

#  In[1]: Create dummy data
np.random.seed(0)
num_cities =5
coords = np.random.randn(num_cities,2)
towns = list(range(num_cities))
edges = list(itertools.combinations(range(num_cities), r=2))
tsp = TSP(coords)
distances_dict = {edge: distance for
                   edge, distance in zip(edges, tsp.distances)}

print('Distances based on TSP solver: ', tsp.distances)
print('Possible edges: ', edges)
print('Towns: ', towns)
print('Distances dict: ', distances_dict)

# In[3] Brute forch
def calculate_route_cost(tour: list[str],
                         distances:dict):
    list_of_edges = list(itertools.pairwise(tour))
    cost = 0
    for (start, end) in list_of_edges:
        try:
            cost += distances[(start, end)]
        except KeyError:
            cost += distances[(end, start)]
    try:
        cost += distances[(tour[-1], tour[0])]
    except KeyError:
        cost += distances[(tour[0], tour[-1])]
    return cost

def find_optimal_tour(towns:list,
                      distances:dict):
    
    min_distance = np.inf
    best_tour = None
    for tour in itertools.permutations(towns):
        tour_cost = calculate_route_cost(tour, distances)
        if tour_cost < min_distance:
            min_distance = tour_cost
            best_tour = tour

    return min_distance, best_tour

print(f'Brute force approach: {find_optimal_tour(towns, distances_dict)}')
print(f'Solver approach: ', tsp.minimum_distance, tsp.optimal_tour)
        


# %%
def optimal_tour_as_set_of_tuples(optimal_tour: list[int]):
    list_of_edges = [frozenset(pair) for pair in itertools.pairwise(optimal_tour)]
    list_of_edges.append(
            frozenset((optimal_tour[-1],optimal_tour[0]))
                )
    return set(list_of_edges)


def compare_solver_with_brute_force(num_cities):
    coords = np.random.randn(num_cities,2)
    towns = list(range(num_cities))
    edges = list(itertools.combinations(range(num_cities), r=2))

    tsp = TSP(coords)
    distances_dict = {edge: distance for
                      edge, distance in zip(edges, tsp.distances)}
    
    min_dist, opt_tour = find_optimal_tour(towns, distances_dict)
    assert math.isclose(min_dist, tsp.minimum_distance,
                        abs_tol=0.0001) , \
    f"{min_dist},{tsp.minimum_distance}"

    assert optimal_tour_as_set_of_tuples(opt_tour) == optimal_tour_as_set_of_tuples(tsp.optimal_tour), \
    f"{optimal_tour_as_set_of_tuples(opt_tour)},{optimal_tour_as_set_of_tuples(tsp.optimal_tour)}"
    
    return 'Solver return the same results with the brute force approach'


# %%
for _ in range(10):
    np.random.seed(_)
    num_cities = np.random.randint(low=5, high=10)
    print('Testing for num_cities: ', num_cities)
    compare_solver_with_brute_force(num_cities)
# %%
