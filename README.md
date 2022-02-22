# PiGarden
Smart garden that helps to grow plants by automatically watering them (based on moisutre of soil) and illuminating them with special light that accelerates growth. It also tracks environmental parameters such as air humidity or ambient temperature.

Users can manually controll all those functions using simple interface to which they can connect via wifi.

## Table of Contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Interface](#interface)
* [Setup](#setup)
* [Hardware](#hardware)

## General info
This project is based on Raspberry Pi 3B. I designed and built expansion board so my raspberry can easily controll LED strips, water pump and communicate with sensors, which are:
* SEN0193 - capacitive soil moisture sensors
* DHT11 - ambient temperature and air humidity sensor

The interface is a local website hosted via apache2. Data from sensors is stored in local database hosted on mariaDB engine.

## Interface
<img src="/Images/Interface.png" alt="Interface screenshot" width="1000">

One the left side, you can see:
* value of the last ambient temperature measurement
* value of the last air humidity measurement
* value of soil moisture which is average of most recent measurements from each sensor. You can see the value of individual sensors by pressing small arrow, next to label.

<br>

Below, you can see current Raspberry Pi data, which is:
* CPU temperature
* System uptime
* OS version

<br>

On the right side there are 2 sliders and 1 button. Using sliders, you can manually turn on/off water pump and lights. Button makes system takes measurements of all sensors and update displayed values.

If the soil moisture drops below certain treshold that you can controll in SEN0193_config.ini (30% by default) you will get alert that let you choose to water plant now or ignore it now.

<br>

On the bottom, there are 2 charts where you can keep track of changes in ambient temperature and humidity.

## Technologies
 1. Raspbian buster 10
 2. [DHT11 library](https://github.com/szazo/DHT11_Python)
 3. [Adafruit MCP3008 library](https://learn.adafruit.com/mcp3008-spi-adc/python-circuitpython)
 4. [ChartJS](https://www.chartjs.org/)

## Setup
Everything in "pi" folder needs to be placed in home directory - /home/pi by default

Web page, which is in "html" folder needs to be placed in apache website directory - /var/www/html by default

PiGarden-Database.sql is my database schema dump. Database from this file must be created on MariaDB engine.

In SEN0193_config.ini you can configure soil moisture sensors. The options are:
* channel - header to which sensor is connected
* min_value - value that sensor reads while being in the air
* max_value - value that sensor reads while being in the water
* treshold - value in % below which this sensor will "assume" it's too dry

## Hardware
<img src="/Images/Expansion_Board_PCB.png" alt="Expansion board PCB" width="750">

### Few pictures
<p>
 <img src="/Images/IMG_1.jpg" alt="PiGarden picture 1" height="250">
 <img src="/Images/IMG_2.jpg" alt="PiGarden board picture 2" height="250">
 <img src="/Images/IMG_3.jpg" alt="PiGarden board picture 3" height="250">
 <img src="/Images/IMG_4.jpg" alt="Expansion board front" height="250">
 <img src="/Images/IMG_5.jpg" alt="Expansion board back" height="250">
 <img src="/Images/IMG_6.jpg" alt="Pump" height="250">
</p>
