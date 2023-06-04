import time
import grovepi

# set I2C to use the hardware bus
grovepi.set_bus("RPI_1")

# Connect the Grove Ultrasonic Ranger to digital port D3
# SIG,NC,VCC,GND
ultrasonic_ranger = 3



def lire_ultrason():
    #Cette fonction permet de recuperer la distance lu par le capteur
    try:
        # Read distance value from Ultrasonic
        return grovepi.ultrasonicRead(ultrasonic_ranger)

    except Exception as e:
        print ("Error:{}".format(e))
        return None



#Test capteur
"""
while True:        
    try:
        # Read distance value from Ultrasonic
        print(grovepi.ultrasonicRead(ultrasonic_ranger))
        time.sleep(0.2)

    except Exception as e:
        print ("Error:{}".format(e))
        """
