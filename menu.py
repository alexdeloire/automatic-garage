import smbus
import time
import buttonscroll
import buttonconfirm
import senddweet

bus = smbus.SMBus(1) 

DISPLAY_RGB_ADDR = 0x62

def textCmd(cmd):
    #Cette fonction envoit une commande a l'ecran
    #Utile pour changer de ligne, clear...
    bus.write_byte_data(0x3e,0x80,cmd)

def init_text():
    #Cette fonction initialise l'ecran
    #Il mets aussi la couleur blanche
    textCmd(0x01)
    time.sleep(0.1)
    textCmd(0x0F)
    time.sleep(0.1)
    textCmd(0x38)
    time.sleep(0.1)
    bus.write_byte_data(DISPLAY_RGB_ADDR,0x00,0x00)
    time.sleep(0.1)
    bus.write_byte_data(DISPLAY_RGB_ADDR,0x01,0x00)
    time.sleep(0.1)
    bus.write_byte_data(DISPLAY_RGB_ADDR,0x02,255) #Bleu
    time.sleep(0.1)
    bus.write_byte_data(DISPLAY_RGB_ADDR,0x03,255) #Vert
    time.sleep(0.1)
    bus.write_byte_data(DISPLAY_RGB_ADDR,0x04,255) #Rouge
    time.sleep(0.1)
    bus.write_byte_data(DISPLAY_RGB_ADDR,0x08,0xAA)
    time.sleep(0.1)


def setText(texte):
    #Cette focntion ecrit du texte a l'ecran
    for c in texte:
        bus.write_byte_data(0x3e,0x40,ord(c))
        time.sleep(0.05)


def menu(radar,est_voiture,liste_hist):
    
    clear_status = False #Si l'utilisateur choisi d'effacer l'historique
    time.sleep(0.1)
    textCmd(0x01) #Clear Screen
    time.sleep(0.1)
    setText("Welcome!") #Page d'accueil
    time.sleep(0.1)
    textCmd(0xc0)
    time.sleep(0.1)
    setText("Press fr options")
    time.sleep(0.1)

    while True:
        time.sleep(0.1)
        button_scroll = buttonscroll.lire_button() 
        if button_scroll==1: #Scroll
            break
    
    time.sleep(0.1)
    textCmd(0x01) #Clear Screen
    time.sleep(0.1)

    if radar: #Le radar est activé actuellement
        setText("Deactivate Radar")
        time.sleep(0.1)
        textCmd(0xc0)
        time.sleep(0.1)
        setText("Press to confirm")
        time.sleep(0.1)
        
        while True:
            button_confirm = buttonconfirm.lire_button()
            time.sleep(0.1)
            button_scroll = buttonscroll.lire_button()
            time.sleep(0.1)
            
            if button_confirm==1: #Confirm to change radar
                textCmd(0x01)
                time.sleep(0.1)
                setText("Radar OFF")
                time.sleep(3)
                textCmd(0x01)
                time.sleep(0.1)
                return False,clear_status #Modify radar

            if button_scroll==1: #Scroll
                break

    else: #Le radar est déactivé actuellement
        setText("Activate Radar")
        time.sleep(0.1)
        textCmd(0xc0)
        time.sleep(0.1)
        setText("Press to confirm")
        time.sleep(0.1)
        
        while True:
            button_confirm = buttonconfirm.lire_button()
            time.sleep(0.1)
            button_scroll = buttonscroll.lire_button()
            time.sleep(0.1)
            
            if button_confirm==1: #Confirm to change radar
                textCmd(0x01)
                time.sleep(0.1)
                setText("Radar ON")
                time.sleep(3)
                textCmd(0x01)
                time.sleep(0.1)
                return True,clear_status #Modify radar
            
            if button_scroll==1: #Scroll
                break
    
    time.sleep(0.1) #Changement page, page qui permet d'envoyer l'historique
    textCmd(0x01)
    time.sleep(0.1)
    setText("Send data")
    time.sleep(0.1)
    textCmd(0xc0)
    time.sleep(0.1)
    setText("Press to confirm")
    time.sleep(0.1)
    
    while True:
            button1 = buttonconfirm.lire_button()
            time.sleep(0.1)
            button2 = buttonscroll.lire_button()
            time.sleep(0.1)
            
            if button1==1: #Send Data
                if est_voiture: #Send data avec le fait que la personne vient de se garer
                    senddweet.ajout_historique(liste_hist) #Ajoute la présence de la personne
                    time.sleep(0.1)
                    textCmd(0x01)
                    time.sleep(0.1)
                    setText("Data Sent!")
                    time.sleep(0.1)
                    senddweet.sendhist()
                    time.sleep(3)
                    textCmd(0x01) #Clear Screen
                    time.sleep(0.1)
                    return radar,clear_status
                else: #Send data sauf il n'y a personne dans le garage
                    textCmd(0x01)
                    time.sleep(0.1)
                    setText("Data Sent!")
                    time.sleep(0.1)
                    senddweet.sendhist()
                    time.sleep(3)
                    time.sleep(0.1)
                    textCmd(0x01) #Clear Screen
                    time.sleep(0.1)
                    return radar,clear_status
            
            if button2==1: #Scroll
                break
            
    time.sleep(0.1) #Changement page, page pour regarder la derniere voiture garée avant soi
    textCmd(0x01)
    time.sleep(0.1)
    setText("Last Parked?")
    time.sleep(0.1)
    textCmd(0xc0)
    time.sleep(0.1)
    setText("Press to confirm")
    time.sleep(0.1)
    
    while True:
            button1 = buttonconfirm.lire_button()
            time.sleep(0.1)
            button2 = buttonscroll.lire_button()
            time.sleep(0.1)
            
            if button1==1: 
                #Récuperer la plaque de la dernière voiture garée avant soi
                textCmd(0x01)
                time.sleep(0.1)
                setText("La Plaque Est:")
                time.sleep(0.1)
                textCmd(0xc0)
                time.sleep(0.1)
                plaque_aff=senddweet.get_plaque()
                setText(plaque_aff)
                time.sleep(4)
                textCmd(0x01) #Clear Screen
                time.sleep(0.1)
                return radar,clear_status
            
            if button2==1: #Scroll
                break

    time.sleep(0.1) #Changement page, page qui permet d'effacer l'historique
    textCmd(0x01)
    time.sleep(0.1)
    setText("Clear Data")
    time.sleep(0.1)
    textCmd(0xc0)
    time.sleep(0.1)
    setText("Press to confirm")
    time.sleep(0.1)

    while True:
            button1 = buttonconfirm.lire_button()
            time.sleep(0.1)
            button2 = buttonscroll.lire_button()
            time.sleep(0.1)
            
            if button1==1: 
                #Effacer l'historique
                textCmd(0x01)
                time.sleep(0.1)
                setText("Data Cleared!")
                time.sleep(0.1)
                senddweet.clear_hist()
                time.sleep(3)
                clear_status = True
                time.sleep(0.1)
                textCmd(0x01) #Clear Screen
                time.sleep(0.1)
                return radar,clear_status
            
            if button2==1: #Scroll
                break


    time.sleep(0.1) #Changement page, page qui indique la fin du menu
    textCmd(0x01)
    time.sleep(0.1)
    setText("End of Menu")
    time.sleep(0.1)
    textCmd(0xc0)
    time.sleep(0.1)
    setText("Press to restart") #Il suffit de rappuyer pour relancer le menu
    time.sleep(0.1)
    
    return radar,clear_status

#Tests
"""
time.sleep(0.5)
init_text()
time.sleep(0.5)
menu(True)
time.sleep(0.1)
print("Fin")
"""











