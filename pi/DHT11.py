import time
import board
import dht11
import RPi.GPIO as GPIO
from LED_indicator import indicator_diode
from time import sleep

class Sensor:
	def __init__(self):
		self.dht = dht11.DHT11(19)

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(26, GPIO.OUT)

	def __power_on(self):
		GPIO.output(26, GPIO.HIGH)

	def __power_off(self):
		GPIO.output(26, GPIO.LOW)

	def current_values(self, power_mgmt = True, LED = True):
		if power_mgmt: self.__power_on()

		reads = self.dht.read()

		MAX_TRIES = 50
		#eliminating measure errors (temperature and humidity showing as 0)
		while reads.temperature == reads.humidity == 0 and MAX_TRIES > 0:
			reads = self.dht.read()
			MAX_TRIES -= 1
		#

		if power_mgmt: self.__power_off()

		if LED: indicator_diode.blink(3, 0.1)

		return [reads.temperature, reads.humidity]

	def values_test(self):

		try:
			self.__power_on()

			while True:
				reads = self.current_values(power_mgmt = False, LED = False)

				print("Temperatura: {}°C | Wilgotność: {}% RH".format(reads[0], reads[1]))
				sleep(1)

		except KeyboardInterrupt:
			self.__power_off()

			print()
			return


#
DHT11_sensor = Sensor()
