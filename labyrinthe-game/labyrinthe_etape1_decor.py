"""
====================================================================
LABYRINTHE - ÉTAPE 1 : CRÉER LE DÉCOR
====================================================================

Nouveau mini-jeu : un personnage se déplace dans un labyrinthe et
ramasse des pièces. On suit exactement la même méthode que pour le
jeu de course :

    Étape 1 (ce fichier)  -> le décor : labyrinthe, sol, personnage,
                              pièces, torches, score
    Étape 2                -> les animations : pièces qui scintillent,
                              torches qui vacillent, poussière ambiante
    Étape 3                -> les événements : déplacement au clavier,
                              collisions avec les murs, ramassage des
                              pièces, victoire

Contrairement au jeu de course, le labyrinthe n'est PAS dessiné "à la
main" : il est généré par un algorithme (un parcours en profondeur,
voir la fonction generer_labyrinthe), ce qui veut dire qu'il sera
différent à chaque fois que vous relancerez le jeu !

------------------------------------------------------------------
IMAGES OPTIONNELLES (comme pour le jeu de course) :
------------------------------------------------------------------
Si vous créez un dossier "assets" à côté de ce fichier et que vous y
placez :
    assets/personnage.png   (vu de dessus)
    assets/piece.png        (une pièce/pièce de monnaie)
elles seront utilisées automatiquement. Sinon, le jeu dessine ces
éléments lui-même (cercle bleu pour le personnage, disque doré pour
les pièces).
====================================================================
"""

import os
import random
import math
import pygame

# --------------------------------------------------------------
# 1. INITIALISATION
# --------------------------------------------------------------
pygame.init()

# --------------------------------------------------------------
# 2. CONSTANTES
# --------------------------------------------------------------
TAILLE_CASE = 40          # taille d'une case du labyrinthe, en pixels
COLONNES = 15              # nombre de cases en largeur (doit être impair)
LIGNES = 13                 # nombre de cases en hauteur (doit être impair)
HAUTEUR_HUD = 70            # bandeau du haut, pour le score

LARGEUR_FENETRE = COLONNES * TAILLE_CASE
HAUTEUR_LABYRINTHE = LIGNES * TAILLE_CASE
HAUTEUR_FENETRE = HAUTEUR_LABYRINTHE + HAUTEUR_HUD

NOMBRE_PIECES = 12
NOMBRE_TORCHES = 5

# Couleurs (R, V, B)
COULEUR_SOL_1 = (214, 192, 150)
COULEUR_SOL_2 = (198, 176, 134)
COULEUR_MUR = (95, 72, 55)
COULEUR_MUR_CLAIR = (135, 105, 80)    # reflet en haut/à gauche du mur (effet "3D")
COULEUR_MUR_FONCE = (60, 44, 33)      # ombre en bas/à droite du mur
COULEUR_PERSONNAGE = (40, 120, 210)
COULEUR_PIECE = (250, 200, 40)
COULEUR_PIECE_REFLET = (255, 240, 180)
COULEUR_TEXTE = (255, 255, 255)
COULEUR_FLAMME = (250, 150, 40)

DOSSIER_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
pygame.display.set_caption("Labyrinthe - Étape 1 : Le Décor")

police = pygame.font.SysFont("Arial", 26, bold=True)


def charger_image(nom_fichier, taille=None):
    """Charge une image dans 'assets/' si elle existe, sinon renvoie None
    (le jeu dessinera alors une version vectorielle à la place)."""
    chemin = os.path.join(DOSSIER_ASSETS, nom_fichier)
    if not os.path.isfile(chemin):
        return None
    try:
        image = pygame.image.load(chemin).convert_alpha()
        if taille:
            image = pygame.transform.smoothscale(image, taille)
        return image
    except pygame.error as erreur:
        print(f"[Info] Impossible de charger {chemin} ({erreur}) : on utilise le dessin vectoriel.")
        return None


image_personnage = charger_image("personnage.png", (28, 28))
image_piece = charger_image("piece.png", (18, 18))


