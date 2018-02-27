#!/usr/bin/env python
# -*- coding: latin-1 -*-

'''
Accéléromètre MMA7455 branché à un Raspberry Pi.
C'est un périphérique I2C, donc on le branche à SCL et SDA, et s'assurer
que l'i2C a été préalablement paramétré sur le Raspbery Pi.
electroniqueamateur.blogspot.com
'''

import smbus
import time
import os
import math
import RPi.GPIO as GPIO

# Valeurs à ajouter à chaque mesure pour calibrer votre MMA7455
# Ajustez ces valeurs pour que ça donne x = 0, y = 0 et z = 63 quand
# l'accéléromètre est immobile, à plat sur une table.

ajustx = 0;   # car j'obtenais -10 à la place de 0
ajusty = 0;   # car j'obtenais -19 à la place de 0
ajustz = 0;   # car j'obtenais 69 à la place de 63
 
# Définition d'une classe associée au capteur
class MMA7455():
    bus = smbus.SMBus(1)
    def __init__(self):
	# Réglage de de la définition. Le 3e parametre est 0x05 pour mesurer de -2g a +2g, 0x09 de -4g a +4g, 0x01 de -8g a +8g
        self.bus.write_byte_data(0x1D, 0x16, 0x05) 
    # lecture des valeurs en x, y et z.
    def getValueX(self):
        return self.bus.read_byte_data(0x1D, 0x06) + ajustx
    def getValueY(self):
        return self.bus.read_byte_data(0x1D, 0x07) + ajusty
    def getValueZ(self):
        return self.bus.read_byte_data(0x1D, 0x08) + ajustz

mma = MMA7455()

# on répète la mesure indefiniment
while True: 
	for a in range(1):
 		x = mma.getValueX()
		if (x > 127):         # les valeurs se trouvent entre 0 et 255, 
 			x = x - 255       # alors qu'on les veut entre -127 et 127
    		y = mma.getValueY()
 		if (y > 127):
   	        	y = y - 255 
  	        z = mma.getValueZ()
		if (z > 127):
            		z = z - 255 

		# valeur totale de l'accélération, peu importe l'orientation
		total = math.sqrt(x*x+y*y+z*z); 

		# calcul des angles et conversion en degrés
		angleX = round(math.asin(x/ total )*180.0/3.1416)
		angleY = round(math.asin(y/ total )*180.0/3.1416)
		angleZ = round(math.acos(z/ total )*180.0/3.1416)

		total = round (total)
   
		print '{0} {1} {2}'.format(x,y,z)
		print '----------------------'
		string = '{0} {1} {2}\n'.format(x,y,z) 
		# (ligne précédente à modifier un peu si vous êtes en python 3)
		monfichier = open("data", "w")
		monfichier.write(string)
		monfichier.close()
		time.sleep(0.5)

