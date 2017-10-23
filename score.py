import csv
import os
import pendulum
import collections
from collections import OrderedDict
import numpy as np


from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.layouts import column


class Generator():
	def __init__(self, path):
		reader = csv.DictReader(open(path))
		self._site_data = collections.OrderedDict()
		for row in reader:
			self._site_data[row['dt']] = float(row['energyExport'])
		self.site_name = path.split('.csv')[0]
		self.result = OrderedDict()
	
	def _getGeneration(self, dt):
		if str(dt) in self._site_data:
			return self._site_data[str(dt)]
		else:
			return 0
	
	def getGeneration(self, dt, period_mins):
		endDt = dt.copy().add(minutes=(period_mins))
		# Ensure the time period is a multiple of the dataset data ie. 5 minute. 
		assert period_mins % 5 == 0, "generatorPeriod_mins must be a multiple of 5. s"
		total = 0
		time = dt.copy()
		while time < endDt:
			total += self._getGeneration(time)
			time = time.add(minutes=5)
		return total


class Consumer():
	def __init__(self, path):
		reader = csv.DictReader(open(path))
		self._site_data = collections.OrderedDict()
		for row in reader:
			self._site_data[row['dt']] = float(row['energyImport'])
		self.site_name = path.split('.csv')[0]
		self.result = OrderedDict()
	
	def _getConsumption(self, dt):
		if str(dt) in self._site_data:
			return self._site_data[str(dt)]
		else:
			return 0
	
	def getConsumption(self, dt, period_mins):
		
		# Ensure the time period is a multiple of the dataset data ie. 5 minute. 
		assert period_mins % 5 == 0
		endDt = dt.copy().add(minutes=period_mins)
		total = 0
		time = dt.copy()
		while time < endDt:
			total += self._getConsumption(time)
			time = time.add(minutes=5)
		return total





def fractionAllocation(consumers, generators, startDt, endDt, period_mins):
	print "Determining fraction allocation, mins: ",period_mins
	assert period_mins % 5 == 0

	results = OrderedDict()
	# Throw error if dates entered the wrong way round. 
	assert startDt < endDt
	time = startDt.copy()
	while time < endDt:
		# Step time forward by 5 mins. 
		time = time.copy().add(minutes=period_mins)
		
		# Setup here
		
		# get total consumption and total generation
		total_consumption = sum([consumers[consumer].getConsumption(time, period_mins) for consumer in consumers])
		total_generation = sum(generators[generator].getGeneration(time, period_mins) for generator in generators)
		# Calculate the network and local solar use in total. 
		apparent_network_import = max(total_consumption - total_generation, 0)
		apparent_network_export = max(total_generation - total_consumption, 0)
		apparent_local_energy = min(total_consumption,total_generation)
		# Verify that consumption is the sum of import and local gen. 
		np.testing.assert_allclose(total_consumption, apparent_network_import + apparent_local_energy, rtol=1e-5, atol=0)
		
		# Algorithm begins here
		# Calculate the local solar fractions
		consumer_p2p_fraction = apparent_local_energy / total_consumption if total_consumption > 0 else 0
		generator_p2p_fraction = apparent_local_energy / total_generation if total_generation > 0 else 0
		
		# Allocate each consumer's p2p energy.
		consumer_p2p = OrderedDict()
		for consumer_name in consumers:
			consumer = consumers[consumer_name]
			# Consumer's energy consumption is given by fraction * total consumption.
			e_p2p = consumer_p2p_fraction * consumer.getConsumption(time, period_mins)
			# Record the p2p consumption.
			consumer_p2p[consumer_name] = e_p2p

		# Allocate each generator's p2p energy. 
		generator_p2p = OrderedDict()
		for generator_name in generators:
			generator = generators[generator_name]
			# Generator's energy consumption is given by fraction * total generation.
			g_p2p = generator_p2p_fraction * generator.getGeneration(time, period_mins)
			# Record the p2p generation
			generator_p2p[generator_name] = g_p2p
		
		# print the results. 
		# print time, total_consumption, total_generation, apparent_network_import, apparent_network_export, consumer_p2p_fraction
		
		#Add the latest calculations to the results list.  
		# results.append({
		# 	'dt': time,
		# 	'consumer_p2p': consumer_p2p,
		# })
		results[time] = {
			'consumer_p2p': consumer_p2p,
			'generator_p2p':generator_p2p
		}
	
	#Spit out the results as a python dictionary.
	return results

		# If there is no network import, all loads

