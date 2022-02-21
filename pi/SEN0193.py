import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

import RPi.GPIO as GPIO
from time import sleep
from LED_indicator import indicator_diode
from configparser import ConfigParser

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)


class Sensor:
	def __init__(self, channel, min_value = 2000, max_value = 5000, treshold = 30):
		self.chan = AnalogIn(mcp, channel)
		self.channel = channel
		self.min_value = min_value
		self.max_value = max_value
		self.treshold = treshold

		#HARDWARE related
		#power pin based on used channel
		channel_to_power_pin = {
						0: 21,
						1: 20,
						2: 16,
						3: 12,
						4: 23,
						5: 18,
						6: 13,
						7: 14
								}

		self.power_pin = channel_to_power_pin[self.channel]

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.power_pin, GPIO.OUT)

	def __power_on(self):
		GPIO.output(self.power_pin, GPIO.HIGH)	#powering sensor

		GPIO.setup(22, GPIO.OUT)		#powering ADC
		GPIO.output(22, GPIO.HIGH)

	def __power_off(self):
		GPIO.output(self.power_pin, GPIO.LOW)	#disabling sensor
		GPIO.cleanup(22)			#disabling ADC

	def current_value(self, value_type = "%", power_mgmt = True, LED = True):
		if power_mgmt: self.__power_on()

		sleep(0.5)	#making sure that the value read will be correct

		if value_type == "%":
			value = int(100 - ((self.chan.value - self.min_value) * 100) / (self.max_value - self.min_value))

			#clamping read value
			if value < 0:
				value = 0
			elif value > 100:
				value = 100

		elif value_type == "raw":
			value = self.chan.value

		elif value_type == "voltage":
			value = self.chan.voltage

		else:
			print("Nieznany typ danych. Dostępne:\n	%\n	raw\n	voltage")
			if power_mgmt: self.__power_off()
			return -1

		if power_mgmt: self.__power_off()

		if LED: indicator_diode.blink(2, 0.1)

		return value

	def value_test(self, test_value_type):

		if test_value_type not in ["%", "raw", "voltage"]:
			print("Nieznany typ danych. Dostępne:\n	%\n	raw\n	voltage")
			return

		try:
			self.__power_on()

			while True:
				print(self.current_value(value_type = test_value_type, power_mgmt = False, LED = False))
				sleep(1)

		except KeyboardInterrupt:
			self.__power_off()

			print()
			return

	def treshold_test(self):

		try:
			self.__power_on()

			indicated = False	#console note and led indicator

			while True:

				if self.current_value(power_mgmt = False, LED = False) <= self.treshold:
					if not indicated:
						print("Pompa włączona")
						indicator_diode.on()

						indicated = True

				else:
					if indicated:
						print("Pompa wyłączona")
						indicator_diode.off()

						indicated = False

		except KeyboardInterrupt:
			self.__power_off()

			if indicated:	#disabling diode if left turned on
				indicator_diode.off()

			print()
			return


#object based on SEN0193_config.ini data
config = ConfigParser()
config.read("SEN0193_config.ini")

SEN0193_sensors = []

for port in config.sections():
	section = config[port]
	SEN0193_sensors.append(Sensor(int(section["channel"]), int(section["min_value"]), int(section["max_value"]), int(section["treshold"])))
