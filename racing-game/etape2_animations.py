"""
====================================================================
ÉTAPE 2 : AJOUTER LES ANIMATIONS (VERSION AMÉLIORÉE)
====================================================================

On reprend le décor réaliste de l'étape 1 (route avec bandes
d'urgence, arbres, voitures détaillées) et on lui donne vie :

    - la route défile (lignes + bandes jaunes "respirent" via les
      pointillés qui se décalent)
    - les arbres défilent sur le bas-côté, et réapparaissent en haut
      avec une nouvelle position quand ils sortent de l'écran
    - les obstacles tombent, avec un léger balancement gauche-droite
      qui donne un effet plus "vivant" qu'un mouvement parfaitement
      rectiligne
    - un petit nuage de poussière/fumée apparaît derrière la voiture
      du joueur, pour renforcer la sensation de vitesse

Le joueur ne contrôle toujours pas la voiture : ce sera l'étape 3.

(Voir le fichier etape1_decor.py pour les explications détaillées
sur le chargement d'images optionnelles dans "assets/".)
====================================================================
"""

import os
import math
import random
import pygame

# --------------------------------------------------------------
# 1. INITIALISATION
# --------------------------------------------------------------
pygame.init()

# --------------------------------------------------------------
# 2. CONSTANTES
# --------------------------------------------------------------
LARGEUR_FENETRE = 600
HAUTEUR_FENETRE = 600

LARGEUR_ROUTE = 360
BORD_ROUTE = (LARGEUR_FENETRE - LARGEUR_ROUTE) // 2
LARGEUR_BANDE_URGENCE = 18

COULEUR_GAZON_1 = (45, 130, 45)
COULEUR_GAZON_2 = (39, 120, 39)
COULEUR_ROUTE = (58, 58, 62)
COULEUR_BANDE_URGENCE = (90, 88, 80)
COULEUR_LIGNE_JAUNE = (235, 195, 40)
COULEUR_LIGNE_BLANCHE = (235, 235, 235)
COULEUR_TEXTE = (255, 255, 255)

COULEURS_VOITURES = [
    (200, 35, 35),
    (35, 90, 200),
    (235, 200, 40),
    (40, 150, 90),
    (230, 230, 230),
]
COULEUR_VOITURE_JOUEUR = (200, 35, 35)

VITESSE_DEFILEMENT = 6  # pixels parcourus à chaque image (60 images/seconde)

DOSSIER_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
pygame.display.set_caption("Mon Jeu de Course - Étape 2 : Les Animations (version réaliste)")

police = pygame.font.SysFont("Arial", 30, bold=True)


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


TAILLE_VOITURE = (54, 96)
TAILLE_ARBRE = (46, 46)

image_voiture_joueur = charger_image("voiture_joueur.png", TAILLE_VOITURE)
images_obstacles = [
    img for img in (
        charger_image("voiture_obstacle_1.png", TAILLE_VOITURE),
        charger_image("voiture_obstacle_2.png", TAILLE_VOITURE),
        charger_image("voiture_obstacle_3.png", TAILLE_VOITURE),
    ) if img is not None
]
image_arbre = charger_image("arbre.png", TAILLE_ARBRE)


# --------------------------------------------------------------
# 3. LA VOITURE DU JOUEUR (statique horizontalement pour l'instant)
# --------------------------------------------------------------
largeur_voiture, hauteur_voiture = TAILLE_VOITURE

voiture_joueur = pygame.Rect(
    LARGEUR_FENETRE // 2 - largeur_voiture // 2,
    HAUTEUR_FENETRE - 160,
    largeur_voiture,
    hauteur_voiture,
)

# --------------------------------------------------------------
# 4. LES LIGNES DE LA ROUTE (animées)
# --------------------------------------------------------------
largeur_ligne = 7
hauteur_pointille = 38
espace_pointille = 28
positions_lignes = list(range(0, HAUTEUR_FENETRE, hauteur_pointille + espace_pointille))


def deplacer_lignes():
    for i in range(len(positions_lignes)):
        positions_lignes[i] += VITESSE_DEFILEMENT
        if positions_lignes[i] > HAUTEUR_FENETRE:
            positions_lignes[i] -= HAUTEUR_FENETRE + hauteur_pointille + espace_pointille


