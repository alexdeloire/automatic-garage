import capteur_lumiere_in
import capteur_lumiere_out
import camera
import led
import ultrason
import buzzer
import buttonscroll
import menu
import moteur
import senddweet
import time
import seconds
import os
from datetime import date

liste_plaque=["12345","AA725AD","AB344CA","KL35AR4646","01300145"]  #Liste plaque autorise
threshold = 750  #Valeur de luminosite, si depasse, alors ouvre garage
#AJUSTEE A MON TELEPHONE (LE FLASH)

varbool = True  #Variable pour lancer la boucle générale
est_voiture = False #Au debut, il n'y a pas de voiture
radar = True #On active le radar par defaut
liste_hist=[] #Ce qu'on va envoyer à l'historique
dernier_id=senddweet.get_id() #Dernier ID dans l'historique
dernier_id=dernier_id+1 #On incrémente
time_launch=time.time() #Temps du lancement

menu.init_text() #On initialise l'ecran si jamais on en a besoin

while varbool:
    print("Debut du programme")      
    while (not est_voiture): #Il n'y a pas de voiture dans le garage
        
        #On attend le declenchement des phares

        luminosite = capteur_lumiere_in.vallumiere()
        
        #On regarde si la personne souhaite le menu
        
        button_menu = buttonscroll.lire_button()
        
        if button_menu==1: #La personne souhaite le menu
            print("Ouverture du Menu")
            time.sleep(0.1)
            radar,clear_status = menu.menu(radar,est_voiture,liste_hist) 
            button_menu = 0 #Safety
            if clear_status:
                dernier_id=1 #Si l'utilisateur a effacer l'historique il faut ajuster les identifiants
            print("Fermeture du Menu")
            
        if time.time() - time_launch > 21600:
            #On envoit l'historique automatiquement tous les 6h
            print("Envoi automatique de l'historique...")
            time.sleep(0.1)
            senddweet.sendhist()
            time_launch = time.time()
            print("Historique envoyé")

        if luminosite >= threshold: #Il y a eu declenchement des phares
            
            print("Il y a eu un appel de phare")
            print("Activation Camera...")
            camera.photo() #On prend la photo
            print("Photo Prise")
            time.sleep(2)

            print("Reconnaissance de plaque...")
            os.system("python3.7 reconnaissance.py") #On lance la reconnaissance de plaque
            time.sleep(1)
            with open("plaquetext.txt","r") as f:
                plaque_lu = f.readline() #On récupère la plaque lu
            time.sleep(0.1)

            print("La plaque est : "+plaque_lu)
            autorise = False
            
            for x in liste_plaque:
                if x == plaque_lu: #Plaque dans la liste
                    liste_hist.append("IdCar_"+str(dernier_id)+":"+str(dernier_id)+",\n") 
                    #On ajoute l'id de la voiture à la liste
                    ajout_plaque="Plaque_"+str(dernier_id)+":"+plaque_lu+",\n"
                    liste_hist.append(ajout_plaque)
                    #On ajoute la plaque à la liste pour 
                    #eventuellement ajouter
                    #à l'hitorique
                    date_ent = date.today()
                    liste_hist.append("DateEnt_"+str(dernier_id)+":"+str(date_ent)+",\n")
                    #On ajoute la date d'entrée de la voiture dans le garage
                    autorise = True

            if autorise == False: #Plaque NON autorise
                print("Plaque NON Reconnu, ACCESS DENIED")
                break #On sort et on attend un autre appel

            time.sleep(2)

            print("Plaque Reconnu! Bienvenu")
            print("Ouverture Garage...")
            time.sleep(0.1)
            led.allumer_led() #Ouverture garage
            time.sleep(0.1)
            moteur.portegarage() #Moteur du garage
            time.sleep(0.1) 

            allumer = False #Pour le buzzer
            iter = 0
            constante = 10 #Distance a laquelle on veut s_arreter (cm)

            print("Garage Ouvert, Rentrez")
            if radar:
                print("Le radar est activé")
            else:
                print("Le radar est en mode silencieux")
            
            #ultra_HS = [495,495,495,495,495,495,300,300,298,189,100,99,95,90,101,105,101,91,90,89,87,86,83,82,81,79,79,78,75,73,69,65,66,64,64,63,62,60,55,54,53,52,51,48,43,40,38,37,37,36,33,30,25,23,22,20,19,17,15,13,11,9,8,4,5,8,9,10,11,12,9,7,7,1,1,7,7,7,7,7,1,7,7,6,6,6,1,6,8,8,1,8,5,1,5,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10]
            #i=0 #Ces deux variables peuvent etre utilisés pour tester le code

            while varbool: #Radar de recul
                
                distance = ultrason.lire_ultrason() #La distance de la voiture
                time.sleep(0.05)
                #distance = ultra_HS[i]
                print("Distance ->",distance)
                #i+=1
                if (constante-5) <= distance <= (constante+5):
                    iter +=1 #Distance varie pas de +-5
                else:
                    iter = 0 #La voiture a bougé
                if iter == 30: #Voiture immobile depuis quelques secondes
                    buzzer.fermer_buzzer()
                    break #On sort du radar de recul
                
                if (constante < distance <= 100) and radar: #Beep Beep
                    buzzer.allumer_buzzer()
                    allumer=True
                    time.sleep(0.01*distance)
                    buzzer.fermer_buzzer()
                    allumer=False
                    time.sleep(0.01*distance/2)

                elif (distance <= constante) and (not allumer) and radar: 
                    #Allumer en permanence en dessous d'un certain seuil
                    buzzer.allumer_buzzer()
                    time.sleep(0.01)
                    allumer=True

                elif distance <= constante and allumer and radar:
                    #Si c'est deja allumé et en dessous d'un certan seuil
                    time.sleep(0.01)

                elif allumer: #Safety
                    buzzer.fermer_buzzer()
                    time.sleep(0.1)
                    
                else:
                    time.sleep(0.1)
            
            print("La voiture est immobile")
            print("Fermeture du garage...")
            
            temps_debut=time.time()
            
            time.sleep(0.1)
            led.eteindre_led() #Fermeture garage
            time.sleep(0.1)
            moteur.portegarage() #Moteur du garage
            time.sleep(0.1)
            
            print("Le garage est fermé, Passez une bonne journée")
            est_voiture = True #il y a maintenant une voiture
            
            
    while est_voiture: #Il y a une voiture garée
        
        #On attend le declenchement des phares

        luminosite = capteur_lumiere_out.vallumiere()
        
        #On regarde si la personne souhaite le menu
        
        button_menu = buttonscroll.lire_button()
        
        if button_menu==1: #La personne souhaite le menu
            print("Ouverture du Menu")
            temps_inter = time.time()
            temps_gare_inter = temps_inter - temps_debut
            temps_gare_inter = int(temps_gare_inter)
            temps_gare_inter = seconds.convert_seconds(temps_gare_inter) #Format plus lisible
            #On indique que la voiture est encore actuellement garée
            temps_gareint_str = "Temps_"+str(dernier_id)+":"+str(temps_gare_inter)+"+Encore La,\n"
            liste_hist.append(temps_gareint_str)
            radar,clear_status = menu.menu(radar,est_voiture,liste_hist)
            liste_hist=liste_hist[:-1]
            button_menu = 0 #Safety
            if clear_status:
                dernier_id=1
                liste_hist=[]
                liste_hist.append("IdCar_"+str(dernier_id)+":"+str(dernier_id)+",\n") 
                #On ajoute l'id de la voiture à la liste
                ajout_plaque="Plaque_"+str(dernier_id)+":"+plaque_lu+",\n"
                liste_hist.append(ajout_plaque)
                #On ajoute la plaque à la liste pour 
                #eventuellement ajouter
                #à l'hitorique
                liste_hist.append("DateEnt_"+str(dernier_id)+":"+str(date_ent)+",\n")
                #On ajoute la date d'entrée de la voiture dans le garage
            print("Fermeture du Menu")
        
        if time.time() - time_launch > 21600:
            print("Envoi automatique de l'historique...")
            #On envoit l'historique automatiquement tous les 6h
            temps_inter = time.time()
            temps_gare_inter = temps_inter - temps_debut
            temps_gare_inter = int(temps_gare_inter)
            temps_gare_inter = seconds.convert_seconds(temps_gare_inter) #Format plus lisible
            #On indique que la voiture est encore actuellement garée
            temps_gareint_str = "Temps_"+str(dernier_id)+":"+str(temps_gare_inter)+"+Encore La,\n"
            liste_hist.append(temps_gareint_str)
            senddweet.ajout_historique(liste_hist)
            time.sleep(0.1)
            senddweet.sendhist()
            liste_hist=liste_hist[:-1]
            time_launch = time.time()
            print("Historique envoyé")
        
        if luminosite >= threshold: #Il y a eu declenchement des phares
            
            print("Il y a eu un appel de phare")
            print("Ouverture garage pour sortir...")
            
            time.sleep(0.1)
            led.allumer_led() #Ouverture garage
            time.sleep(0.1)
            moteur.portegarage() #Moteur du garage
            time.sleep(0.1)
            print("Veuillez sortir...")
            time.sleep(4) #La personne part
            print("Fermeture garage...")
            led.eteindre_led() #Fermeture Garage
            time.sleep(0.1)
            moteur.portegarage() #Moteur du garage
            time.sleep(0.1)
            print("Garage fermé")
            time.sleep(0.1)
            
            est_voiture = False #Il n'y a plus de voiture
            
            #On calcule le temps garé
            temps_fin = time.time()
            temps_gare = temps_fin - temps_debut
            temps_gare = int(temps_gare)
            temps_gare = seconds.convert_seconds(temps_gare) #Format plus lisible
            temps_gare_str = "Temps_"+str(dernier_id)+":"+str(temps_gare)+",\n"
            liste_hist.append(temps_gare_str)
            
            #On regarde si la personne est bien partie
            
            distance = ultrason.lire_ultrason()
            #distance = 400 #Variable utilisé lors de certains tests

            if distance <= constante + 5: #On vérifie si la personne est partie
                
                print("La voiture n'est pas partie du garage")
                liste_hist=liste_hist[:-1] #On supprime le temps garé
                est_voiture = True #La personne n'est pas partie
                
            if (not est_voiture):
                #Si la personne est partie, on ajoute à l'historique
                #et on envoit
                senddweet.ajout_historique(liste_hist)
                time.sleep(0.1)
                senddweet.sendhist()
                time.sleep(0.1)
                liste_hist=[] #On réinitialise la liste de l'historique
                dernier_id=dernier_id+1 #On attend la prochaine voiture
                print("Voiture partie, attente d'une nouvelle entrée...")


