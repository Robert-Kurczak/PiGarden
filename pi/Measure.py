from SEN0193 import SEN0193_sensors
from DHT11 import DHT11_sensor
from LED_indicator import indicator_diode
from Pump import water_pump
import mariadb
from datetime import datetime
import json
from os import popen

def take_measure(auto_wtr=True):
	indicator_diode.blink(2, 0.5)

	#-------------------------------------SEN0193-----------------------------------
	#sensor value with channel it uses: [[value, channel]]
	SEN0193_reads = []

	#check if water is needed
	under_treshold = []

	for sensor in SEN0193_sensors:
		value = sensor.current_value(LED=False)
		SEN0193_reads.append([value, sensor.channel])

		if value <= sensor.treshold:
			under_treshold.append(True)
		else:
			under_treshold.append(False)

	indicator_diode.blink(1, 0.2)
	#-------------------------------------------------------------------------------

	#-------------------------------------DHT11-------------------------------------
	DHT11_reads = DHT11_sensor.current_values(LED=False)
	#-------------------------------------------------------------------------------

	#------------------------------------Pi Data------------------------------------
	#getting CPU temperature
	with open("/sys/class/thermal/thermal_zone0/temp") as temp_file:
		cpu_temp = round(float(temp_file.read())/1000, 2)
	
	#getting system uptime
	with open("/proc/uptime") as uptime_file:
		system_uptime = float(uptime_file.read().split()[0])

	#getting system version
	with open("/etc/os-release") as version_file:
		f = version_file.read()
		system_version = f[13: f.find("\nNAME=") - 1]
	#-------------------------------------------------------------------------------

	indicator_diode.blink(1, 0.25)

	#------------------------------------DATABASE-----------------------------------
	#connecting
	connection = mariadb.connect(
					user = "root",
					password = "PiGarden",
					host = "localhost",
					database = "PiGarden"
										)

	cursor = connection.cursor()

	#----queries----
	add_moisture_query = "INSERT INTO `Soil_Moisture` VALUES (NULL, ?, ?, ?)"
	add_temperature_query = "INSERT INTO `Air_Temperature` VALUES (NULL, ?, ?)"
	add_humidity_query = "INSERT INTO `Air_Humidity` VALUES (NULL, ?, ?)"
	add_pi_data_query = "INSERT INTO `Pi_Data` VALUES (NULL, ?, ?, ?)"
	#---------------
	
	for sensor_reads in SEN0193_reads:
		#timestamp for each of SEN0193 sensors
		current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		#inserting SEN0193`s values
		cursor.execute(add_moisture_query, (sensor_reads[0], sensor_reads[1], current_datetime))

	#timestamp for DHT11
	current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	#inserting DHT11 values
	cursor.execute(add_temperature_query, (DHT11_reads[0], current_datetime))
	cursor.execute(add_humidity_query, (DHT11_reads[1], current_datetime))

	#inserting pi data
	cursor.execute(add_pi_data_query, (cpu_temp, system_uptime, system_version))

	connection.close()
	#-------------------------------------------------------------------------------

	indicator_diode.blink(1, 0.25)

	#-------------------------------------JSON--------------------------------------
	def change_state(state):

		with open("/var/www/html/Do_Not_Touch/Active_software.json") as json_file_r:
			Active_software = json.load(json_file_r)
			Active_software["Measure"] = state

			with open("/var/www/html/Do_Not_Touch/Active_software.json", "w") as json_file_w:
				json.dump(Active_software, json_file_w)
	#-------------------------------------------------------------------------------

	#watering if needed
	if auto_wtr and all(under_treshold):
		water_pump.pump(40)
		change_state("watered")
		print("Ogród został podlany.")
	
	elif not auto_wtr and all(under_treshold):
		change_state("need watering")
		print("Ogród wymaga podlania.")
	
	else:
		change_state("done")
		print("Ogród nie wymaga podlania.")
