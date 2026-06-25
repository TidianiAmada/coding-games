"""
====================================================================
LABYRINTHE - ÉTAPE 2 : AJOUTER LES ANIMATIONS
====================================================================

On reprend exactement le décor de l'étape 1 (labyrinthe généré,
sol, murs, torches, personnage, pièces) et on lui donne vie :

    - les pièces flottent doucement de haut en bas et scintillent
    - les flammes des torches vacillent (taille et opacité qui
      varient légèrement à chaque image)
    - quelques particules de poussière flottent dans l'air, pour
      donner une ambiance "donjon vivant"

Le personnage ne se déplace toujours pas : ce sera l'étape 3.

Rappel du principe : une animation n'est qu'une boucle qui modifie
une valeur (une position, une taille, une opacité...) un petit peu
à chaque image affichée.
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
# 2. CONSTANTES (identiques à l'étape 1)
# --------------------------------------------------------------
TAILLE_CASE = 40
COLONNES = 15
LIGNES = 13
HAUTEUR_HUD = 70

LARGEUR_FENETRE = COLONNES * TAILLE_CASE
HAUTEUR_LABYRINTHE = LIGNES * TAILLE_CASE
HAUTEUR_FENETRE = HAUTEUR_LABYRINTHE + HAUTEUR_HUD

NOMBRE_PIECES = 12
NOMBRE_TORCHES = 5
NOMBRE_POUSSIERES = 25

COULEUR_SOL_1 = (214, 192, 150)
COULEUR_SOL_2 = (198, 176, 134)
COULEUR_MUR = (95, 72, 55)
COULEUR_MUR_CLAIR = (135, 105, 80)
COULEUR_MUR_FONCE = (60, 44, 33)
COULEUR_PERSONNAGE = (40, 120, 210)
COULEUR_PIECE = (250, 200, 40)
COULEUR_PIECE_REFLET = (255, 240, 180)
COULEUR_TEXTE = (255, 255, 255)
COULEUR_FLAMME = (250, 150, 40)

DOSSIER_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
pygame.display.set_caption("Labyrinthe - Étape 2 : Les Animations")

police = pygame.font.SysFont("Arial", 26, bold=True)


def charger_image(nom_fichier, taille=None):
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
# 3. GÉNÉRATION DU LABYRINTHE (identique à l'étape 1)
# --------------------------------------------------------------
def generer_labyrinthe(lignes, colonnes):
    grille = [[1 for _ in range(colonnes)] for _ in range(lignes)]
    for r in range(0, lignes, 2):
        for c in range(0, colonnes, 2):
            grille[r][c] = 0

    depart = (0, 0)
    visitees = {depart}
    pile = [depart]
    deplacements_possibles = [(-2, 0), (2, 0), (0, -2), (0, 2)]

    while pile:
        r, c = pile[-1]
        voisins_non_visites = []
        for dr, dc in deplacements_possibles:
            nr, nc = r + dr, c + dc
            if 0 <= nr < lignes and 0 <= nc < colonnes and (nr, nc) not in visitees:
                voisins_non_visites.append((nr, nc, dr, dc))
        if voisins_non_visites:
            nr, nc, dr, dc = random.choice(voisins_non_visites)
            grille[r + dr // 2][c + dc // 2] = 0
            grille[nr][nc] = 0
            visitees.add((nr, nc))
            pile.append((nr, nc))
        else:
            pile.pop()
    return grille


def construire_murs(grille):
    murs = []
    for r, ligne in enumerate(grille):
        for c, valeur in enumerate(ligne):
            if valeur == 1:
                rect = pygame.Rect(c * TAILLE_CASE, r * TAILLE_CASE + HAUTEUR_HUD, TAILLE_CASE, TAILLE_CASE)
                murs.append({"rect": rect, "variante": random.choice([0, 0, 1])})
    return murs


def cases_praticables(grille):
    resultat = []
    for r, ligne in enumerate(grille):
        for c, valeur in enumerate(ligne):
            if valeur == 0:
                resultat.append((r, c))
    return resultat


def case_vers_pixel(r, c):
    x = c * TAILLE_CASE + TAILLE_CASE // 2
    y = r * TAILLE_CASE + TAILLE_CASE // 2 + HAUTEUR_HUD
    return x, y


def choisir_torches(grille, nombre):
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
    torches = []
    for (r, c) in cases_choisies:
        x, y = case_vers_pixel(r, c)
        # 'phase' = un décalage aléatoire dans le temps, pour que toutes
        # les flammes ne vacillent pas exactement de la même façon
        torches.append({"x": x, "y": y, "phase": random.uniform(0, math.tau)})
    return torches


# --------------------------------------------------------------
# 4. CONSTRUCTION DE LA PARTIE
# --------------------------------------------------------------
grille_labyrinthe = generer_labyrinthe(LIGNES, COLONNES)
murs = construire_murs(grille_labyrinthe)
torches = choisir_torches(grille_labyrinthe, NOMBRE_TORCHES)

x_depart, y_depart = case_vers_pixel(0, 0)
TAILLE_PERSONNAGE = 26
personnage = pygame.Rect(0, 0, TAILLE_PERSONNAGE, TAILLE_PERSONNAGE)
personnage.center = (x_depart, y_depart)

cases_libres = [case for case in cases_praticables(grille_labyrinthe) if case != (0, 0)]
cases_pieces = random.sample(cases_libres, min(NOMBRE_PIECES, len(cases_libres)))
pieces = []
for (r, c) in cases_pieces:
    x, y = case_vers_pixel(r, c)
    # 'phase' permet à chaque pièce de flotter/scintiller à son propre
    # rythme, plutôt que toutes en même temps (plus naturel)
    pieces.append({"x": x, "y": y, "phase": random.uniform(0, math.tau), "ramassee": False})

# Quelques particules de poussière ambiante, purement décoratives
poussieres = []
for _ in range(NOMBRE_POUSSIERES):
    poussieres.append({
        "x": random.uniform(0, LARGEUR_FENETRE),
        "y": random.uniform(HAUTEUR_HUD, HAUTEUR_FENETRE),
        "vitesse_y": random.uniform(-0.3, -0.1),  # monte très lentement
        "taille": random.uniform(1, 2.5),
        "opacite": random.randint(40, 110),
    })

score = 0


# --------------------------------------------------------------
# 5. FONCTIONS D'ANIMATION (mise à jour des positions/valeurs)
# --------------------------------------------------------------
def animer_poussieres():
    """Fait monter doucement chaque particule de poussière. Quand elle
    sort de l'écran par le haut, on la replace en bas avec un nouveau x."""
    for grain in poussieres:
        grain["y"] += grain["vitesse_y"]
        if grain["y"] < HAUTEUR_HUD:
            grain["y"] = HAUTEUR_FENETRE
            grain["x"] = random.uniform(0, LARGEUR_FENETRE)