# Calculates the score for each time period / customer. 
def calculateScore(data_short, data_long, short_period_mins, long_period_mins, generators, consumers):
	results = OrderedDict()
	# Iterate through each of hte longer time periods. Skip last to stop annoying errors to do with trailing time periods & dataset mismatches.
	for time in data_long.keys()[:-4]:
		# print time
		# Object to store scores for consumers. 
		consumer_scores = OrderedDict()
		# Calculate score for each consumer. 
		for consumer_name in data_long[time]['consumer_p2p']:
			# Get the e_p2p_long long time period p2p energy from the longer time period data. 
			e_p2p_long = data_long[time]['consumer_p2p'][consumer_name]
			# Find the total p2p Short energy ie. Sum of all P2p energy at short timescale that fits into long timescale. 
			e_p2p_short =0
			current = time.copy()
			end = time.copy().add(minutes=long_period_mins)
			while current < end:
				e_p2p_short += data_short[current]['consumer_p2p'][consumer_name]
				current = current.add(minutes=short_period_mins)
			# Get total consumption
			total_consumption_long = consumers[consumer_name].getConsumption(time, long_period_mins)
			# Calculate score Dk
			score = abs(e_p2p_long - e_p2p_short) / total_consumption_long if total_consumption_long > 0 else None
			consumer_scores[consumer_name] = score

		# Object to store scores for generators
		generator_scores = OrderedDict()
		# Calculate score for each generator
		for generator_name in data_long[time]['generator_p2p']:
			# get the g_p2p_long loing time period p2p generation from the longer time period data. 
			g_p2p_long = data_long[time]['generator_p2p'][generator_name]
			# Find the total P2p short generation ie sum of all p2p generation at short timescale that fits into long timescale. 
			g_p2p_short = 0
			current = time.copy()
			end = time.copy().add(minutes=long_period_mins)
			while current < end:
				g_p2p_short += data_short[current]['generator_p2p'][generator_name]
				current = current.add(minutes=short_period_mins)
			# Get total generation
			total_generation_long = generators[generator_name].getGeneration(time,long_period_mins)
			# Calculate the score Dk
			score = abs(g_p2p_long - g_p2p_short) / total_generation_long if total_generation_long > 0 else None
			# Store the score from the generator. 
			generator_scores[generator_name] = score

		results[time] = {
			'generator_scores':generator_scores,
			'consumer_scores':consumer_scores
		}
	return results

def calculateAverageScores(scores):
	consumer_results = OrderedDict()
	generator_results = OrderedDict()
	generator_counter = 0
	consumer_counter = 0
	# Go through each time. 
	for time in scores:
		for consumer_name in scores[time]['consumer_scores']:
			# Get the score from the results object
			score = scores[time]['consumer_scores'][consumer_name]
			# Check if score exists here. 0 is good so null results ie no generation are recorded with None.
			if score: 
				consumer_results[consumer_name] = consumer_results[consumer_name] + score if consumer_name in consumer_results else score
				# Increase Counter for later averaging. 
				consumer_counter += 1
		
		for generator_name in scores[time]['generator_scores']:
			# Get the score from the results object. 
			score = scores[time]['generator_scores'][generator_name]
			# Check if score exists here. 0 is good so null results ie no generation are recorded with None.
			if score:
				# Add to cumulative total 
				generator_results[generator_name] = generator_results[generator_name] + score if generator_name in generator_results else score
				# Increase counter for later averaging. 
				generator_counter += 1
	
	for consumer_name in consumer_results:
		consumer_results[consumer_name] = consumer_results[consumer_name] / consumer_counter if consumer_counter > 0 else None
	for generator_name in generator_results:
		generator_results[generator_name] = generator_results[generator_name] / generator_counter if generator_counter > 0 else Nones
	return {
		'consumer_results':consumer_results,
		'generator_results':generator_results
	}

# Iterate over all files in the data directory and add to sites dict. 
data_directory = 'data'
sites = OrderedDict()

generators = OrderedDict()
consumers = OrderedDict()
for filename in os.listdir(data_directory):
    if filename.endswith(".csv"): 
		path = os.path.join(data_directory, filename)
		generator = Generator(path)
		generators[generator.site_name] = generator
		consumer = Consumer(path)
		consumers[consumer.site_name] = consumer
    else:
        continue

startDate = pendulum.parse('2017-10-05T10:00:00+00:00')
endDate = startDate.copy().add(days=1)
print "Running Sim"

result_fa_5 = fractionAllocation(consumers, generators, startDate, endDate, 5)
result_fa_10 = fractionAllocation(consumers, generators, startDate, endDate, 10)
result_fa_15 = fractionAllocation(consumers, generators, startDate, endDate, 15)
result_fa_20 = fractionAllocation(consumers, generators, startDate, endDate, 20)
result_fa_25 = fractionAllocation(consumers, generators, startDate, endDate, 25)
result_fa_30 = fractionAllocation(consumers, generators, startDate, endDate, 30)

