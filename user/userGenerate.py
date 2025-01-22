import json
import random
import string
from datetime import datetime, timedelta
from userSend import create_customer

# Categories d'ages avec des plages de dates de naissance
age_categories = {
    "16-20": (2003, 2007),
    "21-30": (1993, 2002),
    "31-40": (1983, 1992),
    "41-50": (1973, 1982),
    "50-110": (1913, 1972),
}

# Options fixes pour les questions
types_consommation = ["sportif", "gourmand", "bio"]
reponse_cereales = [True, False]
gouts = ["Chocolat", "Nature", "Sucree", "Miel", "Caramel", "Speculoos", "Fraise"]
formes = ["Boule", "Triangle", "Cube", "Petale", "Donut", "Etoile"]
pour_qui = ["Consommation personnelle", "Pour mes enfants", "Les deux"]

# Prénoms et noms fictifs
prenoms_hommes = ["Alex", "Charlie", "Lucas", "Ethan", "Noah", "Liam", "Mason", "James", "Logan", "Aiden"]
prenoms_femmes = ["Emma", "Olivia", "Sophia", "Ava", "Isabella", "Mia", "Amelia", "Harper", "Lily", "Ella"]
noms = ["Smith", "Johnson", "Taylor", "Brown", "White", "Harris", "Martin", "Thompson", "Garcia", "Moore"]

def biased_choice(choices, weights):
    """Retourne une valeur basee sur une distribution de probabilites."""
    return random.choices(choices, weights=weights, k=1)[0]

def generate_date_of_birth(year_range):
    """Genere une date de naissance entre deux annees donnees."""
    start_date = datetime(year_range[0], 1, 1)
    end_date = datetime(year_range[1], 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    dob = start_date + timedelta(days=random_days)
    return dob.strftime("%d/%m/%Y")

def generate_password(length=10):
    """Genere un mot de passe aleatoire."""
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(characters) for _ in range(length))

def generate_user():
    """Genere un utilisateur avec des valeurs realistes."""
    
    # Sexe avec distribution realiste
    sexe = biased_choice(["masculin", "feminin"], [0.48, 0.52])
    
    # Prenom et Nom
    if sexe == "masculin":
        prenom = biased_choice(prenoms_hommes, [1/len(prenoms_hommes)] * len(prenoms_hommes))
    else:
        prenom = biased_choice(prenoms_femmes, [1/len(prenoms_femmes)] * len(prenoms_femmes))
    nom = biased_choice(noms, [1/len(noms)] * len(noms))
    
    # Email
    email = f"{prenom.lower()}.{nom.lower()}@exemple.com"
    
    # Mot de passe
    mot_de_passe = generate_password()
    
    # Categorie d'age et date de naissance
    age_category = biased_choice(list(age_categories.keys()), [0.2, 0.3, 0.25, 0.15, 0.1])
    dob = generate_date_of_birth(age_categories[age_category])
    
    # Type de consommation
    type_consommation = biased_choice(types_consommation, [0.35, 0.45, 0.2])
    
    # Souhaitez-vous decouvrir des cereales originales ?
    souhaite_cereales_originales = biased_choice(reponse_cereales, [0.6, 0.4])
    
    # Gout prefere, ajuste selon le sexe et l'age
    if sexe == "masculin":
        gout_preferé = biased_choice(gouts, [0.3, 0.2, 0.2, 0.1, 0.1, 0.05, 0.05])
    else:  # Feminin
        gout_preferé = biased_choice(gouts, [0.2, 0.1, 0.3, 0.2, 0.1, 0.05, 0.05])

    # Ajustement en fonction de l'age
    if "16-20" in age_category:
        gout_preferé = biased_choice(["Sucree", "Chocolat", "Fraise"], [0.4, 0.4, 0.2])
    elif "50-110" in age_category:
        gout_preferé = biased_choice(["Nature", "Miel", "Chocolat"], [0.5, 0.3, 0.2])
    
    # Forme favorite
    forme_favorite = biased_choice(formes, [0.2, 0.2, 0.2, 0.3, 0.05, 0.05])

    # Pour qui achetez-vous ?
    if "16-20" in age_category:
        consommation_pour_qui = biased_choice(pour_qui, [0.7, 0.15, 0.15])
    elif "21-50" in age_category:
        consommation_pour_qui = biased_choice(pour_qui, [0.4, 0.3, 0.3])
    else:
        consommation_pour_qui = biased_choice(pour_qui, [0.2, 0.4, 0.4])

    # Ajustements pour les enfants
    if consommation_pour_qui in ["Pour mes enfants", "Les deux"]:
        if "16-40" in age_category:  # Parents jeunes
            gout_preferé = biased_choice(["Chocolat", "Caramel", "Sucree"], [0.4, 0.3, 0.3])
        elif "41-110" in age_category:  # Parents plus ages
            gout_preferé = biased_choice(["Nature", "Miel", "Chocolat"], [0.4, 0.4, 0.2])
    
    # Construire l'utilisateur
    user = {
        "prenom": prenom,
        "nom": nom,
        "email": email,
        "mot_de_passe": mot_de_passe,
        "date_naissance": dob,
        "sexe": sexe,
        "type_consommation": type_consommation,
        "souhaitez_cereales_originales": souhaite_cereales_originales,
        "gout_prefere": gout_preferé,
        "forme_favorite": forme_favorite,
        "consommation_pour_qui": consommation_pour_qui,
    }

    return user

def generate_users(num_users):
    """Genere un nombre donne d'utilisateurs."""
    users = []
    for _ in range(num_users):
        user = generate_user()
        users.append(user)
    return users

def save_to_json(users, filename):
    """Enregistre les donnees generees dans un fichier JSON."""
    with open(filename, "w") as f:
        json.dump(users, f, indent=4)
    print(f"Les utilisateurs ont ete sauvegardes dans '{filename}'.")

if __name__ == "__main__":
    NUM_USERS = 3  # Vous pouvez ajuster le nombre d'utilisateurs
    users = generate_users(NUM_USERS)
    save_to_json(users, "user/users.json")
    for user in users:
        create_customer(user)
    print("Le scripte à fini sont exécution !")