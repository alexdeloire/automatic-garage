import time
import grovepi
# Connect the Grove Light Sensor to analog port A0
# SIG,NC,VCC,GND
light_sensor = 0


grovepi.pinMode(light_sensor,"INPUT")
 



def vallumiere():
    #Cette fonction permet de recuperer la valeur de la luminosite
    try:
        # Get sensor value
        sensor_value = grovepi.analogRead(light_sensor)
        #volt = (1023 - sensor_value) * 10 / sensor_value #Ceci est la valeur en volt
        print("Luminosité ->",sensor_value)
        time.sleep(0.5)
        return sensor_value
 
    except IOError:
        print ("Error")

        
#Test capteur
"""
while True:
    try:
        # Get sensor value
        sensor_value = grovepi.analogRead(light_sensor)
        #volt = (1023 - sensor_value) * 10 / sensor_value #ceci est la valeur en volt
        print(sensor_value)
        time.sleep(0.5)
 
    except IOError:
        print ("Error")"""
