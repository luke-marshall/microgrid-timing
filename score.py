import csv
import os
import pendulum

# Iterate over all files in the data directory and add to sites dict. 
data_directory = 'data'
sites = {}

# Find latest start date and earliest end date.
start = pendulum.create(2000,1,1)
end = pendulum.now()


for filename in os.listdir(data_directory):
    if filename.endswith(".csv"): 
		path = os.path.join(data_directory, filename)
		reader = csv.DictReader(open(path))
		site_data = []
		for row in reader:
			site_data.append(row)
		if pendulum.parse(site_data[0]['dt']) > start:
			start = pendulum.parse(site_data[0]['dt'])
		if pendulum.parse(site_data[-1]['dt']) < end:
			end = pendulum.parse(site_data[-1]['dt'])
		site_name = filename.split('.csv')[0]
		print site_name
		sites[site_name] = site_data
    else:
        continue

# Remove dates before official start date. 

for site in sites:
	to_remove = []
	for idx, dp in enumerate(sites[site]):
		if pendulum.parse(dp['dt']) < start or pendulum.parse(dp['dt']) > end:
			to_remove.append(idx)
	sites[site] = [e for e in sites[site] if e not in to_remove]



for site in sites:
	# print site
	print sites[site][-1]




print start
print end


