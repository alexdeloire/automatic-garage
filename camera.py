from picamera import PiCamera
from time import sleep



def photo():
    #Cette focntion prend une photo avec la camera
    camera = PiCamera()
    sleep(2) #Obligatoire
    camera.rotation = 180  #Retourne la camera 
    camera.resolution = (1920, 1080) #Resolution de la camera
    #camera.annotate_text = "Plaque" #Texte si jamais on a besoin
    #camera.annotate_text_size = 160
    camera.capture('/home/pi/garage/plaque.jpg')

