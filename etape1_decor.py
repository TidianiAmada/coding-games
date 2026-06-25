"""
====================================================================
ÉTAPE 1 : CRÉER LE DÉCOR
====================================================================

Dans cette première étape, on ne fait AUCUNE animation.
On se contente de "planter le décor", comme un réalisateur qui
installe ses meubles sur un plateau de tournage avant de tourner
la scène.

On va dessiner :
    1. La route (avec ses bords et ses lignes blanches)
    2. La voiture du joueur (en bas de l'écran)
    3. Quelques obstacles (d'autres voitures, immobiles pour l'instant)
    4. Le score (toujours à 0 pour le moment)

Rien ne bouge encore : c'est normal ! On ajoutera le mouvement
à l'étape 2, puis les contrôles du joueur à l'étape 3.
====================================================================
"""

import pygame

# --------------------------------------------------------------
# 1. INITIALISATION DE PYGAME
# --------------------------------------------------------------
# pygame.init() démarre tous les modules internes de Pygame
# (affichage, son, clavier, etc.). C'est TOUJOURS la première
# ligne à écrire dans un programme Pygame.
pygame.init()

# --------------------------------------------------------------
# 2. CONSTANTES (des valeurs qui ne changeront pas)
# --------------------------------------------------------------
# On les écrit en MAJUSCULES par convention.
LARGEUR_FENETRE = 600
HAUTEUR_FENETRE = 600

# Largeur de la route (elle sera centrée sur l'écran)
LARGEUR_ROUTE = 400 
BORD_ROUTE = (LARGEUR_FENETRE - LARGEUR_ROUTE) // 2  # marge de chaque côté

# Couleurs au format RGB (Rouge, Vert, Bleu) de 0 à 255
COULEUR_GAZON = (34, 139, 34)      # vert
COULEUR_ROUTE = (50, 50, 50)       # gris foncé
COULEUR_LIGNE = (255, 255, 255)    # blanc
COULEUR_VOITURE_JOUEUR = (220, 30, 30)   # rouge
COULEUR_OBSTACLE = (30, 60, 220)         # bleu
COULEUR_TEXTE = (255, 255, 255)          # blanc

# --------------------------------------------------------------
# 3. CRÉATION DE LA FENÊTRE
# --------------------------------------------------------------
# pygame.display.set_mode() crée la fenêtre du jeu et renvoie
# une "surface" : c'est la zone sur laquelle on va dessiner.
fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
pygame.display.set_caption("Mon Jeu de Course - Étape 1 : Le Décor")

# --------------------------------------------------------------
# 4. LA VOITURE DU JOUEUR
# --------------------------------------------------------------
# On représente la voiture par un simple rectangle pour commencer.
# pygame.Rect(x, y, largeur, hauteur)
# x, y = coin supérieur gauche du rectangle
largeur_voiture = 50
hauteur_voiture = 90

voiture_joueur = pygame.Rect(
    LARGEUR_FENETRE // 2 - largeur_voiture // 2,  # centrée horizontalement
    HAUTEUR_FENETRE - 150,                        # proche du bas de l'écran
    largeur_voiture,
    hauteur_voiture
)

# --------------------------------------------------------------
# 5. LES OBSTACLES (autres voitures, immobiles pour l'instant)
# --------------------------------------------------------------
# On stocke chaque obstacle dans une liste de rectangles.
# À l'étape 2, ces rectangles se déplaceront vers le bas.
largeur_obstacle = 50
hauteur_obstacle = 90

obstacles = [
    pygame.Rect(BORD_ROUTE + 30, 150, largeur_obstacle, hauteur_obstacle),
    pygame.Rect(BORD_ROUTE + 250, 350, largeur_obstacle, hauteur_obstacle),
    pygame.Rect(BORD_ROUTE + 130, 550, largeur_obstacle, hauteur_obstacle),
]

# --------------------------------------------------------------
# 6. LE SCORE
# --------------------------------------------------------------
score = 0  # pour l'instant il ne bougera pas, ce sera pour l'étape 3

# pygame.font sert à afficher du texte. On choisit une police
# système et une taille en pixels.
police = pygame.font.SysFont("Arial", 32, bold=True)


def dessiner_route(surface):
    """
    Dessine le gazon, la route et les lignes blanches au centre.
    On regroupe ce code dans une fonction pour que le code principal
    (la boucle de jeu) reste lisible.
    """
    # Le gazon recouvre tout l'écran
    surface.fill(COULEUR_GAZON)

    # La route est un grand rectangle gris au centre de l'écran
    route_rect = pygame.Rect(BORD_ROUTE, 0, LARGEUR_ROUTE, HAUTEUR_FENETRE)
    pygame.draw.rect(surface, COULEUR_ROUTE, route_rect)

    # La ligne blanche centrale, en pointillés
    # On dessine une série de petits rectangles verticaux espacés.
    largeur_ligne = 8
    hauteur_pointille = 40
    espace = 30
    x_ligne = LARGEUR_FENETRE // 2 - largeur_ligne // 2

    y = 0
    while y < HAUTEUR_FENETRE:
        pygame.draw.rect(
            surface,
            COULEUR_LIGNE,
            (x_ligne, y, largeur_ligne, hauteur_pointille)
        )
        y += hauteur_pointille + espace


def dessiner_voiture_joueur(surface, rect):
    """Dessine la voiture du joueur (un simple rectangle rouge + détails)."""
    pygame.draw.rect(surface, COULEUR_VOITURE_JOUEUR, rect, border_radius=8)
    # On ajoute deux petits rectangles noirs pour simuler le pare-brise
    pare_brise = pygame.Rect(rect.x + 8, rect.y + 12, rect.width - 16, 20)
    pygame.draw.rect(surface, (20, 20, 20), pare_brise, border_radius=4)


def dessiner_obstacles(surface, liste_obstacles):
    """Dessine chaque obstacle (voiture adverse) de la liste."""
    for obstacle in liste_obstacles:
        pygame.draw.rect(surface, COULEUR_OBSTACLE, obstacle, border_radius=8)


def dessiner_score(surface, valeur_score):
    """Affiche le score en haut à gauche de l'écran."""
    texte = police.render(f"Score : {valeur_score}", True, COULEUR_TEXTE)
    surface.blit(texte, (20, 20))


# --------------------------------------------------------------
# 7. BOUCLE PRINCIPALE DU JEU
# --------------------------------------------------------------
# Une boucle de jeu tourne en continu, plusieurs dizaines de fois
# par seconde. À chaque tour, on :
#   1. lit les événements (fermeture de fenêtre, clavier...)
#   2. met à jour la logique du jeu (rien à mettre à jour ici)
#   3. redessine tout l'écran
horloge = pygame.time.Clock()
en_cours = True

while en_cours:
    # --- 1. Gestion des événements ---
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False

    # --- 2. Logique du jeu ---
    # (vide pour l'instant : rien ne bouge à l'étape 1)

    # --- 3. Affichage (on redessine tout, dans l'ordre) ---
    dessiner_route(fenetre)
    dessiner_obstacles(fenetre, obstacles)
    dessiner_voiture_joueur(fenetre, voiture_joueur)
    dessiner_score(fenetre, score)

    # pygame.display.flip() affiche réellement tout ce qu'on a dessiné.
    # Sans cette ligne, l'écran resterait noir !
    pygame.display.flip()

    # On limite le jeu à 60 images par seconde (60 FPS).
    horloge.tick(60)

# --------------------------------------------------------------
# 8. FERMETURE PROPRE DU JEU
# --------------------------------------------------------------
pygame.quit()
