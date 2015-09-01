import numpy
import time
import core.manager
m = core.manager.EmotivManager()
#m.monitor_interval = 
m.connect()
m.monitoring = True



#here, we are going to make a module that concatenates some values from the monitor datastream
lastbit = numpy.zeros(1) #this is a formality that lets the while loop not crash
now = time.time()
later = now+5
pool = []
while time.time() < later:
	if lastbit.tolist() != m.sensor_data[:,0].tolist():
		lastbit = m.sensor_data[:,0] #this and the above should be changed to 6 and/or 9 later to get real data.
		pool.extend(lastbit.tolist())
		time.sleep(.065)
print(pool)
m.monitoring = False
#a.extend(b) links a to b. 