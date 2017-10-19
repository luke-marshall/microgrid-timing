import csv
import os
import pendulum
import collections
import numpy as np


class Generator():
	def __init__(self, path):
		reader = csv.DictReader(open(path))
		self._site_data = collections.OrderedDict()
		for row in reader:
			self._site_data[row['dt']] = float(row['energyExport'])
		self.site_name = path.split('.csv')[0]
		self.result = {}
	
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
		while time < endDt:
			total += self._getGeneration(time)
		return total


class Consumer():
	def __init__(self, path):
		reader = csv.DictReader(open(path))
		self._site_data = collections.OrderedDict()
		for row in reader:
			self._site_data[row['dt']] = float(row['energyImport'])
		self.site_name = path.split('.csv')[0]
		self.result = {}
	
	def _getConsumption(self, dt):
		if str(dt) in self._site_data:
			return self._site_data[str(dt)]
		else:
			return 0
	
	def getConsumption(self, dt, period_mins):
		endDt = dt.copy().add(minutes=(period_mins))
		# Ensure the time period is a multiple of the dataset data ie. 5 minute. 
		assert period_mins % 5 == 0
		total = 0
		while time < endDt:
			total += self._getConsumption(time)
		return total





def fractionAllocation(consumers, generators, startDt, endDt):
	time = startDt
	# Throw error if dates entered the wrong way round. 
	assert startDt < endDt
	while time < endDt:
		# Step time forwad by 5 mins. 
		time = time.copy().add(minutes=5)
		
		# Setup here
		# get total consumption and total generation
		total_consumption = sum(consumer.getConsumption(time) for consumer in consumers)
		total_generation = sum(generator.getGeneration(time) for generator in generators)\
		# Calculate the network and local solar use in total. 
		apparent_network_import = max(total_consumption - total_generation, 0)
		apparent_network_export = max(total_generation - total_consumption, 0)
		apparent_local_energy = min(total_consumption,total_generation)
		# Verify that consumption is the sum of import and local gen. 
		np.testing.assert_allclose(total_consumption, apparent_network_import + apparent_local_energy, rtol=1e-5, atol=0)
		
		# Algorithm begins here
		# Calculate the local solar fraction 
		consumer_p2p_fraction = apparent_local_energy / total_consumption


		# print the results. 
		print time, total_consumption, total_generation, apparent_network_import, apparent_network_export, p2p_fraction
		
		

		# If there is no network import, all loads


# Iterate over all files in the data directory and add to sites dict. 
data_directory = 'data'
sites = {}

generators = []
consumers = []
for filename in os.listdir(data_directory):
    if filename.endswith(".csv"): 
		path = os.path.join(data_directory, filename)
		generators.append(Generator(path))
		consumers.append(Consumer(path))
    else:
        continue

startDate = pendulum.parse('2017-10-15T10:00:00+00:00')
endDate = startDate.copy().add(days=1)

fractionAllocation(consumers, generators, startDate, endDate)

# print "Generation"
# for gen in generators:
# 	print gen.getGeneration(testDate), gen.site_name
# print "Consumption"
# for con in consumers:
# 	print con.getConsumption(testDate), con.site_name
















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


