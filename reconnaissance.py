import pytesseract
from PIL import Image


def lireplaque(path):
    #Cette fonction lit le texte sur la plaque de la voiture 
    #et l'enregistre dans un fichier plaquetext.txt

    #Lire avec tesseract
    text = pytesseract.image_to_string(Image.open(path))

    text = text.replace(" ","")
    text = text.replace("-","")
    text = text.replace("\n","")
    
    with open("plaquetext.txt","w") as file:
        file.write(text)
    


lireplaque("/home/pi/garage/plaque1.jpg") #Le path de la photo prise par la camera



#Tests
"""
def lireplaque1():
    #Cette fonction lit le texte sur la plaque de la voiture 
    #et l'enregistre dans un fichier plaquetext.txt

    #Lire avec tesseract
    #text = pytesseract.image_to_string(Image.open(path))
    text = "AFG  - TF 67 GY"
    text = text.replace(" ","")
    text = text.replace("-","")
    text = text.replace("\n","")
    
    with open("plaquetext.txt","w") as file:
        file.write(text)

lireplaque1()
"""
