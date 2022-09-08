import random
import math
import matplotlib.pyplot as plt
from util import City, read_cities, write_cities_and_return_them, generate_cities, path_cost


class Particle:
    def __init__(self, route, cost=None):
        self.route = route
        self.pbest = route
        self.current_cost = cost if cost else self.path_cost()
        self.pbest_cost = cost if cost else self.path_cost()
        self.velocity_male = []
        self.velocity_female = []

    def clear_velocity(self):
        self.velocity_male.clear()
        self.velocity_female.clear()

    def update_costs_and_pbest(self):
        self.current_cost = self.path_cost()
        if self.current_cost < self.pbest_cost:
            self.pbest = self.route
            self.pbest_cost = self.current_cost

    def path_cost(self):
        return path_cost(self.route)


class PSO:

    def __init__(self, iterations, population_size, gbest_probability=1.0, pbest_probability=1.0, cities=None):
        self.cities = cities
        self.gbest = None
        self.gcost_iter = []
        self.iterations = iterations
        self.population_size = population_size
        self.particles_x = []
        self.particles_y = []
        self.gbest_probability = gbest_probability
        self.pbest_probability = pbest_probability

        solutions = self.initial_population()
        self.particles_x = [Particle(route=solution) for solution in solutions]
        self.particles_y = [Particle(route=solution) for solution in solutions]
       
    def random_route(self):
        rd = random.sample(self.cities[1:],len(self.cities[1:]))
        fd = self.cities[:1]
        return fd+rd

    def initial_population(self):
        random_population = [self.random_route() for _ in range(self.population_size - 1)]
        greedy_population = [self.greedy_route(0)]
        return random_population

    def greedy_route(self, start_index):
        unvisited = self.cities[:]
        del unvisited[start_index]
        # route = self.cities[0]
        route = [self.cities[start_index]]
        while len(unvisited):
            index, nearest_city = min(enumerate(unvisited), key=lambda item: item[1].distance(route[-1]))
            route.append(nearest_city)
            del unvisited[index]
            print(route)
        return route

    def run(self):
        self.gbest = min(self.particles_x and self.particles_y, key=lambda p: p.pbest_cost)
        print(f"Global Best : {self.gbest.pbest_cost}")
        # plt.ion()
        # plt.draw()
        for t in range(self.iterations):
            self.gbest = min(self.particles_x and self.particles_y, key=lambda p: p.pbest_cost)
            print(f'Iter {t} Gbest : {pso.gbest.pbest_cost}')
            if t % 50 == 0:
                plt.figure(0)
                plt.plot(pso.gcost_iter, 'g')
                plt.ylabel('Distance')
                plt.xlabel('Generation')
                fig = plt.figure(0)
                fig.suptitle('pso iter')
                x_list, y_list = [], []
                for city in self.gbest.pbest:
                    x_list.append(city.x)
                    y_list.append(city.y)
                x_list.append(pso.gbest.pbest[0].x)
                y_list.append(pso.gbest.pbest[0].y)
                fig = plt.figure(1)
                fig.clear()
                fig.suptitle(f'pso TSP iter {t}')

                plt.plot(x_list, y_list, 'ro')
                plt.plot(x_list, y_list, 'g')
                plt.draw()
                plt.pause(.001)
            self.gcost_iter.append(self.gbest.pbest_cost)

            for particle in self.particles_x and self.particles_y:
                particle.clear_velocity()
                temp_velocity_male = []
                temp_velocity_female = []
                gbest = self.gbest.pbest[:]
                new_route = particle.route[:]
                # print(new_route)

                for i in range(len(self.cities)):
                    if new_route[i] != particle.pbest[i]:
                        first_route = new_route[0]
                        # print(first_route)
                        if new_route[i] != first_route:
                            swap = (i, particle.pbest.index(new_route[i]), self.pbest_probability)
                            temp_velocity_male.append(swap)
                            temp_velocity_female.append(swap)
                            new_route[swap[0]], new_route[swap[1]] = \
                                new_route[swap[1]], new_route[swap[0]]

                for i in range(len(self.cities)):
                    if new_route[i] != gbest[i]:
                        first_route = new_route[0]
                        # print(first_route)
                        if new_route[i] != first_route:
                            swap = (i, gbest.index(new_route[i]), self.gbest_probability)
                            temp_velocity_male.append(swap)
                            temp_velocity_female.append(swap)
                            gbest[swap[0]], gbest[swap[1]] = gbest[swap[1]], gbest[swap[0]]

                particle.velocity_female = temp_velocity_female
                particle.velocity_male = temp_velocity_male

                for swap in temp_velocity_male:
                    if random.random() <= swap[2]:
                        # if new_route[0] != first_route:
                        new_route[swap[0]], new_route[swap[1]] = \
                            new_route[swap[1]], new_route[swap[0]]
                    # print('swap 0 male')
                    # print(swap[0])
                    # print('swap 1 male')
                    # print(swap[1])
                    # print('swap 2 male')
                    # print(swap[2])

                for swap in temp_velocity_female:
                    if random.random() <= swap[2]:
                        # if new_route[0] != first_route:
                        new_route[swap[0]], new_route[swap[1]] = \
                            new_route[swap[1]], new_route[swap[0]]
                    # print('swap 0 female')
                    # print(swap[0])
                    # print('swap 1 female')
                    # print(swap[1])
                    # print('swap 2 female')
                    # print(swap[2])

                particle.route = new_route
                particle.update_costs_and_pbest()


if __name__ == "__main__":
    cities = read_cities(64)
    pso = PSO(iterations=400, population_size=300, pbest_probability=0.9, gbest_probability=0.02, cities=cities)
    pso.run()
    print(f'cost: {pso.gbest.pbest_cost}\t| gbest: {pso.gbest.pbest}')

    x_list, y_list = [], []
    for city in pso.gbest.pbest:
        x_list.append(city.x)
        y_list.append(city.y)
    x_list.append(pso.gbest.pbest[0].x)
    y_list.append(pso.gbest.pbest[0].y)
    fig = plt.figure(1)
    fig.suptitle('pso TSP')

    plt.plot(x_list, y_list, 'ro')
    plt.plot(x_list, y_list)
    plt.show(block=True)