# --------------------------------------------------------------
# 5. LES ARBRES (animés : ils défilent comme le reste du décor)
# --------------------------------------------------------------
NOMBRE_ARBRES = 7
arbres = []
for i in range(NOMBRE_ARBRES):
    cote_gauche = (i % 2 == 0)
    if cote_gauche:
        x = random.randint(18, BORD_ROUTE - 30)
    else:
        x = random.randint(BORD_ROUTE + LARGEUR_ROUTE + 12, LARGEUR_FENETRE - 32)
    y = int(i * (HAUTEUR_FENETRE / NOMBRE_ARBRES)) + random.randint(-20, 20)
    arbres.append({"x": x, "y": y, "echelle": random.uniform(0.8, 1.25), "cote": "gauche" if cote_gauche else "droite"})


def deplacer_arbres():
    """Fait défiler les arbres vers le bas. Quand un arbre sort de
    l'écran, on le replace en haut avec un nouveau x ALÉATOIRE mais
    du MÊME côté de la route (pour ne pas qu'un arbre saute soudain
    de la gauche à la droite, ce qui casserait l'illusion)."""
    for arbre in arbres:
        arbre["y"] += VITESSE_DEFILEMENT
        if arbre["y"] > HAUTEUR_FENETRE + 30:
            arbre["y"] = -30
            if arbre["cote"] == "gauche":
                arbre["x"] = random.randint(18, BORD_ROUTE - 30)
            else:
                arbre["x"] = random.randint(BORD_ROUTE + LARGEUR_ROUTE + 12, LARGEUR_FENETRE - 32)
            arbre["echelle"] = random.uniform(0.8, 1.25)


# --------------------------------------------------------------
# 6. LES OBSTACLES (animés : ils tombent avec un léger balancement)
# --------------------------------------------------------------
largeur_obstacle, hauteur_obstacle = TAILLE_VOITURE


def image_aleatoire_obstacle():
    return random.choice(images_obstacles) if images_obstacles else None


def creer_obstacle(y=None):
    """Crée un obstacle à une position X aléatoire sur la route, avec
    une couleur et une image (si disponible) tirées au hasard, et une
    phase de balancement aléatoire pour que tous les obstacles ne se
    balancent pas exactement en même temps (plus naturel)."""
    x_min = BORD_ROUTE + LARGEUR_BANDE_URGENCE + 8
    x_max = BORD_ROUTE + LARGEUR_ROUTE - LARGEUR_BANDE_URGENCE - largeur_obstacle - 8
    x = random.randint(x_min, x_max)
    if y is None:
        y = -hauteur_obstacle - random.randint(0, 300)
    return {
        "rect": pygame.Rect(x, y, largeur_obstacle, hauteur_obstacle),
        "x_base": x,  # position centrale autour de laquelle on balance
        "phase": random.uniform(0, math.tau),
        "couleur": random.choice(COULEURS_VOITURES),
        "image": image_aleatoire_obstacle(),
    }


obstacles = [creer_obstacle(y=-200), creer_obstacle(y=-500), creer_obstacle(y=-800)]


def deplacer_obstacles():
    """Fait descendre chaque obstacle, avec un léger mouvement sinusoïdal
    gauche-droite (comme si le véhicule corrigeait sa trajectoire),
    et le 'recycle' en haut quand il sort de l'écran."""
    x_min = BORD_ROUTE + LARGEUR_BANDE_URGENCE + 8
    x_max = BORD_ROUTE + LARGEUR_ROUTE - LARGEUR_BANDE_URGENCE - largeur_obstacle - 8

    for i in range(len(obstacles)):
        obstacle = obstacles[i]
        obstacle["rect"].y += VITESSE_DEFILEMENT

        # Le balancement : une sinusoïde douce autour de x_base.
        balancement = math.sin(pygame.time.get_ticks() / 400 + obstacle["phase"]) * 18
        nouveau_x = obstacle["x_base"] + balancement
        obstacle["rect"].x = int(max(x_min, min(x_max, nouveau_x)))

        if obstacle["rect"].y > HAUTEUR_FENETRE:
            obstacles[i] = creer_obstacle(y=-hauteur_obstacle)


# --------------------------------------------------------------
# 7. PARTICULES DE POUSSIÈRE DERRIÈRE LA VOITURE (effet de vitesse)
# --------------------------------------------------------------
particules = []  # chaque particule : {"x", "y", "vie"} ; "vie" décroît jusqu'à 0


