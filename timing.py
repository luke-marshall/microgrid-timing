import datetime as dt
import random
import pprint
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import column
from bokeh.palettes import Spectral6


def getDay5mSolarData():
	times = ['6:30AM', '6:35AM','6:40AM','6:45AM','6:50AM','6:55AM','7:00AM','7:05AM','7:10AM','7:15AM','7:20AM','7:25AM','7:30AM','7:35AM','7:40AM','7:45AM','7:50AM','7:55AM','8:00AM','8:05AM','8:10AM','8:15AM','8:20AM','8:25AM','8:30AM','8:35AM','8:40AM','8:45AM','8:50AM','8:55AM','9:00AM','9:05AM','9:10AM','9:15AM','9:20AM','9:25AM','9:30AM','9:35AM','9:40AM','9:45AM','9:50AM','9:55AM','10:00AM','10:05AM','10:10AM','10:15AM','10:20AM','10:25AM','10:30AM','10:35AM','10:40AM','10:45AM','10:50AM','10:55AM','11:00AM','11:05AM','11:10AM','11:15AM','11:20AM','11:25AM','11:30AM','11:35AM','11:40AM','11:45AM','11:50AM','11:55AM','12:00PM','12:05PM','12:10PM','12:15PM','12:20PM','12:25PM','12:30PM','12:35PM','12:40PM','12:45PM','12:50PM','12:55PM','1:00PM','1:05PM','1:10PM','1:15PM','1:20PM','1:25PM','1:30PM','1:35PM','1:40PM','1:45PM','1:50PM','1:55PM','2:00PM','2:05PM','2:10PM','2:15PM','2:20PM','2:25PM','2:30PM','2:35PM','2:40PM','2:45PM','2:50PM','2:55PM','3:00PM','3:05PM','3:10PM','3:15PM','3:20PM','3:25PM','3:30PM','3:35PM','3:40PM','3:45PM','3:50PM','3:55PM','4:00PM','4:05PM','4:10PM','4:15PM','4:20PM','4:25PM','4:30PM','4:35PM','4:40PM','4:45PM','4:50PM','4:55PM','5:00PM','5:05PM','5:10PM','5:15PM','5:20PM','5:25PM','5:30PM','7:20PM','7:25PM','7:30PM']
	energyOut =  [0.001, 0.001,0.003,0.004,0.008,0.012,0.016,0.030,0.044,0.058,0.085,0.111,0.138,0.177,0.216,0.255,0.310,0.366,0.421,0.495,0.568,0.642,0.736,0.830,0.923,1.038,1.153,1.267,1.400,1.534,1.667,1.817,1.967,2.117,2.282,2.448,2.613,2.792,2.972,3.151,3.344,3.538,3.731,3.938,4.145,4.351,4.568,4.785,5.002,5.227,5.452,5.677,5.910,6.143,6.376,6.616,6.855,7.095,7.339,7.583,7.828,8.077,8.327,8.576,8.828,9.081,9.333,9.586,9.840,10.093,10.348,10.602,10.856,11.111,11.365,11.620,11.873,12.126,12.379,12.630,12.882,13.133,13.383,13.633,13.884,14.130,14.376,14.622,14.861,15.101,15.340,15.572,15.804,16.036,16.260,16.484,16.708,16.921,17.135,17.349,17.552,17.754,17.957,18.147,18.337,18.528,18.703,18.878,19.053,19.209,19.365,19.521,19.656,19.791,19.926,20.039,20.152,20.265,20.336,20.407,20.478,20.505,20.531,20.558,20.565,20.573,20.580,20.582,20.583,20.584,20.584,20.584,20.584,20.584,20.584,20.584]
	if len(times) != len(energyOut):
		raise ValueError("Length of two arrays doesn't match.")
	data = {}
	lastEnergy = 0
	for idx, time in enumerate(times):
		if len(time.split(':')[0]) == 1: #needs to be zero-padded for strptime.
			time = '0'+time
		data[dt.datetime.strptime(time, "%I:%M%p")] = {'5m_generation': (energyOut[idx] - lastEnergy) * (0.5 + random.random()/2.0)} #Add some random variation
		lastEnergy = energyOut[idx]
	return data

