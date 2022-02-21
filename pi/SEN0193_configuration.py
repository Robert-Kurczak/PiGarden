from configparser import ConfigParser
from termcolor import colored

config = ConfigParser()
config.read("SEN0193_config.ini")

avalible_ports = [int(port[4:]) for port in config.sections()]

print("Możliwe do konfiguracji porty: \n")
for port in avalible_ports:
	print(colored("	Port " + str(port), "green"))
print()

port_to_configure = -1

while port_to_configure not in avalible_ports:
	port_to_configure = int(input("Urządzenie na którym porcie chcesz skonfigurować?: "))

	if port_to_configure not in avalible_ports:
		print("Niewłaściwy numer portu.\n")

section = config["PORT" + str(port_to_configure)]
keys = ["channel", "min_value", "max_value", "treshold"]

print("\nAktualna konfiguracja wybranego portu: \n")
for key in keys:
	print(colored(key + ": " + section[key], "cyan"))

print("\nWpisz nazwę klucza a następnie, po dwukropku, wybraną wartość | [klucz: wartość]\n"\
	"Aby wyświetlić aktualną konfigurację, wpisz 'see'.\n"\
	"Aby zapisać zmiany, wpisz 'save'.\n"\
	"Aby wyjść, wpisz 'exit'.\n")

while True:
	user_input = input(colored(">> ", "yellow"))

	if user_input == "save":
		with open("SEN0193_config.ini", "w") as configfile:
			config.write(configfile)
		print("Zmiany zapisano pomyślnie.\n")
		continue

	elif user_input == "see":
		config.read("SEN0193_config.ini")
		for key in keys:
				print(key + ": " + section[key])

		print()

	elif user_input == "exit":
		exit()

	else:

		property = user_input.replace(" ", "")

		break_index = property.find(":")

		choosen_key = property[:break_index]

		try:
			value = int(property[break_index + 1:])

		except ValueError:
			print("\nNiewłaściwa wartość.")
			continue

		if choosen_key not in keys:
			print("\nNiewłaściwy klucz.")

		else:
			config.set("PORT" + str(port_to_configure), choosen_key, str(value))
			print("\nZmianę dodano pomyślnie.")
