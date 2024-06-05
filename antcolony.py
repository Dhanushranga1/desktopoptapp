import random
import math

class AntColonyAlgorithm:
    def __init__(self, num_ants, num_iterations, pheromone_evaporation_rate, pheromone_deposit_rate):
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.pheromone_evaporation_rate = pheromone_evaporation_rate
        self.pheromone_deposit_rate = pheromone_deposit_rate

    def initialize_ants(self, fabric_rolls):
        self.ants = []
        for _ in range(self.num_ants):
            ant = {'path': [], 'pheromone': {}}
            for roll in fabric_rolls:
                ant['path'].append(random.choice(roll['from']))
                ant['pheromone'][roll['from'][0]] = 1.0
            self.ants.append(ant)

    def calculate_distance(self, ant, roll):
        distance = 0
        for i in range(len(ant['path']) - 1):
            distance += abs(roll['from'][i] - roll['from'][i + 1])
        return distance

    def update_pheromone(self, ant, roll):
        for i in range(len(ant['path']) - 1):
            pheromone = ant['pheromone'].get(roll['from'][i], 0)
            ant['pheromone'][roll['from'][i]] = pheromone * (1 - self.pheromone_evaporation_rate) + self.pheromone_deposit_rate

    def optimize_fabric(self, fabric_rolls):
        self.initialize_ants(fabric_rolls)
        for _ in range(self.num_iterations):
            for ant in self.ants:
                for roll in fabric_rolls:
                    if roll['from'][0] in ant['path']:
                        distance = self.calculate_distance(ant, roll)
                        if random.random() < 1 / (distance + 1):
                            ant['path'].append(roll['from'][0])
                            self.update_pheromone(ant, roll)
        return self.ants

# Example usage
fabric_rolls = [
    {'from': [7, 15, 23, 25, 28, 30, 41, 41, 52, 66, 68, 71, 76],
     'to': [7, 15, 23, 25, 28, 30, 41, 41, 52, 66, 68, 71, 76],
     'name': ['HOLE', 'MISSING END', 'MISSING END', 'RUST STAIN', 'HANDLING STAIN', 'LOOSE WARP', 'MISSING END', 'SLUB', 'RUST STAIN', 'HANDLING STAIN', 'HANDLING STAIN', 'MISSING END', 'WRONG END'],
     'type': ['MAJOR', 'MINOR', 'MAJOR', 'MINOR', 'MINOR', 'MINOR', 'MINOR', 'MAJOR', 'MINOR', 'MAJOR', 'MAJOR', 'MINOR', 'MAJOR'],
     'points': [4, 1, 5, 1, 4, 1, 4, 4, 1, 4, 4, 1, 4],
     'length': 88.7
    },
    {'from': [3, 27, 37, 46, 48, 54, 58, 67, 75, 76],
     'to': [3, 27, 37, 46, 48, 54, 58, 67, 75, 76],
     'name': ['CONTOMINATION', 'WRONG END', 'SLUB YARN', 'SLUB YARN', 'SLUB YARN', 'CONTOMINATION', 'MISSING END', 'BROKEN PICK', 'SLUB YARN', 'SLUB YARN'],
     'type': ['MINOR', 'MAJOR', 'MAJOR', 'MAJOR', 'MAJOR', 'MAJOR', 'MINOR', 'MAJOR', 'MAJOR', 'MAJOR'],
     'points': [2, 4, 4, 4, 4, 4, 1, 4, 4, 4],
     'length': 81.1
    }
]

num_ants = 10
num_iterations = 100
pheromone_evaporation_rate = 0.1
pheromone_deposit_rate = 0.1

ant_colony = AntColonyAlgorithm(num_ants, num_iterations, pheromone_evaporation_rate, pheromone_deposit_rate)
optimized_ants = ant_colony.optimize_fabric(fabric_rolls)

# Print the optimized paths
for ant in optimized_ants:
    print(ant['path'])