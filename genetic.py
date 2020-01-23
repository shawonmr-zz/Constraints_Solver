# A genetic algorithm file that uses give constraints.py for the fitness calculation

from constraints import Constraint
import numpy as np
import random
from random import gauss, randrange, seed


class Genetic():

    def __init__(self, p, g, fname):
        print('initializing ga')
        self.pop_size = p
        self.gene_size = g
        self.file_name = fname

    def get_population(self):
        pop_size = (self.pop_size, self.gene_size)
        self.pop = np.random.uniform(0.0, 1.0, size=pop_size)
        return self.pop

    def get_filename(self):
        #returns
        return self.file_name

    def get_gen_size(self):

        return self.gene_size;

    def get_pop_size(self):

        return self.pop_size

    def cal_pop_fitness(self):
        # Calculating the fitness value of each solution in the current population.
        # The fitness function calculates fitness by adding the no of constraints that
        # the population passes.
        fitness = []

        fname = self.get_filename()

        c = Constraint(fname)
        for p in self.pop:
            f = c.count_passed_constrain(p)
            fitness.append(f)
        return fitness

    def get_constrain(self):
        fname = self.get_filename()
        c = Constraint(fname)
        self.no_of_constrain = c.get_no_of_constrain()
        return self.no_of_constrain

    def select_mating_pool(self, fitness, num_parents):
        # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
        parents = np.empty((num_parents, self.pop.shape[1]))
        for parent_num in range(num_parents):
            max_fitness_idx = np.where(fitness == np.max(fitness))
            max_fitness_idx = max_fitness_idx[0][0]
            parents[parent_num, :] = self.pop[max_fitness_idx, :]
            fitness[max_fitness_idx] = -99999999999
        return parents

    def crossover(self, parents, offspring_size):
        offspring = np.empty(offspring_size)
        # The point at which crossover takes place between two parents. Usually it is at the center.
        # crossover_point = np.uint8(offspring_size[1] / 2)
        crossover_point = randrange(offspring_size[1])
        for k in range(offspring_size[0]):
            # Index of the first parent to mate.
            parent1_idx = k % parents.shape[0]
            # Index of the second parent to mate.
            parent2_idx = (k + 1) % parents.shape[0]
            # The new offspring will have its first half of its genes taken from the first parent.
            offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
            # The new offspring will have its second half of its genes taken from the second parent.
            offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
        return offspring

    def mutation(self, offspring_crossover):
        # Mutation changes a single gene in each offspring randomly.
        for idx in range(offspring_crossover.shape[0]):
            # The random value to be added to the gene.
            pos = randrange(offspring_crossover.shape[1])  # generate a random value position for mutation
            # random_value = np.random.uniform(0.0, 1.0, 1)
            # offspring_crossover[idx, pos] = offspring_crossover[idx, pos] + random_value
            #offspring_crossover[idx, pos] = random.random()
            offspring_crossover[idx, pos] = np.random.uniform(0.0, 1.0, 1)
        return offspring_crossover

    def eval_ga(self, ncount):
        nconstrain = self.get_constrain()
        gsize = self.get_gen_size()
        psize = 20  #no of unique solution that will distributed for non successful population generation
        print('Total no of constrain', nconstrain)
        total_best_pop_count = 0
        generation = 1
        temp_solution = []
        while int(total_best_pop_count) <= int(ncount):
            seed(1)
            # for generation in range(num_generations):
            print("Generation : ", generation)
            # Measing the fitness of each chromosome in the population.
            fitness = self.cal_pop_fitness()

            # num_parents_mating = randrange(self.pop.shape[0])
            num_parents_mating = int(self.pop.shape[0] / 2)
            #num_parents_mating = int(self.pop.shape[0])
            # Selecting the best parents in the population for mating.
            parents = self.select_mating_pool(fitness,
                                              num_parents_mating)

            # Generating next generation using crossover.
            offspring_crossover = self.crossover(parents,
                                                 offspring_size=(
                                                 self.pop.shape[0] - parents.shape[0], self.pop.shape[1]))

            # Adding some variations to the offsrping using mutation.
            offspring_mutation = self.mutation(offspring_crossover)

            # Creating the new population based on the parents and offspring.
            self.pop[0:parents.shape[0], :] = parents
            self.pop[parents.shape[0]:, :] = offspring_mutation

            # The best result in the current iteration.
            temp_fitness = self.cal_pop_fitness()
            max_fitness = np.max(temp_fitness)

            temp_pop_count = 0


            for i in range(len(temp_fitness)):
                if temp_fitness[i] == nconstrain:
                    temp_solution.append(self.pop[i, :].tolist())
                    total_best_pop_count += 1
                    temp_pop_count += 1
                    for j in range(gsize):
                        self.pop[i,j] = np.random.uniform(0.0, 1.0, 1) #reinitializing the best fit population

                    #self.pop[i, :] = np.random.uniform(0.0, 1.0, 1)  # reinitializing the best fit population
            if temp_pop_count == 0 and len(temp_solution) > psize:
                psize = self.get_pop_size()
                for j in range(psize):
                    ind = randrange(len(temp_solution))
                    #print('assigning',temp_solution[ind][:])
                    self.pop[j,:] = temp_solution[ind][:]
            generation += 1
            print("Best result : ", max_fitness)
            print("Best population : ", temp_solution)
            print("Total no of best population : ", total_best_pop_count)
            print("\n")

            #if total_best_pop_count == ncount:
            #    break
        return temp_solution[:ncount][:] #returns the best fit population