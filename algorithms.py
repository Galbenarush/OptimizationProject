"""
Gal Ben Arush
Shir Zituni
"""

from deap import algorithms

from utils import nsgaToolbox, statsGen

'''
The algorithms module is intended to contain some specific algorithms
in order to execute very common evolutionary algorithms.
'''

'''
Run Genetic Algorithm
'''
def runGeneticAlgorithm(toolbox = nsgaToolbox, popSize = 50, maxGen = 10, mutProb = 0.1, stats = statsGen, hallOfFame = None):
	pop = toolbox.population(n = popSize)
	pop = toolbox.select(pop, len(pop))

	# Run evolutionary algorithm using deap algorithms
	return algorithms.eaMuPlusLambda(
		pop,
		toolbox,
		mu = popSize,
		lambda_ = popSize,
		cxpb = 1.0 - mutProb,
		mutpb = mutProb,
		stats = stats,
		ngen = maxGen,
		halloffame = hallOfFame,
		verbose = False
	)


'''
Run Random Algorithm
'''
def runRandom(toolbox = nsgaToolbox, popSize = 50, maxGen = 10):
	currentGen = 0
	allGenerations, fitnessesPerGen = [], []

	# Use toolbox only to generate population
	population = toolbox.population(n = popSize)

	while currentGen < maxGen:
		allGenerations.append(population)
		fitnessesPerGen.append(
			list(toolbox.map(toolbox.evaluate, population))
		)
		population = toolbox.population(n = popSize)
		currentGen += 1
	return allGenerations, fitnessesPerGen


if __name__ == '__main__':
	# print results
	print(runGeneticAlgorithm())
	print(runRandom())

