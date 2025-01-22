import requests
from requests.auth import HTTPBasicAuth
import os
import hashlib
from dotenv import load_dotenv

# Charger le fichier .env
load_dotenv()

# Configuration de l'API
PS_WS_AUTH_KEY = os.getenv("API_KEY")
PS_SHOP_URL = os.getenv("API_URL")

# Configuration de l'API locale
#API_KEY = "B7DCTKJUSQ56E1F8QKYVNR3ZTECZVGUS"  # Remplacez par votre clé API
#API_URL = "http://localhost:8080/api/customers"  # URL locale


def create_customer(data):
    """Ajoute un client à PrestaShop via les web services."""
    # Préparer les données en XML
    
    xml_data = f"""<prestashop xmlns:xlink="http://www.w3.org/1999/xlink">
        <customer>
            <lastname>{data["nom"]}</lastname>
            <firstname>{data["prenom"]}</firstname>
            <email>{data["email"]}</email>
            <passwd>{data["mot_de_passe"]}</passwd>
            <id_default_group>3</id_default_group>
            <active>1</active>
            <newsletter>{data.get("newsletter", 0)}</newsletter>
        </customer>
    </prestashop>"""

    # En-têtes pour l'API PrestaShop
    headers = {
        "Content-Type": "application/xml",
        "Accept": "application/xml",
    }
    
    # Envoyer une requête POST à l'API
    response = requests.post(
        PS_SHOP_URL,
        auth=HTTPBasicAuth(PS_WS_AUTH_KEY, ""),
        data=xml_data,  # Envoyer les données en XML
        headers=headers,
        verify=False  # Désactive la vérification SSL en local
    )
    
    if response.status_code == 201:
        print(f"Client {data['prenom']} {data['nom']} ajouté avec succès !")
    else:
        print(f"Erreur ({response.status_code}): {response.text}")

""" users = [
    {
        "lastname": "Dupont",
        "firstname": "Marie",
        "email": "marie.dupont@example.com",
        "password": "motdepasse123",
        "newsletter": 1
    },
    {
        "lastname": "Martin",
        "firstname": "Jean",
        "email": "jean.martin@example.com",
        "password": "motdepasse456",
        "newsletter": 0
    }
]

for user in users:
    create_customer(user) """

