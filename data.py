"""
This is a class for data loading and and spliting to requirement costs and customers
"""

import os
from itertools import chain

location = os.path.realpath(
	os.path.join(os.getcwd(), os.path.dirname(__file__))
)

filePaths = [
	os.path.join(location, '/dataset.txt'),
]

#
'''
	Data will be in this form:
	data = {
		textFileName: {
			requirementCosts: number[],
			customers: [
				{ weight: float, requirements: number[] },
				...
			]
		}
	}
'''
data = {}
rows = []

for line in open('dataset.txt'):
	split_strings = [string.strip('\n') for string in line.split(' ')]

	# Filter empty strings
	filtered = list(filter(None, split_strings))
	numbers = list(map(int, filtered))
	rows.append(numbers)


numLevels = rows[0][0]
requirementCosts = rows[1:numLevels * 2 + 1:]

# Flatten [[1], [2, 3], ...] to [1, 2, 3, ...]
requirementCosts = list(chain(*requirementCosts[1::2]))

withoutRequirementCosts = rows[numLevels * 2 + 1:]
rowsToSkip = withoutRequirementCosts[0][0]

customerRows = withoutRequirementCosts[rowsToSkip + 2:]

data['dataset.txt'] = {
	'requirementCosts': requirementCosts[:],
	'customers': [],
}

profitsSum = sum([element[0] for element in customerRows])

for row in customerRows:
	profit = row[0]

	data['dataset.txt']['customers'].append({
		'weight': profit / profitsSum,
		'requirements': row[2:]
	})