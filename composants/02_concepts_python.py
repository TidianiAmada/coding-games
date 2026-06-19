"""
====================================================================
02_concepts_python.py
====================================================================
Avant de comprendre Pygame, il faut comprendre les BRIQUES DE BASE
de Python que notre jeu utilise tout le temps.

Ce fichier ne nécessite AUCUNE installation : il n'utilise que des
outils intégrés à Python (on appelle ça la "bibliothèque standard"),
en particulier le module "random" qui est livré avec Python.

Lancez ce fichier avec :   python3 02_concepts_python.py
====================================================================
"""

import random  # module intégré à Python : pas besoin de l'installer


def section(titre):
    """Petite fonction maison pour afficher un joli séparateur entre
    les sections de la démonstration."""
    print("\n" + "=" * 60)
    print(titre)
    print("=" * 60)


# --------------------------------------------------------------
# 1. LES VARIABLES ET LES TUPLES (LES COULEURS)
# --------------------------------------------------------------
section("1. Les variables et les tuples (les couleurs)")

print("""
Une VARIABLE est une boîte avec un nom, qui contient une valeur.
Un TUPLE est une petite liste figée entre parenthèses : on
l'utilise pour stocker une couleur au format RGB (Rouge, Vert,
Bleu), trois nombres entre 0 et 255.
""")

largeur_voiture = 50
hauteur_voiture = 90
couleur_voiture = (220, 30, 30)  # un tuple : (Rouge, Vert, Bleu)

print("Largeur de la voiture :", largeur_voiture, "pixels")
print("Couleur de la voiture (R, V, B) :", couleur_voiture)


# --------------------------------------------------------------
# 2. LES LISTES ET LA BOUCLE FOR
# --------------------------------------------------------------
section("2. Les listes et la boucle 'for'")

print("""
Une LISTE range plusieurs valeurs dans l'ordre, entre crochets.
La boucle 'for' permet de répéter une action pour CHAQUE élément
de la liste, plutôt que d'écrire le même code plusieurs fois.
""")

obstacles_x = [120, 280, 200]  # position horizontale de 3 obstacles

for x in obstacles_x:
    print("Un obstacle se trouve à la position x =", x)

print("Nombre total d'obstacles :", len(obstacles_x))


# --------------------------------------------------------------
# 3. LE DICTIONNAIRE : RANGER TOUTES LES INFOS DU JEU
# --------------------------------------------------------------
section("3. Le dictionnaire : ranger toutes les infos du jeu")

print("""
Un DICTIONNAIRE associe des clés (des noms) à des valeurs.
Dans 'etape3_evenements.py', on utilise un seul gros dictionnaire
appelé 'etat' pour stocker TOUT l'état du jeu (la voiture, les
obstacles, le score...). Pratique pour le faire voyager entre
les fonctions sans avoir 10 variables séparées !
""")

etat_du_jeu = {
    "score": 0,
    "vitesse": 6,
    "game_over": False,
}

print("Etat actuel du jeu :", etat_du_jeu)
print("Score actuel :", etat_du_jeu["score"])

etat_du_jeu["score"] = etat_du_jeu["score"] + 5
print("Nouveau score après modification :", etat_du_jeu["score"])


# --------------------------------------------------------------
# 4. LES FONCTIONS : DONNER UN NOM A UNE RECETTE REUTILISABLE
# --------------------------------------------------------------
section("4. Les fonctions : donner un nom à une recette réutilisable")

print("""
Une FONCTION regroupe plusieurs instructions sous un seul nom,
pour ne pas réécrire le même code partout. 'creer_obstacle()' est
utilisée plusieurs fois dans nos trois fichiers de jeu !
""")


def creer_obstacle(x, y):
    """Construit un obstacle sous la forme d'un petit dictionnaire."""
    return {"x": x, "y": y, "largeur": 50, "hauteur": 90}


obstacle_1 = creer_obstacle(120, -100)
obstacle_2 = creer_obstacle(280, -400)

print(obstacle_1)
print(obstacle_2)


# --------------------------------------------------------------
# 5. LE MODULE RANDOM : SIMULER LE HASARD
# --------------------------------------------------------------
section("5. Le module 'random' : simuler le hasard")

print("""
Le module 'random' permet de tirer des nombres au hasard. C'est
lui qui fait apparaître les obstacles à des positions différentes
à chaque partie ! Il fait partie de la bibliothèque standard de
Python : pas besoin de l'installer avec pip.
""")

for i in range(5):
    x_aleatoire = random.randint(100, 300)
    print(f"Obstacle n°{i + 1} apparait à x = {x_aleatoire}")


print("\nFin de la démonstration des concepts Python. ")
print("Passez maintenant au fichier 03_concepts_pygame.py")
