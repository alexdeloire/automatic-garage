# stdlib imports
import time
import json

try:
    # python 3
    from urllib.parse import quote
except ImportError:
    # python 2
    from urllib import quote

# third-party imports
import requests


# base url for all requests
BASE_URL = 'https://dweet.io'
path_hist = r"/home/pi/garage/historique.txt"
#path_hist = r"/home/alexandre/Desktop/transfer/historique.txt"


class DweepyError(Exception):
    pass


def _request(method, url, session=None, **kwargs):
    """Make HTTP request, raising an exception if it fails.
    """
    url = BASE_URL + url

    if session:
        request_func = getattr(session, method)
    else:
        request_func = getattr(requests, method)
    response = request_func(url, **kwargs)
    # raise an exception if request is not successful
    if not response.status_code == requests.codes.ok:
        raise DweepyError('HTTP {0} response'.format(response.status_code))
    response_json = response.json()
    if response_json['this'] == 'failed':
        raise DweepyError(response_json['because'])
    return response_json['with']


def _send_dweet(payload, url, params=None, session=None):
    """Send a dweet to dweet.io
    """
    data = json.dumps(payload, sort_keys=True)
    headers = {'Content-type': 'application/json'}
    return _request('post', url, data=data, headers=headers, params=params, session=session)


def dweet(payload, session=None):
    """Send a dweet to dweet.io without naming your thing
    """
    return _send_dweet(payload, '/dweet', session=session)


def dweet_for(thing_name, payload, key=None, session=None):
    """Send a dweet to dweet.io for a thing with a known name
    """
    if key is not None:
        params = {'key': key}
    else:
        params = None
    return _send_dweet(payload, '/dweet/for/{0}'.format(thing_name), params=params, session=session)


def get_latest_dweet_for(thing_name, key=None, session=None):
    """Read the latest dweet for a dweeter
    """
    if key is not None:
        params = {'key': key}
    else:
        params = None
    return _request('get', '/get/latest/dweet/for/{0}'.format(thing_name), params=params, session=session)


def get_dweets_for(thing_name, key=None, session=None):
    """Read all the dweets for a dweeter
    """
    if key is not None:
        params = {'key': key}
    else:
        params = None
    return _request('get', '/get/dweets/for/{0}'.format(thing_name), params=params, session=None)


def remove_lock(lock, key, session=None):
    """Remove a lock (no matter what it's connected to).
    """
    return _request('get', '/remove/lock/{0}'.format(lock), params={'key': key}, session=session)


def lock(thing_name, lock, key, session=None):
    """Lock a thing (prevents unauthed dweets for the locked thing)
    """
    return _request('get', '/lock/{0}'.format(thing_name), params={'key': key, 'lock': lock}, session=session)


def unlock(thing_name, key, session=None):
    """Unlock a thing
    """
    return _request('get', '/unlock/{0}'.format(thing_name), params={'key': key}, session=session)


def set_alert(thing_name, who, condition, key, session=None):
    """Set an alert on a thing with the given condition
    """
    return _request('get', '/alert/{0}/when/{1}/{2}'.format(
        ','.join(who),
        thing_name,
        quote(condition),
    ), params={'key': key}, session=session)


def get_alert(thing_name, key, session=None):
    """Set an alert on a thing with the given condition
    """
    return _request('get', '/get/alert/for/{0}'.format(thing_name), params={'key': key}, session=session)


def remove_alert(thing_name, key, session=None):
    """Remove an alert for the given thing
    """
    return _request('get', '/remove/alert/for/{0}'.format(thing_name), params={'key': key}, session=session)


def sendhist(): 
    #Cette fonction construit le payload à partir du fichier historique.txt
    #et envoit l'historique du garage sur dweet à l'objet GarageFASEProj

    payload = {} #Ce qu'on va envoyer sur dweet.io

    with open(path_hist,"r") as file:
        liste = file.readlines() #On recupère l'historique

    for i in range(len(liste)): #On enlève les ,\n
            liste[i]=liste[i][:-2]

    for x in liste: #On construit le payload
        inter = x.split(":")
        if inter[0][:-1]=="IdCar_":
            payload[inter[0]]=int(inter[1]) #Pour que ca soit un integer
        else:
            payload[inter[0]]=inter[1]

    dweet_for("GarageFASEProj",payload)

def get_plaque():
    #Cette fonction recupère la plaque de la dernière personne
    #qui s'est garé dans le garage.

    payload = get_latest_dweet_for("GarageFASEProj")
    contenu=payload[0]["content"] #On récupère le contenu du dernier dweet
    
    last_car = 0
    for x in contenu.keys(): #On récupère l'ID de la derniere voiture
        if x[:-1]=="IdCar_":
            if contenu[x] >= last_car:
                last_car = contenu[x]
    plaque = contenu["Plaque_"+str(last_car)]
    plaque = str(plaque) #Pour les plaques int, pour pouvoir afficher

    return plaque


def ajout_historique(liste):
    #Cette focntion ajoute une entree dans le fichier historique
    with open(path_hist,"a") as file:
        for line in liste:
            file.write(line)

def get_id():
    #Recupere l'ID de la derniere voiture de l'historique
    #Utile si il y a une coupure de courant et au demarrage

    payload = {}
    with open(path_hist,"r") as file:
        liste = file.readlines() #On recupère l'historique

    for i in range(len(liste)): #On enlève les ,\n
            liste[i]=liste[i][:-2]

    for x in liste: #On construit le payload
        inter = x.split(":")
        if inter[0][:-1]=="IdCar_":
            payload[inter[0]]=int(inter[1]) #Pour que ca soit un integer
        else:
            payload[inter[0]]=inter[1]

    last_car = 0
    for x in payload.keys(): #On récupère l'ID de la derniere voiture
        if x[:-1]=="IdCar_":
            if payload[x] >= last_car:
                last_car = payload[x]
    
    return last_car

def clear_hist():
    #Cette fonction supprime l'historique du fichier historique et du site web
    with open(path_hist,"w") as file:
        file.write("")
    dweet_for("GarageFASEProj",{})

#Tests

#clear_hist()

#time.sleep(0.5)

#ajout_historique(["IdCar_7:7,\n","Plaque_7:Test2,\n","DateEnt_7:11-16-2022,\n","Temps_7:1h,\n"])

#time.sleep(0.5)

#sendhist()

#time.sleep(0.5)

#print(get_plaque())