def getDay5mLoadData():
	times = ['6:30AM', '6:35AM','6:40AM','6:45AM','6:50AM','6:55AM','7:00AM','7:05AM','7:10AM','7:15AM','7:20AM','7:25AM','7:30AM','7:35AM','7:40AM','7:45AM','7:50AM','7:55AM','8:00AM','8:05AM','8:10AM','8:15AM','8:20AM','8:25AM','8:30AM','8:35AM','8:40AM','8:45AM','8:50AM','8:55AM','9:00AM','9:05AM','9:10AM','9:15AM','9:20AM','9:25AM','9:30AM','9:35AM','9:40AM','9:45AM','9:50AM','9:55AM','10:00AM','10:05AM','10:10AM','10:15AM','10:20AM','10:25AM','10:30AM','10:35AM','10:40AM','10:45AM','10:50AM','10:55AM','11:00AM','11:05AM','11:10AM','11:15AM','11:20AM','11:25AM','11:30AM','11:35AM','11:40AM','11:45AM','11:50AM','11:55AM','12:00PM','12:05PM','12:10PM','12:15PM','12:20PM','12:25PM','12:30PM','12:35PM','12:40PM','12:45PM','12:50PM','12:55PM','1:00PM','1:05PM','1:10PM','1:15PM','1:20PM','1:25PM','1:30PM','1:35PM','1:40PM','1:45PM','1:50PM','1:55PM','2:00PM','2:05PM','2:10PM','2:15PM','2:20PM','2:25PM','2:30PM','2:35PM','2:40PM','2:45PM','2:50PM','2:55PM','3:00PM','3:05PM','3:10PM','3:15PM','3:20PM','3:25PM','3:30PM','3:35PM','3:40PM','3:45PM','3:50PM','3:55PM','4:00PM','4:05PM','4:10PM','4:15PM','4:20PM','4:25PM','4:30PM','4:35PM','4:40PM','4:45PM','4:50PM','4:55PM','5:00PM','5:05PM','5:10PM','5:15PM','5:20PM','5:25PM','5:30PM','7:20PM','7:25PM','7:30PM']
	data = {}
	for idx, time in enumerate(times):
		data[dt.datetime.strptime(time, "%I:%M%p")] = {'5m_load':random.random() * (20.0 / 300.0)}
	return data

def calculate5m(solar_systems, load_systems, times):
	for time in times:
		# Find total generation
		generation = 0
		for system in list(solar_systems):
			generation += solar_systems[system][time]['5m_generation']

		# Find total load
		load = 0
		for system in list(load_systems):
			load += load_systems[system][time]['5m_load']
		
		# Calculate demand on network from loads
		networkDemand = load - generation if load > generation else 0

		# Allocation rule:
		# 1. Calculate amount of solar each participant is entitled to get if split equally.
		n_users = len(list(load_systems))
		# 2. Build a list of load users sorted smallest to largest (list of tuples feat. key and value)
		sorted_loads = []
		for system in load_systems: #create the list of tuples
			sorted_loads.append((system, load_systems[system][time]['5m_load']))
		sorted_loads = sorted(sorted_loads, key=lambda x : x[1]) #sort the list
		# 3. Starting from smallest load user, allocate solar. Record when there is a shortfall, add surplus to kitty and recalculate total solar per participant with n-1 paricipants.
		for system in sorted_loads:
			system = system[0]
			available_energy = generation / n_users
			if available_energy < load_systems[system][time]['5m_load']: #shortfall
				load_systems[system][time]['5m_network_impact'] = load_systems[system][time]['5m_load'] - available_energy
				generation -= available_energy
			else:
				load_systems[system][time]['5m_network_impact'] = 0
				generation -= available_energy - load_systems[system][time]['5m_load'] 
			n_users -= 1
		
		export = generation #export is whatever remains after allocated to all users. 

	return load_systems

# Calculates available solar and network impact based on longer timeperiod metering. 
def calculateTimePeriodMultiple(solar_systems, load_systems, times, multiple):
	# Find timeperiod label
	label = str(int(round(5 * multiple)))+'m_'
	
	# 1. Record cumulative load or generation in the respective dict. 
	gen_temp = {}
	load_temp = {}
	for idx, time in enumerate(times):
		
		# Add this 5 minutes' generation to the larger timeperiod's temporary record.
		for system in list(solar_systems):
			# Make sure the right object exists in the temp dict. 
			gen_temp[system] = 0 if not system in gen_temp else gen_temp[system]
			# Add to the record.
			gen_temp[system] += solar_systems[system][time]['5m_generation']
		
		# Add this 5 minutes' load to the larger timeperiod's temporary record.
		for system in list(load_systems):
			# Make sure the right object exists in the temp dict. 
			load_temp[system] = 0 if not system in load_temp else load_temp[system]
			# Add to the record.	
			load_temp[system] += load_systems[system][time]['5m_load']
		
		# If it is the multiple-th time, record in the load or gen system
		if idx % multiple == 0:
			for system in list(load_systems):
				load_systems[system][time][label+'load'] = load_temp[system]
			for system in list(solar_systems):
				solar_systems[system][time][label+'generation'] = gen_temp[system]
			gen_temp = {}
			load_temp = {}
	
	# 2. Perform allocation rule. 
	for idx, time in enumerate(times):
		if idx % multiple == 0:
			# Find total generation
			generation = 0
			for system in list(solar_systems):
				generation += solar_systems[system][time][label+'generation']

			# Find total load
			load = 0
			for system in list(load_systems):
				load += load_systems[system][time][label+'load']
			
			# Calculate demand on network from loads
			networkDemand = load - generation if load > generation else 0

			# Allocation rule:
			# 1. Calculate amount of solar each participant is entitled to get if split equally.
			n_users = len(list(load_systems))
			# 2. Build a list of load users sorted smallest to largest (list of tuples feat. key and value)
			sorted_loads = []
			for system in load_systems: #create the list of tuples
				sorted_loads.append((system, load_systems[system][time][label+'load']))
			sorted_loads = sorted(sorted_loads, key=lambda x : x[1]) #sort the list
			# 3. Starting from smallest load user, allocate solar. Record when there is a shortfall, add surplus to kitty and recalculate total solar per participant with n-1 paricipants.
			for system in sorted_loads:
				system = system[0]
				available_energy = generation / n_users
				if available_energy < load_systems[system][time][label+'load']: #shortfall
					load_systems[system][time][label+'network_impact'] = load_systems[system][time][label+'load'] - available_energy
					generation -= available_energy
				else:
					load_systems[system][time][label+'network_impact'] = 0
					generation -= available_energy - load_systems[system][time][label+'load'] 
				n_users -= 1
			
			export = generation #export is whatever remains after allocated to all users. 
	return load_systems
	



