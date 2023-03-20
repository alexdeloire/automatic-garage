import time
import grovepi
 
# Connect the Grove Buzzer to digital port D8
# SIG,NC,VCC,GND
buzzer = 8
grovepi.pinMode(buzzer,"OUTPUT")

# set I2C to use the hardware bus
grovepi.set_bus("RPI_1")


def allumer_buzzer():
    #Cette fonction allume le buzzer
    try: 
        grovepi.digitalWrite(buzzer,1)
        print ('start')
    except KeyboardInterrupt:
        grovepi.digitalWrite(buzzer,0)
    except IOError:
        print ("Error")

def fermer_buzzer():
    #Cette fonction eteint le buzzer
    try: 
        grovepi.digitalWrite(buzzer,0)
        print ('stop')
    except KeyboardInterrupt:
        grovepi.digitalWrite(buzzer,0)
    except IOError:
        print ("Error")
    


