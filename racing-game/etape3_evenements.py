"""
====================================================================
ÉTAPE 3 : GÉRER LES ÉVÉNEMENTS (VERSION AMÉLIORÉE - JEU COMPLET)
====================================================================

C'est le fichier final, à lancer pour JOUER pour de vrai. Il reprend
le décor réaliste et les animations des étapes 1 et 2, et ajoute :

    - le contrôle de la voiture avec les flèches gauche/droite
    - une accélération/décélération avec les flèches haut/bas
      (la vitesse de défilement change, ce qui est plus amusant
      qu'une vitesse fixe)
    - la détection de collision (avec un effet de "flash rouge"
      à l'impact, pour un Game Over plus spectaculaire)
    - un score qui augmente avec le temps + un bonus par obstacle évité
    - un écran de Game Over avec relance via la touche ESPACE

(Voir etape1_decor.py pour les explications sur le chargement
d'images optionnelles dans le dossier "assets/".)
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
COULEUR_GAME_OVER = (255, 70, 70)

COULEURS_VOITURES = [
    (200, 35, 35),
    (35, 90, 200),
    (235, 200, 40),
    (40, 150, 90),
    (230, 230, 230),
]
COULEUR_VOITURE_JOUEUR = (200, 35, 35)

VITESSE_DEFILEMENT_MIN = 4
VITESSE_DEFILEMENT_MAX = 16
VITESSE_DEFILEMENT_INITIALE = 6
ACCELERATION_PAR_FRAME = 0.25     # effet de la flèche HAUT
FREINAGE_PAR_FRAME = 0.35         # effet de la flèche BAS
RALENTISSEMENT_NATUREL = 0.04     # la vitesse revient doucement vers la valeur initiale
VITESSE_VOITURE_JOUEUR = 7        # déplacement horizontal en pixels par image

DOSSIER_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
pygame.display.set_caption("Mon Jeu de Course - Étape 3 : Le Jeu Complet (version réaliste)")

police = pygame.font.SysFont("Arial", 30, bold=True)
police_titre = pygame.font.SysFont("Arial", 54, bold=True)


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

largeur_voiture, hauteur_voiture = TAILLE_VOITURE
largeur_obstacle, hauteur_obstacle = TAILLE_VOITURE

largeur_ligne = 7
hauteur_pointille = 38
espace_pointille = 28

NOMBRE_ARBRES = 7


# --------------------------------------------------------------
# 3. FONCTIONS DE CRÉATION / RÉINITIALISATION DE LA PARTIE
# --------------------------------------------------------------
def image_aleatoire_obstacle():
    return random.choice(images_obstacles) if images_obstacles else None


def creer_obstacle(y=None):
    x_min = BORD_ROUTE + LARGEUR_BANDE_URGENCE + 8
    x_max = BORD_ROUTE + LARGEUR_ROUTE - LARGEUR_BANDE_URGENCE - largeur_obstacle - 8
    x = random.randint(x_min, x_max)
    if y is None:
        y = -hauteur_obstacle - random.randint(0, 300)
    return {
        "rect": pygame.Rect(x, y, largeur_obstacle, hauteur_obstacle),
        "x_base": x,
        "phase": random.uniform(0, math.tau),
        "couleur": random.choice(COULEURS_VOITURES),
        "image": image_aleatoire_obstacle(),
    }


def creer_arbres():
    arbres = []
    for i in range(NOMBRE_ARBRES):
        cote_gauche = (i % 2 == 0)
        if cote_gauche:
            x = random.randint(18, BORD_ROUTE - 30)
        else:
            x = random.randint(BORD_ROUTE + LARGEUR_ROUTE + 12, LARGEUR_FENETRE - 32)
        y = int(i * (HAUTEUR_FENETRE / NOMBRE_ARBRES)) + random.randint(-20, 20)
        arbres.append({"x": x, "y": y, "echelle": random.uniform(0.8, 1.25),
                        "cote": "gauche" if cote_gauche else "droite"})
    return arbres


def nouvelle_partie():
    """Réinitialise toutes les variables du jeu dans un seul dictionnaire,
    pour pouvoir relancer une partie facilement après un Game Over."""
    voiture_joueur = pygame.Rect(
        LARGEUR_FENETRE // 2 - largeur_voiture // 2,
        HAUTEUR_FENETRE - 160,
        largeur_voiture,
        hauteur_voiture,
    )
    return {
        "voiture_joueur": voiture_joueur,
        "obstacles": [creer_obstacle(y=-200), creer_obstacle(y=-500), creer_obstacle(y=-800)],
        "arbres": creer_arbres(),
        "positions_lignes": list(range(0, HAUTEUR_FENETRE, hauteur_pointille + espace_pointille)),
        "particules": [],
        "score": 0,
        "vitesse_defilement": VITESSE_DEFILEMENT_INITIALE,
        "game_over": False,
        "compteur_frames": 0,
        "flash_collision": 0,  # nombre d'images restantes pour l'effet de flash rouge
    }


# --------------------------------------------------------------
# 4. FONCTIONS DE MISE À JOUR (LOGIQUE DU JEU)
# --------------------------------------------------------------
def gerer_clavier(etat):
    """Déplace la voiture à gauche/droite, et fait accélérer/freiner
    avec les flèches haut/bas. La vitesse revient ensuite doucement
    vers sa valeur initiale (un peu comme un régulateur de vitesse)."""
    touches = pygame.key.get_pressed()
    voiture = etat["voiture_joueur"]

    if touches[pygame.K_LEFT] or touches[pygame.K_q] or touches[pygame.K_a]:
        voiture.x -= VITESSE_VOITURE_JOUEUR
    if touches[pygame.K_RIGHT] or touches[pygame.K_d]:
        voiture.x += VITESSE_VOITURE_JOUEUR

    x_min = BORD_ROUTE + LARGEUR_BANDE_URGENCE + 4
    x_max = BORD_ROUTE + LARGEUR_ROUTE - LARGEUR_BANDE_URGENCE - voiture.width - 4
    voiture.x = max(x_min, min(x_max, voiture.x))

    if touches[pygame.K_UP] or touches[pygame.K_z] or touches[pygame.K_w]:
        etat["vitesse_defilement"] = min(VITESSE_DEFILEMENT_MAX, etat["vitesse_defilement"] + ACCELERATION_PAR_FRAME)
    elif touches[pygame.K_DOWN] or touches[pygame.K_s]:
        etat["vitesse_defilement"] = max(VITESSE_DEFILEMENT_MIN, etat["vitesse_defilement"] - FREINAGE_PAR_FRAME)
    else:
        # ralentissement naturel vers la vitesse de croisière
        if etat["vitesse_defilement"] > VITESSE_DEFILEMENT_INITIALE:
            etat["vitesse_defilement"] -= RALENTISSEMENT_NATUREL
        elif etat["vitesse_defilement"] < VITESSE_DEFILEMENT_INITIALE:
            etat["vitesse_defilement"] += RALENTISSEMENT_NATUREL


def deplacer_decor(etat):
    vitesse = etat["vitesse_defilement"]

    positions_lignes = etat["positions_lignes"]
    for i in range(len(positions_lignes)):
        positions_lignes[i] += vitesse
        if positions_lignes[i] > HAUTEUR_FENETRE:
            positions_lignes[i] -= HAUTEUR_FENETRE + hauteur_pointille + espace_pointille

    for arbre in etat["arbres"]:
        arbre["y"] += vitesse
        if arbre["y"] > HAUTEUR_FENETRE + 30:
            arbre["y"] = -30
            if arbre["cote"] == "gauche":
                arbre["x"] = random.randint(18, BORD_ROUTE - 30)
            else:
                arbre["x"] = random.randint(BORD_ROUTE + LARGEUR_ROUTE + 12, LARGEUR_FENETRE - 32)
            arbre["echelle"] = random.uniform(0.8, 1.25)


def deplacer_obstacles_et_compter_points(etat):
    """Fait descendre les obstacles (avec leur léger balancement). Quand
    un obstacle sort de l'écran (= évité avec succès), on le recycle en
    haut et on donne un bonus de points."""
    vitesse = etat["vitesse_defilement"]
    x_min = BORD_ROUTE + LARGEUR_BANDE_URGENCE + 8
    x_max = BORD_ROUTE + LARGEUR_ROUTE - LARGEUR_BANDE_URGENCE - largeur_obstacle - 8

    for i in range(len(etat["obstacles"])):
        obstacle = etat["obstacles"][i]
        obstacle["rect"].y += vitesse

        balancement = math.sin(pygame.time.get_ticks() / 400 + obstacle["phase"]) * 18
        nouveau_x = obstacle["x_base"] + balancement
        obstacle["rect"].x = int(max(x_min, min(x_max, nouveau_x)))

        if obstacle["rect"].y > HAUTEUR_FENETRE:
            etat["obstacles"][i] = creer_obstacle(y=-hauteur_obstacle)
            etat["score"] += 5  # bonus pour avoir évité l'obstacle


def emettre_particule(etat):
    voiture = etat["voiture_joueur"]
    x = voiture.centerx + random.randint(-14, 14)
    y = voiture.bottom + random.randint(0, 6)
    etat["particules"].append({"x": x, "y": y, "vie": 18})


def mettre_a_jour_particules(etat):
    for particule in etat["particules"]:
        particule["y"] += 2
        particule["vie"] -= 1
    etat["particules"][:] = [p for p in etat["particules"] if p["vie"] > 0]


def detecter_collision(etat):
    """Vérifie si la voiture du joueur touche un obstacle. Si oui, on
    déclenche le Game Over ET un court flash rouge à l'écran, pour que
    l'impact se sente davantage."""
    voiture = etat["voiture_joueur"]
    for obstacle in etat["obstacles"]:
        if voiture.colliderect(obstacle["rect"]):
            etat["game_over"] = True
            etat["flash_collision"] = 10  # durée du flash, en images


