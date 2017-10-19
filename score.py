import csv
import os
import pendulum
import collections


class Generator():
	def __init__(self, path):
		reader = csv.DictReader(open(path))
		self._site_data = collections.OrderedDict()
		for row in reader:
			self._site_data[row['dt']] = row['energyExport']
		self.site_name = path.split('.csv')[0]
	
	def getGeneration(self, dt):
		if str(dt) in self._site_data:
			return self._site_data[str(dt)]
		else:
			return 0

class Consumer():
	def __init__(self, path):
		reader = csv.DictReader(open(path))
		self._site_data = collections.OrderedDict()
		for row in reader:
			self._site_data[row['dt']] = row['energyImport']
		self.site_name = path.split('.csv')[0]
	
	def getConsumption(self, dt):
		if str(dt) in self._site_data:
			return self._site_data[str(dt)]
		else:
			return 0


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

testDate = pendulum.parse('2017-10-15T10:00:00+00:00')
print "Generation"
for gen in generators:
	print gen.getGeneration(testDate), gen.site_name
print "Consumption"
for con in consumers:
	print con.getConsumption(testDate), con.site_name


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