solar_systems = {
	'pv_1': getDay5mSolarData(),
	'pv_2': getDay5mSolarData(),
	'pv_3': getDay5mSolarData(),
	'pv_4': getDay5mSolarData(),
	'pv_5': getDay5mSolarData(),
	'pv_6': getDay5mSolarData(),
}

load_systems = {
	'load_1': getDay5mLoadData(),
	'load_2': getDay5mLoadData(),
	'load_3': getDay5mLoadData(),
	'load_4': getDay5mLoadData(),
	'load_5': getDay5mLoadData(),
	'load_6': getDay5mLoadData(),
	'load_7': getDay5mLoadData(),
	'load_8': getDay5mLoadData(),
	'load_9': getDay5mLoadData(),
}
times = sorted(list(getDay5mLoadData()))

load_systems = calculate5m(solar_systems, load_systems, sorted(list(getDay5mLoadData())))
load_systems = calculateTimePeriodMultiple( solar_systems, load_systems, times, 2 )
load_systems = calculateTimePeriodMultiple( solar_systems, load_systems, times, 3 )
load_systems = calculateTimePeriodMultiple( solar_systems, load_systems, times, 4 )
load_systems = calculateTimePeriodMultiple( solar_systems, load_systems, times, 5 )
load_systems = calculateTimePeriodMultiple( solar_systems, load_systems, times, 6 )
load_systems = calculateTimePeriodMultiple( solar_systems, load_systems, times, 7 )
load_systems = calculateTimePeriodMultiple( solar_systems, load_systems, times, 8 )
load_systems = calculateTimePeriodMultiple( solar_systems, load_systems, times, 9 )
pprint.pprint(load_systems)

results = {}
for system in list(load_systems):
	results[system] = {'5m_network_impact':0,'10m_network_impact':0,'15m_network_impact':0,'20m_network_impact':0,'25m_network_impact':0,'30m_network_impact':0,'35m_network_impact':0, '40m_network_impact':0, '45m_network_impact':0}
	for time in times:
		for tp_label in list(results[system]):
			if tp_label in load_systems[system][time]:
				results[system][tp_label] += load_systems[system][time][tp_label]
pprint.pprint(results)

output_file('vbar.html')

# Print the vbar results too.
all_time_labels = ['5m_network_impact','10m_network_impact','15m_network_impact','20m_network_impact','25m_network_impact','30m_network_impact','35m_network_impact', '40m_network_impact', '45m_network_impact']

plots = []
for label in all_time_labels:
	print "\n\n"+label
	total = 0
	for load in results:
		print load+ ": "+str(results[load][label])
		total +=results[load][label]
	print "Total: "+str(total)


# Bar charts of deviation results
labels = ['10m_network_impact','15m_network_impact','20m_network_impact','25m_network_impact','30m_network_impact','35m_network_impact', '40m_network_impact', '45m_network_impact']
for idx, system in enumerate(list(results)):
	# Load line chart
	p = figure(plot_width=800, plot_height=400, title="Load trend (kWh): "+system)
	data = []
	for time in times:
		data.append(load_systems[system][time]['5m_load'])
	p.line(range(len(data)), data, line_width=2, color=Spectral6[idx % 6])
	plots.append(p)
	
	# deviation
	p1 = figure(plot_width=800, plot_height=400, title="Absolute % deviation from 5-min time period measurement (kWh) vs time period: "+system)
	data = []
	for label in labels:
		data.append(abs( 100* (results[system][label]  - results[system]['5m_network_impact'] )/ results[system]['5m_network_impact'] ))
	p1.vbar(x=[ 10, 15, 20, 25, 30,35,40,45], width=0.5, bottom=0,
		top=data, color=Spectral6[idx % 6])
	plots.append(p1)

	

# p = column(plots)
# show(p)