scores_10 = calculateScore(result_fa_5, result_fa_10, 5, 10, generators, consumers)
scores_15 = calculateScore(result_fa_5, result_fa_15, 5, 15, generators, consumers)
scores_20 = calculateScore(result_fa_5, result_fa_20, 5, 20, generators, consumers)
scores_25 = calculateScore(result_fa_5, result_fa_25, 5, 25, generators, consumers)
scores_30 = calculateScore(result_fa_5, result_fa_30, 5, 30, generators, consumers)

averages_10 = calculateAverageScores(scores_10)
averages_15 = calculateAverageScores(scores_15)
averages_20 = calculateAverageScores(scores_20)
averages_25 = calculateAverageScores(scores_25)
averages_30 = calculateAverageScores(scores_30)



output_file("bar_nested_colormapped.html")

labels = [str(idx) for idx in range(len(averages_10['consumer_results'].keys()))]
years = ['10 Min', '15 Min',  '20 Min', '25 Min','30 Min']

data = {'labels' : labels,
        '10 Min'   : [averages_10['consumer_results'][c] for c in averages_10['consumer_results']],
		'15 Min'   : [averages_15['consumer_results'][c] for c in averages_10['consumer_results']],
		'20 Min'   : [averages_20['consumer_results'][c] for c in averages_10['consumer_results']],
		'25 Min'   : [averages_25['consumer_results'][c] for c in averages_10['consumer_results']],
        '30 Min'   : [averages_30['consumer_results'][c] for c in averages_10['consumer_results']],
}

palette = ["#c9d9d3", "#718dbf", "#e84d60"]

# this creates [ ("Apples", "10 Min"), ("Apples", "30 Min"), ("Apples", "2017"), ("Pears", "10 Min), ... ]

# Plot number 1
x = [ (label, year) for label in labels for year in years ]
counts = sum(zip(data['10 Min'], data['15 Min'],  data['20 Min'], data['25 Min'],data['30 Min']), ()) # like an hstack

source = ColumnDataSource(data=dict(x=x, counts=counts))


p = figure(x_range=FactorRange(*x), plot_height=350, plot_width=800, title="Consumer Average Dk Scores - Fractional Allocation Method",
           toolbar_location=None, tools="")

p.vbar(x='x', top='counts', width=0.9, source=source, line_color="white",
       fill_color=factor_cmap('x', palette=palette, factors=years, start=1, end=2))

p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xaxis.major_label_orientation = 1
p.xgrid.grid_line_color = None

# Plot number 2
p2 = figure(x_range=FactorRange(*x), plot_height=350, plot_width=800, title="Consumer Average Dk Scores - Fractional Allocation Method",
           toolbar_location=None, tools="")

p2.vbar(x='x', top='counts', width=0.9, source=source, line_color="white",
       fill_color=factor_cmap('x', palette=palette, factors=years, start=1, end=2))

p2.y_range.start = 0
p2.x_range.range_padding = 0.1
p2.xaxis.major_label_orientation = 1
p2.xgrid.grid_line_color = None

show(p)
show(column(p, p2))














# # Find latest start date and earliest end date.
# start = pendulum.create(2000,1,1)
# end = pendulum.now()


# # for filename in os.listdir(data_directory):
# #     if filename.endswith(".csv"): 
# # 		path = os.path.join(data_directory, filename)
# # 		reader = csv.DictReader(open(path))
# # 		site_data = []
# # 		for row in reader:
# # 			site_data.append(row)
# # 		if pendulum.parse(site_data[0]['dt']) > start:
# # 			start = pendulum.parse(site_data[0]['dt'])
# # 			print ">>>>>>>>>>>>>>>>>>>>>>>> new start", start
# # 		if pendulum.parse(site_data[-1]['dt']) < end:
# # 			end = pendulum.parse(site_data[-1]['dt'])
# # 			print ">>>>>>>>>>>>>>>>>>>>>>>> new end", end
# # 		site_name = filename.split('.csv')[0]
# # 		print site_name, site_data[-1]
# # 		sites[site_name] = site_data
# #     else:
# #         continue

# # Remove dates before official start date. 
# print "REMOVING DATES"
# for site in sites:
# 	to_remove = []
# 	for idx, dp in enumerate(sites[site]):
# 		if pendulum.parse(dp['dt']) < start or pendulum.parse(dp['dt']) > end:
# 			to_remove.append(idx)
# 	print site, to_remove
# 	updated_list = [e for idx, e in enumerate(sites[site]) if idx not in to_remove]
# 	sites[site] = updated_list



# # for site in sites:
# # 	# print site
# # 	print sites[site][0], site

# for site in sites:
# 	# print site
# 	print len(sites[site]),sites[site][-1], pendulum.parse(sites[site][-1]['dt']), site




# print start
# print end


