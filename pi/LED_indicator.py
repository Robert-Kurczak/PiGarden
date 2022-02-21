import RPi.GPIO as GPIO
from time import sleep
from termcolor import colored
import json

class LED:
	def __init__(self, pin, color):
		self.pin = pin
		self.color = color

		self.__active_hardware = None

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(pin, GPIO.OUT)

	#returning hardware state, updating active_hardware variable
	def __active_state_read(self):
		with open("/var/www/html/Do_Not_Touch/Active_hardware.json") as json_file:
			self.__active_hardware = json.load(json_file)

		return self.__active_hardware["LED_indicator"]

	#saving updating hardware states file
	def __active_state_save(self, state):
		#another update of actibe_hardware can be placed here

		self.__active_hardware["LED_indicator"] = state

		with open("/var/www/html/Do_Not_Touch/Active_hardware.json", "w") as json_file:
			json.dump(self.__active_hardware, json_file)

	def on(self):
		if not self.__active_state_read():
			self.__active_state_save(True)

			GPIO.output(self.pin, GPIO.HIGH)

		else:
			print(colored("Błąd metody 'on()' klasy 'LED'. Dioda na pinie {} jest już włączona".format(self.pin), self.color))

	def off(self):
		if self.__active_state_read():
			GPIO.output(self.pin, GPIO.LOW)

			self.__active_state_save(False)

		else:
			print(colored("Błąd metody 'off()' klasy 'LED'. Dioda na pinie {} jest już wyłączona".format(self.pin), self.color))


	def blink(self, times, delay):
		if not self.__active_state_read():
			self.__active_state_save(True)

			for i in range(times):

				try:
					GPIO.output(self.pin, GPIO.HIGH)
					sleep(delay)
					GPIO.output(self.pin, GPIO.LOW)
					sleep(delay)

				except KeyboardInterrupt:
					self.__active_state_save(False)

					print()
					exit()

			self.__active_state_save(False)

		else:
			print(colored("Błąd metody 'blink() klasy 'LED'. Dioda na pinie {} jest już włączona".format(self.pin), self.color))


#
indicator_diode = LED(24, "cyan")
