"""
====================================================================
ÉTAPE 2 : AJOUTER LES ANIMATIONS
====================================================================

Maintenant que le décor est posé (étape 1), on va lui donner vie !

Au cinéma, une animation n'est qu'une succession rapide d'images
fixes légèrement différentes. Dans un jeu vidéo, c'est exactement
la même chose : à chaque tour de la boucle de jeu, on déplace un
peu les objets, puis on redessine l'écran. Fait 60 fois par
seconde, l'œil humain perçoit ça comme un mouvement fluide.

Dans cette étape, on va :
    1. Faire défiler la route vers le bas (sensation d'avancer)
    2. Faire descendre les obstacles
    3. Faire réapparaître un obstacle en haut quand il sort de l'écran
       en bas (pour ne jamais en manquer)
    4. Donner une sensation de vitesse grâce à la vitesse de défilement

Le joueur ne peut toujours pas contrôler sa voiture : ce sera
l'objet de l'étape 3.
====================================================================
"""

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

LARGEUR_ROUTE = 400
BORD_ROUTE = (LARGEUR_FENETRE - LARGEUR_ROUTE) // 2

COULEUR_GAZON = (34, 139, 34)
COULEUR_ROUTE = (50, 50, 50)
COULEUR_LIGNE = (255, 255, 255)
COULEUR_VOITURE_JOUEUR = (220, 30, 30)
COULEUR_OBSTACLE = (30, 60, 220)
COULEUR_TEXTE = (255, 255, 255)

# Vitesse de défilement : plus ce nombre est grand, plus on a
# l'impression d'aller vite. On pourra l'augmenter au fil du temps
# pour simuler une accélération.
VITESSE_DEFILEMENT = 6

fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
pygame.display.set_caption("Mon Jeu de Course - Étape 2 : Les Animations")

# --------------------------------------------------------------
# 3. LA VOITURE DU JOUEUR (toujours statique pour l'instant)
# --------------------------------------------------------------
largeur_voiture = 50
hauteur_voiture = 90

voiture_joueur = pygame.Rect(
    LARGEUR_FENETRE // 2 - largeur_voiture // 2,
    HAUTEUR_FENETRE - 150,
    largeur_voiture,
    hauteur_voiture
)

# --------------------------------------------------------------
# 4. LES LIGNES DE LA ROUTE (objets animés)
# --------------------------------------------------------------
# Contrairement à l'étape 1 où les lignes étaient dessinées "en dur"
# dans une boucle, on les stocke maintenant dans une LISTE de
# positions Y, pour pouvoir les faire bouger facilement.
largeur_ligne = 8
hauteur_pointille = 40
espace_pointille = 30

positions_lignes = list(range(0, HAUTEUR_FENETRE, hauteur_pointille + espace_pointille))


def deplacer_lignes():
    """Fait descendre chaque ligne, et la replace en haut si elle sort de l'écran."""
    for i in range(len(positions_lignes)):
        positions_lignes[i] += VITESSE_DEFILEMENT
        # Si la ligne est sortie en bas de l'écran, on la "recycle"
        # en la replaçant juste au-dessus de l'écran.
        if positions_lignes[i] > HAUTEUR_FENETRE:
            positions_lignes[i] -= HAUTEUR_FENETRE + hauteur_pointille + espace_pointille


# --------------------------------------------------------------
# 5. LES OBSTACLES (animés : ils descendent)
# --------------------------------------------------------------
largeur_obstacle = 50
hauteur_obstacle = 90


def creer_obstacle(y=None):
    """
    Crée un nouvel obstacle à une position X aléatoire sur la route.
    Si y n'est pas précisé, on le place au-dessus de l'écran (hors
    champ de vision), prêt à apparaître en descendant.
    """
    x_min = BORD_ROUTE + 10
    x_max = BORD_ROUTE + LARGEUR_ROUTE - largeur_obstacle - 10
    x = random.randint(x_min, x_max)
    if y is None:
        y = -hauteur_obstacle - random.randint(0, 300)  # un peu d'aléatoire
    return pygame.Rect(x, y, largeur_obstacle, hauteur_obstacle)


# On démarre avec 3 obstacles, échelonnés sur la hauteur de l'écran.
obstacles = [creer_obstacle(y=-200), creer_obstacle(y=-500), creer_obstacle(y=-800)]


def deplacer_obstacles():
    """Fait descendre chaque obstacle. Si un obstacle sort en bas de
    l'écran, on le replace en haut avec une nouvelle position X
    aléatoire : c'est ce qui donne l'impression d'un flot continu
    de voitures qui arrivent."""
    for i in range(len(obstacles)):
        obstacles[i].y += VITESSE_DEFILEMENT
        if obstacles[i].y > HAUTEUR_FENETRE:
            obstacles[i] = creer_obstacle(y=-hauteur_obstacle)


# --------------------------------------------------------------
# 6. SCORE (toujours figé, ce sera pour l'étape 3)
# --------------------------------------------------------------
score = 0
police = pygame.font.SysFont("Arial", 32, bold=True)


# --------------------------------------------------------------
# 7. FONCTIONS DE DESSIN
# --------------------------------------------------------------
def dessiner_route(surface):
    """Dessine le gazon, la route, et les lignes (à leur position animée)."""
    surface.fill(COULEUR_GAZON)

    route_rect = pygame.Rect(BORD_ROUTE, 0, LARGEUR_ROUTE, HAUTEUR_FENETRE)
    pygame.draw.rect(surface, COULEUR_ROUTE, route_rect)

    x_ligne = LARGEUR_FENETRE // 2 - largeur_ligne // 2
    for y in positions_lignes:
        pygame.draw.rect(surface, COULEUR_LIGNE, (x_ligne, y, largeur_ligne, hauteur_pointille))


def dessiner_voiture_joueur(surface, rect):
    pygame.draw.rect(surface, COULEUR_VOITURE_JOUEUR, rect, border_radius=8)
    pare_brise = pygame.Rect(rect.x + 8, rect.y + 12, rect.width - 16, 20)
    pygame.draw.rect(surface, (20, 20, 20), pare_brise, border_radius=4)


def dessiner_obstacles(surface, liste_obstacles):
    for obstacle in liste_obstacles:
        pygame.draw.rect(surface, COULEUR_OBSTACLE, obstacle, border_radius=8)


def dessiner_score(surface, valeur_score):
    texte = police.render(f"Score : {valeur_score}", True, COULEUR_TEXTE)
    surface.blit(texte, (20, 20))


# --------------------------------------------------------------
# 8. BOUCLE PRINCIPALE
# --------------------------------------------------------------
horloge = pygame.time.Clock()
en_cours = True

while en_cours:
    # --- 1. Événements ---
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False

    # --- 2. Logique / animation ---
    # C'est ICI que la magie de l'étape 2 se joue : on met à jour
    # les positions AVANT de redessiner l'écran.
    deplacer_lignes()
    deplacer_obstacles()

    # Petite astuce : on augmente très légèrement la vitesse au fil
    # du temps pour donner une sensation de jeu qui s'accélère.
    # (décommentez la ligne suivante pour essayer !)
    # VITESSE_DEFILEMENT += 0.001

    # --- 3. Affichage ---
    dessiner_route(fenetre)
    dessiner_obstacles(fenetre, obstacles)
    dessiner_voiture_joueur(fenetre, voiture_joueur)
    dessiner_score(fenetre, score)

    pygame.display.flip()
    horloge.tick(60)

pygame.quit()
