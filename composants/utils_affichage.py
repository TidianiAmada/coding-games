"""
====================================================================
utils_affichage.py
====================================================================
Ce fichier n'est PAS un module externe à installer : c'est juste
un fichier Python qu'on a écrit nous-mêmes, et que les autres
fichiers de l'atelier importent avec `import utils_affichage`.

Il fournit un mini "moteur d'affichage" en texte (ASCII), pour
représenter la route, la voiture et les obstacles SANS avoir besoin
de Pygame ni de matplotlib. C'est moins joli qu'une vraie fenêtre de
jeu, mais ça permet de comprendre exactement les mêmes mécanismes
(positions x/y, dessin, collisions) avec uniquement la bibliothèque
standard de Python.
====================================================================
"""

# Dimensions de notre "écran" en caractères (volontairement petit
# pour que ça reste lisible dans un terminal)
LARGEUR_GRILLE = 14
HAUTEUR_GRILLE = 16

# La route occupe les colonnes 3 à 10 (8 colonnes de large)
BORD_ROUTE = 3
LARGEUR_ROUTE = 8

# Caractères utilisés pour chaque élément du décor
CARACTERE_GAZON = "."
CARACTERE_ROUTE = " "
CARACTERE_LIGNE = "|"
CARACTERE_VOITURE = "V"
CARACTERE_OBSTACLE = "X"
CARACTERE_COLLISION = "#"


def construire_grille():
    """
    Construit une grille vide (gazon partout) avec la route au milieu.
    Une grille est juste une liste de listes de caractères :
    grille[y][x] donne le caractère à la position (x, y).
    """
    grille = [[CARACTERE_GAZON for _ in range(LARGEUR_GRILLE)] for _ in range(HAUTEUR_GRILLE)]
    for y in range(HAUTEUR_GRILLE):
        for x in range(BORD_ROUTE, BORD_ROUTE + LARGEUR_ROUTE):
            grille[y][x] = CARACTERE_ROUTE
    return grille


def ajouter_ligne_centrale(grille, decalage=0):
    """Ajoute les pointillés blancs au centre de la route (en pointillés,
    comme sur une vraie route). 'decalage' permet de les faire 'bouger'
    d'une image à l'autre pour simuler le défilement."""
    centre_x = BORD_ROUTE + LARGEUR_ROUTE // 2
    for y in range(HAUTEUR_GRILLE):
        if (y + decalage) % 4 < 2:
            grille[y][centre_x] = CARACTERE_LIGNE
    return grille


def placer(grille, x, y, caractere):
    """Place un caractère à la position (x, y) si elle est visible à l'écran."""
    if 0 <= y < HAUTEUR_GRILLE and 0 <= x < LARGEUR_GRILLE:
        grille[y][x] = caractere


def afficher(grille, titre=None):
    """Affiche la grille dans le terminal, ligne par ligne."""
    if titre:
        print(f"--- {titre} ---")
    cadre = "+" + "-" * LARGEUR_GRILLE + "+"
    print(cadre)
    for ligne in grille:
        print("|" + "".join(ligne) + "|")
    print(cadre)


if __name__ == "__main__":
    # Ce bloc ne s'exécute que si on lance CE fichier directement
    # (pas quand un autre fichier fait "import utils_affichage").
    # Il sert juste à vérifier que le moteur d'affichage fonctionne.
    grille = construire_grille()
    ajouter_ligne_centrale(grille)
    placer(grille, BORD_ROUTE + 3, HAUTEUR_GRILLE - 2, CARACTERE_VOITURE)
    placer(grille, BORD_ROUTE + 1, 2, CARACTERE_OBSTACLE)
    afficher(grille, "Test du moteur d'affichage ASCII")
