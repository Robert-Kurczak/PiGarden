# PiGarden
Smart garden that helps to grow plants by automatically watering them (based on moisutre of soil) and illuminating them with special light that accelerates growth. It also tracks environmental parameters such as air humidity or ambient temperature.

Users can manually controll all those functions using simple interface to which they can connect via wifi.

## Table of Contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Hardware](#hardware)

## General info
This project is based on Raspberry Pi 3B. I designed and built expansion board so my raspberry can easily controll LED strips, water pump and communicate with sensors, which are:
* SEN0193 - capacitive soil moisture sensors
* DHT11 - ambient temperature and air humidity sensor

The interface is a local website I built, hosted via apache2. Data from sensors is stored in local database hosted on mariaDB engine.

## Technologies
 1. [DHT11 library](https://github.com/szazo/DHT11_Python)
 2. [Adafruit MCP3008 library](https://learn.adafruit.com/mcp3008-spi-adc/python-circuitpython)
 3. [ChartJS](https://www.chartjs.org/)

## Setup
Everything in "pi" folder needs to be placed in home directory - /home/pi by default

Web page, which is in "html" folder needs to be placed in apache website directory - /var/www/html by default

PiGarden-Database.sql is my database schema dump. Database from this file must be created on MariaDB engine.

## Hardware
### Design
<img src="/Images/Expansion_Board_Schematic.png" alt="Expansion board schematic" width="1000">

### Few pictures
<p>
 <img src="/Images/IMG_1.jpg" alt="Expansion board picture 1" height="250">
 <img src="/Images/IMG_2.jpg" alt="Expansion board picture 2" height="250">
 <img src="/Images/IMG_3.jpg" alt="Expansion board picture 3" height="250">
 <img src="/Images/IMG_4.jpg" alt="Expansion board picture 4" height="250">
 <img src="/Images/IMG_5.jpeg" alt="Expansion board picture 5" height="250">
 <img src="/Images/IMG_6.jpeg" alt="Expansion board picture 6" height="250">
</p>
