# Read Me du Projet Garage Automatique
fait par: DELOIRE Alexandre et Jorge Rémi

IMPORTANT: Lisez le Manuel Utilisateur du projet

Informations complémentaires au manuel:

Ressources extérieures nécessaires pour faire marcher le code:

Installer Python3.7 sur la raspberry.
(n'importe quelle sous version de Python3.7 marche mais essayez de prendre la dernière)

Python3.7 peut etre trouvé sur le site officiel de python (www.python.org)
N'ECRASEZ PAS LA VERSION PYTHON3.5 DEJA INSTALLEE SUR VOTRE RASPBERRY

Une fois que vous avez installé Python3.7, il vous faut installer le module pytesseract à l'aide de pip3.7
Pour cela tapez dans un terminal : pip3.7 install pytesseract 

Il faut aussi installer le logiciel tesseract.
Tapez cette commande dans un terminal: 
sudo apt install tesseract-ocr -y


C'est tout ce qu'il vous faudra, nous faisons l'hypothèse que vous avez déja les modules grovepi, smbus, ect... sur votre raspberry.
Sinon installez les avec pip.

IMPORTANT, LANCEZ LE MAIN SEULEMENT AVEC PYTHON3.5
COMMANDE:
python3.5 main.py 
(déplacez vous dans le répertoire avec les fichiers du projet avant)

Pour information voici comment brancher les capteurs:

- Ultrason -> D3
- Ecran -> I2C1
- Led -> D4
- Capteur Lumière pour rentrer -> A0
- Capteur Lumière pour sortir -> A1
- Bouton Scroll -> D2
- Bouton Confirm -> D7
- Buzzer -> D8
- Moteur -> 
  - Power : fil rouge -> pin 2
  - Ground : fil marron -> pin 6 
  - Input : fil orange -> pin 11 C'EST LE PIN GPIO 17
- Caméra -> Port Caméra

N'OUBLIEZ PAS DE CONNECTER LA RASPBERRY A L'INTERNET 
(si vous faites un ssh et vous etes connecté à l'internet cela suffit)