# --------------------------------------------------------------
# 6. FONCTIONS DE DESSIN
# --------------------------------------------------------------
def dessiner_sol(surface):
    for r in range(LIGNES):
        for c in range(COLONNES):
            couleur = COULEUR_SOL_1 if (r + c) % 2 == 0 else COULEUR_SOL_2
            rect = pygame.Rect(c * TAILLE_CASE, r * TAILLE_CASE + HAUTEUR_HUD, TAILLE_CASE, TAILLE_CASE)
            pygame.draw.rect(surface, couleur, rect)


def dessiner_murs(surface, liste_murs):
    epaisseur_relief = 4
    for mur in liste_murs:
        rect = mur["rect"]
        couleur_base = COULEUR_MUR if mur["variante"] == 0 else (COULEUR_MUR[0] - 6, COULEUR_MUR[1] - 4, COULEUR_MUR[2] - 4)
        pygame.draw.rect(surface, couleur_base, rect)
        pygame.draw.rect(surface, COULEUR_MUR_CLAIR, (rect.x, rect.y, rect.width, epaisseur_relief))
        pygame.draw.rect(surface, COULEUR_MUR_CLAIR, (rect.x, rect.y, epaisseur_relief, rect.height))
        pygame.draw.rect(surface, COULEUR_MUR_FONCE, (rect.x, rect.bottom - epaisseur_relief, rect.width, epaisseur_relief))
        pygame.draw.rect(surface, COULEUR_MUR_FONCE, (rect.right - epaisseur_relief, rect.y, epaisseur_relief, rect.height))