def emettre_particule():
    """Fait apparaître un petit nuage de poussière juste derrière la
    voiture (donc en dessous d'elle à l'écran, puisque y augmente vers
    le bas)."""
    x = voiture_joueur.centerx + random.randint(-14, 14)
    y = voiture_joueur.bottom + random.randint(0, 6)
    particules.append({"x": x, "y": y, "vie": 18})


def mettre_a_jour_particules():
    """Fait vieillir chaque particule (elle descend doucement et
    s'estompe), et retire celles qui ont atteint la fin de leur vie."""
    for particule in particules:
        particule["y"] += 2
        particule["vie"] -= 1
    # On garde uniquement les particules encore "vivantes"
    particules[:] = [p for p in particules if p["vie"] > 0]


def dessiner_particules(surface):
    for particule in particules:
        opacite = max(0, min(255, particule["vie"] * 12))
        rayon = 3 + (18 - particule["vie"]) // 6
        nuage = pygame.Surface((rayon * 2, rayon * 2), pygame.SRCALPHA)
        pygame.draw.circle(nuage, (210, 210, 200, opacite), (rayon, rayon), rayon)
        surface.blit(nuage, (particule["x"] - rayon, particule["y"] - rayon))


# --------------------------------------------------------------
# 8. SCORE (figé pour l'instant)
# --------------------------------------------------------------
score = 0