# --------------------------------------------------------------
# 3. GÉNÉRATION DU LABYRINTHE
# --------------------------------------------------------------
def generer_labyrinthe(lignes, colonnes):
    """
    Génère un labyrinthe "parfait" (un seul chemin possible entre deux
    cases quelconques, pas de boucle) avec un algorithme classique :
    le parcours en profondeur (DFS) sur une grille.

    Principe : on imagine une grille de "salles" placées uniquement
    aux cases PAIRES (0, 2, 4...). Au départ, tout est mur (1). On part
    d'une salle, on choisit une salle voisine non visitée au hasard, on
    "creuse" le mur entre les deux, puis on continue depuis cette
    nouvelle salle -- exactement comme on explorerait un vrai labyrinthe
    en posant la main sur le mur et en reculant dès qu'on est bloqué.

    Renvoie une grille (liste de listes) où :
        0 = case praticable (sol)
        1 = case mur
    """
    grille = [[1 for _ in range(colonnes)] for _ in range(lignes)]

    # Toutes les "salles" (cases paires) commencent praticables
    for r in range(0, lignes, 2):
        for c in range(0, colonnes, 2):
            grille[r][c] = 0

    depart = (0, 0)
    visitees = {depart}
    pile = [depart]  # on utilise une pile pour explorer "en profondeur"

    deplacements_possibles = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # haut, bas, gauche, droite

    while pile:
        r, c = pile[-1]  # la case actuelle = sommet de la pile

        voisins_non_visites = []
        for dr, dc in deplacements_possibles:
            nr, nc = r + dr, c + dc
            if 0 <= nr < lignes and 0 <= nc < colonnes and (nr, nc) not in visitees:
                voisins_non_visites.append((nr, nc, dr, dc))

        if voisins_non_visites:
            nr, nc, dr, dc = random.choice(voisins_non_visites)
            # on creuse le mur qui se trouve EXACTEMENT entre les 2 salles
            grille[r + dr // 2][c + dc // 2] = 0
            grille[nr][nc] = 0
            visitees.add((nr, nc))
            pile.append((nr, nc))
        else:
            # plus aucun voisin disponible : on "recule" (backtrack)
            pile.pop()

    return grille


def construire_murs(grille):
    """Transforme la grille (0/1) en une liste de rectangles Pygame,
    un par case de mur. C'est cette liste qu'on utilisera plus tard
    pour dessiner les murs ET pour détecter les collisions."""
    murs = []
    for r, ligne in enumerate(grille):
        for c, valeur in enumerate(ligne):
            if valeur == 1:
                rect = pygame.Rect(c * TAILLE_CASE, r * TAILLE_CASE + HAUTEUR_HUD, TAILLE_CASE, TAILLE_CASE)
                # une petite variante de teinte, choisie UNE FOIS pour
                # que chaque mur ait toujours le même aspect (sinon ça
                # clignoterait à chaque image affichée)
                murs.append({"rect": rect, "variante": random.choice([0, 0, 1])})
    return murs


def cases_praticables(grille):
    """Renvoie la liste de toutes les coordonnées (r, c) praticables."""
    resultat = []
    for r, ligne in enumerate(grille):
        for c, valeur in enumerate(ligne):
            if valeur == 0:
                resultat.append((r, c))
    return resultat


def case_vers_pixel(r, c):
    """Convertit des coordonnées de case (r, c) en coordonnées du CENTRE
    de cette case à l'écran, en pixels."""
    x = c * TAILLE_CASE + TAILLE_CASE // 2
    y = r * TAILLE_CASE + TAILLE_CASE // 2 + HAUTEUR_HUD
    return x, y


def choisir_torches(grille, murs, nombre):
    """Choisit quelques cases de MUR qui touchent au moins une case de
    sol, pour y accrocher une torche décorative (comme dans un vrai
    donjon, les torches sont fixées AU mur, pas posées par terre)."""
    candidats = []
    lignes, colonnes = len(grille), len(grille[0])
    for r in range(lignes):
        for c in range(colonnes):
            if grille[r][c] != 1:
                continue
            voisins = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
            touche_un_sol = any(
                0 <= vr < lignes and 0 <= vc < colonnes and grille[vr][vc] == 0
                for vr, vc in voisins
            )
            if touche_un_sol:
                candidats.append((r, c))

    nombre = min(nombre, len(candidats))
    cases_choisies = random.sample(candidats, nombre)
    return [{"x": case_vers_pixel(r, c)[0], "y": case_vers_pixel(r, c)[1]} for r, c in cases_choisies]


# --------------------------------------------------------------
# 4. CONSTRUCTION DE LA PARTIE
# --------------------------------------------------------------
grille_labyrinthe = generer_labyrinthe(LIGNES, COLONNES)
murs = construire_murs(grille_labyrinthe)
torches = choisir_torches(grille_labyrinthe, murs, NOMBRE_TORCHES)

# Le personnage démarre toujours dans la case (0, 0), qui est forcément
# praticable (c'est notre point de départ dans generer_labyrinthe).
x_depart, y_depart = case_vers_pixel(0, 0)
TAILLE_PERSONNAGE = 26
personnage = pygame.Rect(0, 0, TAILLE_PERSONNAGE, TAILLE_PERSONNAGE)
personnage.center = (x_depart, y_depart)

# Les pièces sont placées sur des cases praticables, en évitant la case
# de départ du personnage.
cases_libres = [case for case in cases_praticables(grille_labyrinthe) if case != (0, 0)]
cases_pieces = random.sample(cases_libres, min(NOMBRE_PIECES, len(cases_libres)))
pieces = []
for (r, c) in cases_pieces:
    x, y = case_vers_pixel(r, c)
    pieces.append({"x": x, "y": y, "ramassee": False})

score = 0


# --------------------------------------------------------------
# 5. FONCTIONS DE DESSIN
# --------------------------------------------------------------
def dessiner_sol(surface):
    """Dessine le sol en damier (2 teintes de sable), case par case."""
    for r in range(LIGNES):
        for c in range(COLONNES):
            couleur = COULEUR_SOL_1 if (r + c) % 2 == 0 else COULEUR_SOL_2
            rect = pygame.Rect(c * TAILLE_CASE, r * TAILLE_CASE + HAUTEUR_HUD, TAILLE_CASE, TAILLE_CASE)
            pygame.draw.rect(surface, couleur, rect)


def dessiner_murs(surface, liste_murs):
    """Dessine chaque mur avec un petit effet de relief (bord clair en
    haut/à gauche, bord sombre en bas/à droite) pour qu'il ressemble
    à un bloc de pierre plutôt qu'à un simple carré plat."""
    epaisseur_relief = 4
    for mur in liste_murs:
        rect = mur["rect"]
        couleur_base = COULEUR_MUR if mur["variante"] == 0 else (COULEUR_MUR[0] - 6, COULEUR_MUR[1] - 4, COULEUR_MUR[2] - 4)
        pygame.draw.rect(surface, couleur_base, rect)
        # reflet clair (haut + gauche)
        pygame.draw.rect(surface, COULEUR_MUR_CLAIR, (rect.x, rect.y, rect.width, epaisseur_relief))
        pygame.draw.rect(surface, COULEUR_MUR_CLAIR, (rect.x, rect.y, epaisseur_relief, rect.height))
        # ombre sombre (bas + droite)
        pygame.draw.rect(surface, COULEUR_MUR_FONCE, (rect.x, rect.bottom - epaisseur_relief, rect.width, epaisseur_relief))
        pygame.draw.rect(surface, COULEUR_MUR_FONCE, (rect.right - epaisseur_relief, rect.y, epaisseur_relief, rect.height))


def dessiner_torche(surface, x, y):
    """Dessine une torche fixée au mur : un petit support marron et une
    flamme orange (statique pour l'instant, elle vacillera à l'étape 2)."""
    pygame.draw.rect(surface, (70, 50, 35), (x - 3, y - 4, 6, 14), border_radius=2)
    pygame.draw.polygon(surface, COULEUR_FLAMME, [(x, y - 18), (x - 6, y - 4), (x + 6, y - 4)])
    pygame.draw.polygon(surface, (255, 220, 120), [(x, y - 14), (x - 3, y - 4), (x + 3, y - 4)])


def dessiner_personnage(surface, rect, image=None):
    """Dessine le personnage du joueur : une image si fournie, sinon un
    cercle bleu avec un petit reflet pour donner un peu de volume."""
    if image is not None:
        surface.blit(image, image.get_rect(center=rect.center))
        return
    pygame.draw.circle(surface, (10, 30, 70), rect.center, rect.width // 2 + 2)  # contour foncé
    pygame.draw.circle(surface, COULEUR_PERSONNAGE, rect.center, rect.width // 2)
    pygame.draw.circle(surface, (140, 190, 255), (rect.centerx - 4, rect.centery - 4), 4)  # reflet


def dessiner_piece(surface, x, y, image=None):
    """Dessine une pièce de monnaie : une image si fournie, sinon un
    disque doré avec un reflet en forme de croissant."""
    if image is not None:
        surface.blit(image, image.get_rect(center=(x, y)))
        return
    pygame.draw.circle(surface, (150, 110, 10), (x, y), 9)       # contour foncé (relief)
    pygame.draw.circle(surface, COULEUR_PIECE, (x, y), 8)
    pygame.draw.circle(surface, COULEUR_PIECE_REFLET, (x - 2, y - 2), 3)


def dessiner_hud(surface, valeur_score, pieces_ramassees, pieces_totales):
    """Bandeau du haut avec le score et le nombre de pièces restantes."""
    pygame.draw.rect(surface, (30, 24, 20), (0, 0, LARGEUR_FENETRE, HAUTEUR_HUD))
    texte_score = police.render(f"Score : {valeur_score}", True, COULEUR_TEXTE)
    texte_pieces = police.render(f"Pièces : {pieces_ramassees} / {pieces_totales}", True, COULEUR_TEXTE)
    surface.blit(texte_score, (20, HAUTEUR_HUD // 2 - texte_score.get_height() // 2))
    surface.blit(texte_pieces, (LARGEUR_FENETRE - texte_pieces.get_width() - 20,
                                 HAUTEUR_HUD // 2 - texte_pieces.get_height() // 2))


# --------------------------------------------------------------
# 6. BOUCLE PRINCIPALE (rien ne bouge encore : décor uniquement)
# --------------------------------------------------------------
horloge = pygame.time.Clock()
en_cours = True

while en_cours:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False

    dessiner_sol(fenetre)
    dessiner_murs(fenetre, murs)
    for torche in torches:
        dessiner_torche(fenetre, torche["x"], torche["y"])
    for piece in pieces:
        if not piece["ramassee"]:
            dessiner_piece(fenetre, piece["x"], piece["y"], image_piece)
    dessiner_personnage(fenetre, personnage, image_personnage)
    dessiner_hud(fenetre, score, 0, len(pieces))

    pygame.display.flip()
    horloge.tick(60)

pygame.quit()
