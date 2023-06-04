import time
import grovepi

# Connect the Grove Button to digital port D7
# SIG,NC,VCC,GND
button = 7
grovepi.pinMode(button,"INPUT")



def lire_button():
    #Cette fonction permet de savoir si le bouton est appuyé
    try:
        return grovepi.digitalRead(button)
    except IOError:
        print ("Error")
        return None
