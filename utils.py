from deap import base, tools, creator
from random import randint
from copy import deepcopy
from data import data
import numpy

'''
Score functions in order to get score vectors
'''


def value(requirement=-1, customer={'requirements': []}):
	'''
	How valuable a requirement is to a customer.
	Returns a value between 0 and 1.
	1 for the first requirement,
	proportionally smaller to customer requirements length thereafter.
	'''
	requirements = customer['requirements']
	if requirement in requirements:
		length = len(requirements)

		return (length - requirements.index(requirement)) / length
	return 0.0


def score(requirement=-1, customers=[{'weight': 0.0, 'requirements': []}]):
	'''
	The sum of scores of a requirement for each customer.
	'''
	score = 0
	for customer in customers:
		score += customer['weight'] * value(requirement, customer)
	return score


def getScoreVector(dataSet={
	'requirementCosts': [],
	'customers': [{'weight': 0.0, 'requirements': []}]
}):
	result, numberOfRequirements = [], len(dataSet['requirementCosts'])

	for i in range(numberOfRequirements):
		currentScore = score(i, dataSet['customers'])

		result.append(currentScore)
	return result

'''
UTILS
'''


# here we need to insert the relevant dataset
dataSet = data['dataset.txt']

scoreVector = getScoreVector(dataSet)
costVector = dataSet['requirementCosts']


# Create a fitness Type,
# maximise first (score), minimise second (cost) element
creator.create('FitnessMaxMin', base.Fitness, weights = (1.0, -1.0))

# Create an Individual type that will have the fitness declared above
creator.create('Individual', list, typecode = 'd', fitness = creator.FitnessMaxMin)

nsgaToolbox = base.Toolbox()

# Make functions that will be called later,
# first argument is name of the function,
# second is the actual function being called,
# all arguments after are passed to function being called

# Each solution will be made up of bools
nsgaToolbox.register('attr_bool', randint, 0, 1)

# and will be 'n' elements long
nsgaToolbox.register('individual', tools.initRepeat, creator.Individual, nsgaToolbox.attr_bool, n = len(costVector))
nsgaToolbox.register('population', tools.initRepeat, list, nsgaToolbox.individual)


# Fitness Function
def getFitness(requirementVec = [], scoreVec = scoreVector, costVec = costVector):
	score = numpy.dot(scoreVec, requirementVec)
	cost = numpy.dot(costVec, requirementVec)

	return score, cost


nsgaToolbox.register('evaluate', getFitness)
nsgaToolbox.register('mate', tools.cxTwoPoint)
nsgaToolbox.register('mutate', tools.mutFlipBit, indpb = 0.05)
nsgaToolbox.register('select', tools.selNSGA2)


# Make a single objective toolbox
creator.create('FitnessMax', base.Fitness, weights = (1.0,))
creator.create('SingleObjIndividual', list, typecode = 'd', fitness = creator.FitnessMax)

singleObjToolbox = base.Toolbox()
singleObjToolbox.register('attr_bool', randint, 0, 1)
singleObjToolbox.register('individual', tools.initRepeat, creator.SingleObjIndividual, singleObjToolbox.attr_bool, n = len(costVector))
singleObjToolbox.register('population', tools.initRepeat, list, singleObjToolbox.individual)


# Fitness Function
def getSingleFitness(requirementVec = [], scoreVec = scoreVector, costVec = costVector):
	score = numpy.dot(scoreVec, requirementVec)
	cost = numpy.dot(costVec, requirementVec)

	# Return a sequence with one element
	return score / cost,


singleObjToolbox.register('evaluate', getSingleFitness)
singleObjToolbox.register('mate', tools.cxTwoPoint)
singleObjToolbox.register('mutate', tools.mutFlipBit, indpb = 0.05)
singleObjToolbox.register('select', tools.selTournament, tournsize = 3)

# Export stats objects
statsGen = tools.Statistics()
statsGen.register('allGenerations', deepcopy)

# Needs to be passed population of fitness
statsFit = tools.Statistics()
statsFit.register('avg', numpy.mean, axis = 0)
statsFit.register('std', numpy.std, axis = 0)
statsFit.register('min', numpy.min, axis = 0)
statsFit.register('max', numpy.max, axis = 0)