"""
====================================================================
04_zoom_decor.py
====================================================================
Le décor, ce sont simplement des rectangles dessinés avec une
"couleur" (ici un caractère), à des coordonnées précises.

On recrée ici, en ASCII, exactement les mêmes idées que dans
'etape1_decor.py' : la route, la voiture, et quelques obstacles.

Ce fichier importe 'utils_affichage.py' (notre propre fichier,
pas un module à installer) pour ne pas réécrire le moteur
d'affichage à chaque fois.

Lancez ce fichier avec :   python3 04_zoom_decor.py
====================================================================
"""

import utils_affichage as ui


print("""
Rappel : dans le vrai jeu (etape1_decor.py), chaque objet est un
pygame.Rect(x, y, largeur, hauteur), dessiné avec une couleur :

    voiture_joueur = pygame.Rect(275, 650, 50, 90)
    obstacle_1     = pygame.Rect(150, 150, 50, 90)

Ici, on utilise les MEMES idées de position (x, y), mais on les
adapte à une petite grille de texte pour pouvoir les afficher
sans fenêtre graphique.
""")

# On construit le décor : le gazon + la route
grille = ui.construire_grille()
ui.ajouter_ligne_centrale(grille)

# La voiture du joueur, en bas de l'écran (comme dans le vrai jeu)
x_voiture = ui.BORD_ROUTE + ui.LARGEUR_ROUTE // 2
y_voiture = ui.HAUTEUR_GRILLE - 2
ui.placer(grille, x_voiture, y_voiture, ui.CARACTERE_VOITURE)

# Quelques obstacles, à différentes positions (x, y)
positions_obstacles = [
    (ui.BORD_ROUTE + 1, 2),
    (ui.BORD_ROUTE + 5, 6),
    (ui.BORD_ROUTE + 3, 10),
]
for (x, y) in positions_obstacles:
    ui.placer(grille, x, y, ui.CARACTERE_OBSTACLE)

ui.afficher(grille, "Le décor recréé en ASCII")

print("""
Remarquez que :
  - le caractère 'V' représente la voiture du joueur (en bas)
  - le caractère 'X' représente un obstacle
  - le caractère '|' représente la ligne centrale en pointillés
  - en informatique graphique, l'axe Y est inversé : y=0 est EN
    HAUT de l'écran, et y augmente vers le BAS (contrairement aux
    maths, où y augmente vers le haut !)

Dans le vrai jeu, on remplace ui.placer(...) par
pygame.draw.rect(surface, couleur, rect). Le principe est
rigoureusement identique : on donne une position, une taille,
une couleur.

Passez maintenant au fichier 05_zoom_animations.py
""")