def dessiner_torche(surface, x, y, phase):
    """Dessine une torche dont la flamme VACILLE : sa taille et son
    opacité varient avec une sinusoïde + un petit bruit aléatoire,
    pour un effet de scintillement réaliste."""
    temps = pygame.time.get_ticks() / 1000  # temps écoulé, en secondes
    vacillement = math.sin(temps * 6 + phase) * 3 + random.uniform(-1, 1)

    pygame.draw.rect(surface, (70, 50, 35), (x - 3, y - 4, 6, 14), border_radius=2)

    # halo lumineux semi-transparent autour de la flamme (donne une lueur)
    rayon_halo = int(16 + vacillement)
    halo = pygame.Surface((rayon_halo * 2, rayon_halo * 2), pygame.SRCALPHA)
    pygame.draw.circle(halo, (255, 170, 60, 50), (rayon_halo, rayon_halo), rayon_halo)
    surface.blit(halo, (x - rayon_halo, y - 10 - rayon_halo))

    hauteur_flamme = 18 + vacillement
    pygame.draw.polygon(surface, COULEUR_FLAMME, [(x, y - hauteur_flamme), (x - 6, y - 4), (x + 6, y - 4)])
    pygame.draw.polygon(surface, (255, 220, 120), [(x, y - hauteur_flamme + 4), (x - 3, y - 4), (x + 3, y - 4)])


def dessiner_personnage(surface, rect, image=None):
    if image is not None:
        surface.blit(image, image.get_rect(center=rect.center))
        return
    pygame.draw.circle(surface, (10, 30, 70), rect.center, rect.width // 2 + 2)
    pygame.draw.circle(surface, COULEUR_PERSONNAGE, rect.center, rect.width // 2)
    pygame.draw.circle(surface, (140, 190, 255), (rect.centerx - 4, rect.centery - 4), 4)


def dessiner_piece(surface, x, y, phase, image=None):
    """Dessine une pièce qui FLOTTE (légère oscillation verticale) et
    SCINTILLE (son reflet change d'intensité)."""
    temps = pygame.time.get_ticks() / 1000
    decalage_y = math.sin(temps * 3 + phase) * 4         # flottement
    intensite_reflet = (math.sin(temps * 5 + phase) + 1) / 2  # entre 0 et 1

    position_y = y + decalage_y

    if image is not None:
        surface.blit(image, image.get_rect(center=(x, position_y)))
        return

    pygame.draw.circle(surface, (150, 110, 10), (x, int(position_y)), 9)
    pygame.draw.circle(surface, COULEUR_PIECE, (x, int(position_y)), 8)
    couleur_reflet = tuple(int(COULEUR_PIECE[i] + (255 - COULEUR_PIECE[i]) * intensite_reflet) for i in range(3))
    pygame.draw.circle(surface, couleur_reflet, (x - 2, int(position_y) - 2), 3)


def dessiner_poussieres(surface, liste_poussieres):
    for grain in liste_poussieres:
        particule = pygame.Surface((6, 6), pygame.SRCALPHA)
        pygame.draw.circle(particule, (255, 230, 190, grain["opacite"]), (3, 3), grain["taille"])
        surface.blit(particule, (grain["x"] - 3, grain["y"] - 3))


def dessiner_hud(surface, valeur_score, pieces_ramassees, pieces_totales):
    pygame.draw.rect(surface, (30, 24, 20), (0, 0, LARGEUR_FENETRE, HAUTEUR_HUD))
    texte_score = police.render(f"Score : {valeur_score}", True, COULEUR_TEXTE)
    texte_pieces = police.render(f"Pièces : {pieces_ramassees} / {pieces_totales}", True, COULEUR_TEXTE)
    surface.blit(texte_score, (20, HAUTEUR_HUD // 2 - texte_score.get_height() // 2))
    surface.blit(texte_pieces, (LARGEUR_FENETRE - texte_pieces.get_width() - 20,
                                 HAUTEUR_HUD // 2 - texte_pieces.get_height() // 2))


# --------------------------------------------------------------
# 7. BOUCLE PRINCIPALE
# --------------------------------------------------------------
horloge = pygame.time.Clock()
en_cours = True

while en_cours:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False

    # --- Logique / animation ---
    animer_poussieres()

    # --- Affichage ---
    dessiner_sol(fenetre)
    dessiner_murs(fenetre, murs)
    dessiner_poussieres(fenetre, poussieres)

    for torche in torches:
        dessiner_torche(fenetre, torche["x"], torche["y"], torche["phase"])

    for piece in pieces:
        if not piece["ramassee"]:
            dessiner_piece(fenetre, piece["x"], piece["y"], piece["phase"], image_piece)

    dessiner_personnage(fenetre, personnage, image_personnage)
    dessiner_hud(fenetre, score, 0, len(pieces))

    pygame.display.flip()
    horloge.tick(60)

pygame.quit()
