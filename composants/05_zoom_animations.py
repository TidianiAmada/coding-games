"""
====================================================================
05_zoom_animations.py
====================================================================
Une animation, ce n'est qu'une SUITE D'IMAGES très proches, où
l'on a juste changé une valeur (souvent y) entre chaque image.

Ce fichier affiche plusieurs images ASCII successives, où l'on
augmente la position 'y' d'un obstacle à chaque fois -- exactement
comme le fait deplacer_obstacles() dans 'etape2_animations.py'.

Lancez ce fichier avec :   python3 05_zoom_animations.py
====================================================================
"""

import utils_affichage as ui

print("""
La ligne la plus importante de toute l'étape 2 est en réalité
minuscule :

    obstacles[i].y += VITESSE_DEFILEMENT

Répétée 60 fois par seconde par la boucle de jeu, cette simple
addition suffit à donner l'illusion que l'obstacle "tombe".
C'est tout le secret de l'animation 2D : pas de magie, juste
une boucle + une addition.

Voici 5 images successives (on a ralenti le mouvement pour
qu'on puisse bien le suivre image par image) :
""")

x_voiture = ui.BORD_ROUTE + ui.LARGEUR_ROUTE // 2
y_voiture = ui.HAUTEUR_GRILLE - 2
x_obstacle = ui.BORD_ROUTE + 4
y_obstacle = 0  # l'obstacle commence en haut de l'écran

NOMBRE_IMAGES = 5
VITESSE = 3  # de combien de lignes l'obstacle descend à chaque image

for numero_image in range(1, NOMBRE_IMAGES + 1):
    grille = ui.construire_grille()
    ui.ajouter_ligne_centrale(grille, decalage=numero_image)
    ui.placer(grille, x_voiture, y_voiture, ui.CARACTERE_VOITURE)
    ui.placer(grille, x_obstacle, y_obstacle, ui.CARACTERE_OBSTACLE)

    ui.afficher(grille, f"Image {numero_image} (y_obstacle = {y_obstacle})")
    print()

    # ---- C'est ICI la ligne-clé de toute animation 2D ----
    y_obstacle += VITESSE

print("""
Vous remarquez aussi que la ligne centrale '|' se décale d'une
image à l'autre : c'est exactement comme ça que la route donne
l'illusion de défiler sous la voiture, même si la voiture, elle,
ne bouge jamais verticalement !

On y ajoute, dans le vrai jeu, un petit "recyclage" : quand un
obstacle sort de l'écran en bas (y > HAUTEUR_FENETRE), on le
replace en haut avec un nouveau x aléatoire. C'est ce qui crée
un flot infini d'obstacles, sans jamais en garder des milliers
en mémoire.

Passez maintenant au fichier 06_zoom_evenements_et_regles.py
""")
