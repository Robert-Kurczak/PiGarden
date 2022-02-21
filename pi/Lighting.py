import RPi.GPIO as GPIO
from time import sleep
from termcolor import colored
import json

class Lighting:
	def __init__(self, pin):
		self.pin = pin

		self.__active_hardware = None

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(17, GPIO.OUT)

	#returning hardware state, updating active_hardware variable
	def __active_state_read(self):
		with open("/var/www/html/Do_Not_Touch/Active_hardware.json") as json_file:
			self.__active_hardware = json.load(json_file)

		return self.__active_hardware["Lighting"]

	#updating hardware states file
	def __active_state_save(self, state):
		#another update of active_hardware can be placed here

		self.__active_hardware["Lighting"] = state

		with open("/var/www/html/Do_Not_Touch/Active_hardware.json", "w") as json_file:
			json.dump(self.__active_hardware, json_file)

	def on(self):
		if not self.__active_state_read():
			self.__active_state_save(True)

			GPIO.output(17, GPIO.HIGH)
		else:
			print(colored("Błąd metody 'on()' klasy 'Lighting'. Oświetlenie na pinie 17 jest już włączone", "yellow"))

	def off(self):
		if self.__active_state_read():
			GPIO.output(17, GPIO.LOW)

			self.__active_state_save(False)
		else:
			print(colored("Błąd metody 'off()' klasy 'Lighting'. Oświetlenie na pinie 17 jest już wyłączone", "yellow"))

#
grow_light = Lighting(2)
