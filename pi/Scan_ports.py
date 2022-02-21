from SEN0193 import Sensor
from termcolor import colored

print("Skanowanie najlepiej przeprowadzać gdy sensory nie mają kontaktu z wilgocią.\n")
print("Skanowanie...\n")

found = []	#storing used ports numbers

for i in range(8):
	sensor = Sensor(i)

	if sensor.current_value(value_type = "voltage", LED = False) > 0.5:
		found.append(i)

if len(found) == 0:
	print("Nie znaleziono sensorów na żadnym z dostępnych portów.")
else:
	print("Znaleziono sensor(y) na:")

	for port in found:
		print(colored("	Port " + str(port), "green"))

print()

answer = None

while answer not in ["t", "n"]:
	answer = input("Czy chcesz zapisać obecną konfigurację portów? [t/n]: ").lower()

if answer == "t":
	config_template = ""

	for port in found:
		config_template += "[PORT" + str(port) + "]\n"\
				  "channel: " + str(port) + "\n"\
				  "min_value: 2000\n"\
				  "max_value: 5000\n"\
				  "treshold: 30\n\n"

	with open("SEN0193_config.ini", "w") as config_file:
		config_file.write(config_template)
