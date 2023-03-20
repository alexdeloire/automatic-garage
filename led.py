import time
from grovepi import *
 
# Connect the Grove LED to digital port D4
led = 4
 
pinMode(led,"OUTPUT")
time.sleep(0.1)
 
 

def allumer_led():
    #Cette fonction allume la led
    try:
        digitalWrite(led,1)     # Send HIGH to switch on LED
        #LED ON
        time.sleep(0.5)
 
    except KeyboardInterrupt:   # Turn LED off before stopping
        digitalWrite(led,0)
        
    except IOError:             # Print "Error" if communication error encountered
        print ("Error")


def eteindre_led():
    #Cette focntion eteint la led
    try:
        digitalWrite(led,0)     # Send LOW to switch off LED
        #LED OFF
        time.sleep(0.5)
 
    except KeyboardInterrupt:   # Turn LED off before stopping
        digitalWrite(led,0)

    except IOError:             # Print "Error" if communication error encountered
        print ("Error")
        