def mettre_a_jour_score_et_difficulte(etat):
    etat["compteur_frames"] += 1
    if etat["compteur_frames"] % 10 == 0:
        etat["score"] += 1


# --------------------------------------------------------------
# 5. FONCTIONS DE DESSIN
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


def dessiner_lignes_centrales(surface, positions_lignes):
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


def dessiner_particules(surface, particules):
    for particule in particules:
        opacite = max(0, min(255, particule["vie"] * 12))
        rayon = 3 + (18 - particule["vie"]) // 6
        nuage = pygame.Surface((rayon * 2, rayon * 2), pygame.SRCALPHA)
        pygame.draw.circle(nuage, (210, 210, 200, opacite), (rayon, rayon), rayon)
        surface.blit(nuage, (particule["x"] - rayon, particule["y"] - rayon))


def dessiner_score_et_vitesse(surface, valeur_score, vitesse):
    texte = police.render(f"Score : {valeur_score}", True, COULEUR_TEXTE)
    cadre = pygame.Surface((texte.get_width() + 24, texte.get_height() + 14), pygame.SRCALPHA)
    pygame.draw.rect(cadre, (0, 0, 0, 120), cadre.get_rect(), border_radius=10)
    surface.blit(cadre, (14, 14))
    surface.blit(texte, (14 + 12, 14 + 7))

    # petite jauge de vitesse, en haut à droite
    largeur_jauge = 140
    hauteur_jauge = 16
    x_jauge = LARGEUR_FENETRE - largeur_jauge - 14
    y_jauge = 18
    proportion = (vitesse - VITESSE_DEFILEMENT_MIN) / (VITESSE_DEFILEMENT_MAX - VITESSE_DEFILEMENT_MIN)
    proportion = max(0.0, min(1.0, proportion))

    fond_jauge = pygame.Surface((largeur_jauge, hauteur_jauge), pygame.SRCALPHA)
    pygame.draw.rect(fond_jauge, (0, 0, 0, 120), fond_jauge.get_rect(), border_radius=8)
    surface.blit(fond_jauge, (x_jauge, y_jauge))
    pygame.draw.rect(surface, (235, 200, 40), (x_jauge + 2, y_jauge + 2, int((largeur_jauge - 4) * proportion), hauteur_jauge - 4), border_radius=6)


