import RPi.GPIO as GPIO
from time import sleep
from termcolor import colored
import json

class Pump:
	def __init__(self):
		self.__active_hardware = None

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(27, GPIO.OUT)

	#returning hardware state, updating active_hardware variable
	def __active_state_read(self):
		with open("/var/www/html/Do_Not_Touch/Active_hardware.json") as json_file:
			self.__active_hardware = json.load(json_file)

		return self.__active_hardware["Pump"]

	#updating hardware states file
	def __active_state_save(self, state):
		#another update of active_hardware can be placed here

		self.__active_hardware["Pump"] = state

		with open("/var/www/html/Do_Not_Touch/Active_hardware.json", "w") as json_file:
			json.dump(self.__active_hardware, json_file)

	def on(self):
		if not self.__active_state_read():
			self.__active_state_save(True)

			GPIO.output(27, GPIO.HIGH)

		else:
			print("Błąd metody 'on()' klasy 'Pump'. Pompa na pinie 27 jest już włączona")

	def off(self):
		if self.__active_state_read():
			GPIO.output(27, GPIO.LOW)

			self.__active_state_save(False)
		else:
			print("Błąd metody 'off()' klasy 'Pump'. Pompa na pinie 27 jest już wyłączona")

	def pump(self, time):
		if not self.__active_state_read():
			self.__active_state_save(True)

			GPIO.output(27, GPIO.HIGH)
			sleep(time)
			GPIO.output(27, GPIO.LOW)

			self.__active_state_save(False)
		else:
			print("Błąd metody 'pump()' klasy 'Pump'. Pompa na pinie 27 jest już włączona")

#
water_pump = Pump()