# --------------------------------------------------------------
# 9. FONCTIONS DE DESSIN (identiques à l'étape 1)
# --------------------------------------------------------------
def dessiner_fond_et_route(surface):
    hauteur_bande = 40
    for y in range(0, HAUTEUR_FENETRE, hauteur_bande):
        couleur = COULEUR_GAZON_1 if (y // hauteur_bande) % 2 == 0 else COULEUR_GAZON_2
        pygame.draw.rect(surface, couleur, (0, y, LARGEUR_FENETRE, hauteur_bande))

    pygame.draw.rect(surface, COULEUR_ROUTE, (BORD_ROUTE, 0, LARGEUR_ROUTE, HAUTEUR_FENETRE))
    pygame.draw.rect(surface, COULEUR_BANDE_URGENCE, (BORD_ROUTE, 0, LARGEUR_BANDE_URGENCE, HAUTEUR_FENETRE))
    pygame.draw.rect(surface, COULEUR_BANDE_URGENCE,
                      (BORD_ROUTE + LARGEUR_ROUTE - LARGEUR_BANDE_URGENCE, 0, LARGEUR_BANDE_URGENCE, HAUTEUR_FENETRE))

    epaisseur_ligne_jaune = 4
    x_jaune_gauche = BORD_ROUTE + LARGEUR_BANDE_URGENCE
    x_jaune_droite = BORD_ROUTE + LARGEUR_ROUTE - LARGEUR_BANDE_URGENCE - epaisseur_ligne_jaune
    pygame.draw.rect(surface, COULEUR_LIGNE_JAUNE, (x_jaune_gauche, 0, epaisseur_ligne_jaune, HAUTEUR_FENETRE))
    pygame.draw.rect(surface, COULEUR_LIGNE_JAUNE, (x_jaune_droite, 0, epaisseur_ligne_jaune, HAUTEUR_FENETRE))


def dessiner_lignes_centrales(surface):
    x_ligne = LARGEUR_FENETRE // 2 - largeur_ligne // 2
    for y in positions_lignes:
        pygame.draw.rect(surface, COULEUR_LIGNE_BLANCHE, (x_ligne, y, largeur_ligne, hauteur_pointille))


def dessiner_arbre(surface, x, y, echelle=1.0, image=None):
    if image is not None:
        rect_image = image.get_rect(center=(x, y))
        surface.blit(image, rect_image)
        return
    rayon = int(20 * echelle)
    largeur_tronc = max(4, int(8 * echelle))
    hauteur_tronc = int(16 * echelle)
    pygame.draw.ellipse(surface, (20, 70, 20), (x - rayon, y + rayon - 6, rayon * 2, 12))
    pygame.draw.rect(surface, (96, 64, 40), (x - largeur_tronc // 2, y, largeur_tronc, hauteur_tronc))
    pygame.draw.circle(surface, (24, 100, 35), (x, y - int(6 * echelle)), rayon)
    pygame.draw.circle(surface, (34, 130, 45), (x - int(9 * echelle), y - int(11 * echelle)), int(rayon * 0.78))
    pygame.draw.circle(surface, (46, 150, 55), (x + int(9 * echelle), y - int(11 * echelle)), int(rayon * 0.78))


def dessiner_voiture(surface, rect, couleur_carrosserie, image=None):
    if image is not None:
        surface.blit(image, rect)
        return

    x, y, largeur, hauteur = rect.x, rect.y, rect.width, rect.height

    surface_ombre = pygame.Surface((largeur + 12, hauteur + 12), pygame.SRCALPHA)
    pygame.draw.ellipse(surface_ombre, (0, 0, 0, 80), surface_ombre.get_rect())
    surface.blit(surface_ombre, (x - 2, y))

    largeur_roue, hauteur_roue = 8, 20
    for decalage_y in (10, hauteur - 30):
        pygame.draw.rect(surface, (20, 20, 20), (x - 3, y + decalage_y, largeur_roue, hauteur_roue), border_radius=2)
        pygame.draw.rect(surface, (20, 20, 20), (x + largeur - largeur_roue + 3, y + decalage_y, largeur_roue, hauteur_roue), border_radius=2)

    pygame.draw.rect(surface, couleur_carrosserie, rect, border_radius=14)
    couleur_reflet = tuple(min(255, c + 45) for c in couleur_carrosserie)
    pygame.draw.rect(surface, couleur_reflet, (x + 5, y + 4, largeur - 10, 6), border_radius=3)

    couleur_vitre = (35, 40, 55)
    pare_brise = pygame.Rect(x + 8, y + 16, largeur - 16, 22)
    lunette_arriere = pygame.Rect(x + 8, y + hauteur - 38, largeur - 16, 18)
    pygame.draw.rect(surface, couleur_vitre, pare_brise, border_radius=6)
    pygame.draw.rect(surface, couleur_vitre, lunette_arriere, border_radius=6)

    pygame.draw.circle(surface, (255, 250, 210), (x + 9, y + 6), 4)
    pygame.draw.circle(surface, (255, 250, 210), (x + largeur - 9, y + 6), 4)
    pygame.draw.rect(surface, (200, 30, 30), (x + 6, y + hauteur - 6, 10, 4), border_radius=2)
    pygame.draw.rect(surface, (200, 30, 30), (x + largeur - 16, y + hauteur - 6, 10, 4), border_radius=2)


def dessiner_score(surface, valeur_score):
    texte = police.render(f"Score : {valeur_score}", True, COULEUR_TEXTE)
    largeur_cadre = texte.get_width() + 24
    hauteur_cadre = texte.get_height() + 14
    cadre = pygame.Surface((largeur_cadre, hauteur_cadre), pygame.SRCALPHA)
    pygame.draw.rect(cadre, (0, 0, 0, 120), cadre.get_rect(), border_radius=10)
    surface.blit(cadre, (14, 14))
    surface.blit(texte, (14 + 12, 14 + 7))


# --------------------------------------------------------------
# 10. BOUCLE PRINCIPALE
# --------------------------------------------------------------
horloge = pygame.time.Clock()
compteur_frames = 0
en_cours = True

while en_cours:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False

    # --- Logique / animation ---
    deplacer_lignes()
    deplacer_arbres()
    deplacer_obstacles()

    # On émet une particule de poussière environ toutes les 3 images
    # (sinon il y en aurait beaucoup trop, et l'effet serait moins joli)
    compteur_frames += 1
    if compteur_frames % 3 == 0:
        emettre_particule()
    mettre_a_jour_particules()

    # --- Affichage, du fond vers le premier plan ---
    dessiner_fond_et_route(fenetre)
    for arbre in arbres:
        dessiner_arbre(fenetre, arbre["x"], arbre["y"], arbre["echelle"], image_arbre)
    dessiner_lignes_centrales(fenetre)
    dessiner_particules(fenetre)

    for obstacle in obstacles:
        dessiner_voiture(fenetre, obstacle["rect"], obstacle["couleur"], obstacle["image"])

    dessiner_voiture(fenetre, voiture_joueur, COULEUR_VOITURE_JOUEUR, image_voiture_joueur)
    dessiner_score(fenetre, score)

    pygame.display.flip()
    horloge.tick(60)

pygame.quit()