def dessiner_game_over(surface, valeur_score):
    calque = pygame.Surface((LARGEUR_FENETRE, HAUTEUR_FENETRE), pygame.SRCALPHA)
    calque.fill((0, 0, 0, 180))
    surface.blit(calque, (0, 0))

    titre = police_titre.render("GAME OVER", True, COULEUR_GAME_OVER)
    surface.blit(titre, titre.get_rect(center=(LARGEUR_FENETRE // 2, 300)))

    score_final = police.render(f"Score final : {valeur_score}", True, COULEUR_TEXTE)
    surface.blit(score_final, score_final.get_rect(center=(LARGEUR_FENETRE // 2, 380)))

    rejouer = police.render("Appuyez sur ESPACE pour rejouer", True, COULEUR_TEXTE)
    surface.blit(rejouer, rejouer.get_rect(center=(LARGEUR_FENETRE // 2, 440)))


def dessiner_flash_collision(surface, intensite):
    """Un voile rouge semi-transparent, plus fort juste après l'impact
    puis qui s'estompe -- ça donne un vrai "ressenti" de choc."""
    if intensite <= 0:
        return
    opacite = int(160 * (intensite / 10))
    flash = pygame.Surface((LARGEUR_FENETRE, HAUTEUR_FENETRE), pygame.SRCALPHA)
    flash.fill((200, 0, 0, opacite))
    surface.blit(flash, (0, 0))


# --------------------------------------------------------------
# 6. BOUCLE PRINCIPALE
# --------------------------------------------------------------
horloge = pygame.time.Clock()
etat = nouvelle_partie()
en_cours = True

while en_cours:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False
        if evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_SPACE and etat["game_over"]:
                etat = nouvelle_partie()

    if not etat["game_over"]:
        gerer_clavier(etat)
        deplacer_decor(etat)
        deplacer_obstacles_et_compter_points(etat)
        mettre_a_jour_score_et_difficulte(etat)

        # On émet une particule de poussière environ toutes les 3 images
        if etat["compteur_frames"] % 3 == 0:
            emettre_particule(etat)
        mettre_a_jour_particules(etat)

        detecter_collision(etat)
    elif etat["flash_collision"] > 0:
        etat["flash_collision"] -= 1

    # --- Affichage ---
    dessiner_fond_et_route(fenetre)
    for arbre in etat["arbres"]:
        dessiner_arbre(fenetre, arbre["x"], arbre["y"], arbre["echelle"], image_arbre)
    dessiner_lignes_centrales(fenetre, etat["positions_lignes"])
    dessiner_particules(fenetre, etat["particules"])

    for obstacle in etat["obstacles"]:
        dessiner_voiture(fenetre, obstacle["rect"], obstacle["couleur"], obstacle["image"])

    dessiner_voiture(fenetre, etat["voiture_joueur"], COULEUR_VOITURE_JOUEUR, image_voiture_joueur)
    dessiner_score_et_vitesse(fenetre, etat["score"], etat["vitesse_defilement"])

    if etat["flash_collision"] > 0:
        dessiner_flash_collision(fenetre, etat["flash_collision"])

    if etat["game_over"]:
        dessiner_game_over(fenetre, etat["score"])

    pygame.display.flip()
    horloge.tick(60)

pygame.quit()
