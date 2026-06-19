"""
====================================================================
ÉTAPE 3 : GÉRER LES ÉVÉNEMENTS
====================================================================

C'est la dernière étape, celle qui transforme notre belle animation
(étape 2) en un VRAI jeu vidéo : le joueur doit pouvoir agir, et
le jeu doit réagir à ses actions.

On va ajouter :
    1. Le contrôle de la voiture avec les flèches gauche/droite du
       clavier (et haut/bas en bonus pour accélérer/freiner)
    2. La détection de collision entre la voiture du joueur et les
       obstacles
    3. Le gain de points au fil du temps (et un bonus quand on évite
       un obstacle)
    4. Un écran de "Game Over" quand on percute un obstacle, avec
       la possibilité de relancer une partie en appuyant sur ESPACE

C'est le fichier final : vous pouvez le lancer et JOUER !
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
COULEUR_GAME_OVER = (255, 60, 60)

VITESSE_DEFILEMENT_INITIALE = 6
VITESSE_VOITURE_JOUEUR = 8  # déplacement horizontal en pixels par frame

fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
pygame.display.set_caption("Mon Jeu de Course - Étape 3 : Le Jeu Complet")

police = pygame.font.SysFont("Arial", 32, bold=True)
police_titre = pygame.font.SysFont("Arial", 56, bold=True)

largeur_voiture = 50
hauteur_voiture = 90
largeur_obstacle = 50
hauteur_obstacle = 90

largeur_ligne = 8
hauteur_pointille = 40
espace_pointille = 30


# --------------------------------------------------------------
# 3. FONCTIONS UTILITAIRES POUR CRÉER/RÉINITIALISER LE JEU
# --------------------------------------------------------------
def creer_obstacle(y=None):
    """Crée un obstacle à une position X aléatoire sur la route."""
    x_min = BORD_ROUTE + 10
    x_max = BORD_ROUTE + LARGEUR_ROUTE - largeur_obstacle - 10
    x = random.randint(x_min, x_max)
    if y is None:
        y = -hauteur_obstacle - random.randint(0, 300)
    return pygame.Rect(x, y, largeur_obstacle, hauteur_obstacle)


def nouvelle_partie():
    """
    Réinitialise toutes les variables du jeu.
    On utilise cette fonction au démarrage ET chaque fois que le
    joueur relance une partie après un Game Over : ça évite de
    dupliquer le code de réinitialisation.
    Elle renvoie un dictionnaire contenant tout l'état du jeu.
    """
    voiture_joueur = pygame.Rect(
        LARGEUR_FENETRE // 2 - largeur_voiture // 2,
        HAUTEUR_FENETRE - 150,
        largeur_voiture,
        hauteur_voiture
    )

    obstacles = [creer_obstacle(y=-200), creer_obstacle(y=-500), creer_obstacle(y=-800)]

    positions_lignes = list(range(0, HAUTEUR_FENETRE, hauteur_pointille + espace_pointille))

    return {
        "voiture_joueur": voiture_joueur,
        "obstacles": obstacles,
        "positions_lignes": positions_lignes,
        "score": 0,
        "vitesse_defilement": VITESSE_DEFILEMENT_INITIALE,
        "game_over": False,
        # compteur de frames, utilisé pour donner 1 point toutes les
        # quelques frames (plutôt qu'à chaque frame, sinon le score
        # grimperait beaucoup trop vite)
        "compteur_frames": 0,
    }


# --------------------------------------------------------------
# 4. FONCTIONS DE MISE À JOUR (LOGIQUE DU JEU)
# --------------------------------------------------------------
def gerer_clavier(etat):
    """
    Lit l'état actuel du clavier et déplace la voiture du joueur.

    pygame.key.get_pressed() renvoie la liste de TOUTES les touches,
    avec True/False selon qu'elles sont enfoncées. C'est différent
    de pygame.event.get() : ici on sait si une touche est *maintenue*
    enfoncée, pas seulement si elle vient d'être appuyée.
    """
    touches = pygame.key.get_pressed()
    voiture = etat["voiture_joueur"]

    if touches[pygame.K_LEFT] or touches[pygame.K_q] or touches[pygame.K_a]:
        voiture.x -= VITESSE_VOITURE_JOUEUR
    if touches[pygame.K_RIGHT] or touches[pygame.K_d]:
        voiture.x += VITESSE_VOITURE_JOUEUR

    # On empêche la voiture de sortir de la route (limites gauche/droite)
    voiture.x = max(BORD_ROUTE + 5, voiture.x)
    voiture.x = min(BORD_ROUTE + LARGEUR_ROUTE - voiture.width - 5, voiture.x)


def deplacer_decor(etat):
    """Fait défiler les lignes de la route vers le bas."""
    vitesse = etat["vitesse_defilement"]
    positions_lignes = etat["positions_lignes"]

    for i in range(len(positions_lignes)):
        positions_lignes[i] += vitesse
        if positions_lignes[i] > HAUTEUR_FENETRE:
            positions_lignes[i] -= HAUTEUR_FENETRE + hauteur_pointille + espace_pointille


def deplacer_obstacles_et_compter_points(etat):
    """
    Fait descendre les obstacles. Quand un obstacle sort de l'écran
    par le bas (= le joueur l'a évité avec succès), on :
        - le replace en haut avec une nouvelle position X
        - donne 5 points bonus au joueur
    """
    vitesse = etat["vitesse_defilement"]
    obstacles = etat["obstacles"]

    for i in range(len(obstacles)):
        obstacles[i].y += vitesse
        if obstacles[i].y > HAUTEUR_FENETRE:
            obstacles[i] = creer_obstacle(y=-hauteur_obstacle)
            etat["score"] += 5  # bonus pour avoir évité l'obstacle


def detecter_collision(etat):
    """
    Vérifie si la voiture du joueur touche un obstacle.

    pygame.Rect.colliderect() renvoie True si deux rectangles se
    superposent, peu importe leur forme exacte. C'est la méthode la
    plus simple pour détecter une collision entre deux objets en
    Pygame.
    """
    voiture = etat["voiture_joueur"]
    for obstacle in etat["obstacles"]:
        if voiture.colliderect(obstacle):
            etat["game_over"] = True


def mettre_a_jour_score_et_difficulte(etat):
    """
    Ajoute régulièrement des points juste pour avoir survécu, et
    augmente très progressivement la vitesse du jeu : plus la
    partie dure, plus c'est difficile !
    """
    etat["compteur_frames"] += 1

    # +1 point toutes les 10 frames (≈ 6 fois par seconde à 60 FPS)
    if etat["compteur_frames"] % 10 == 0:
        etat["score"] += 1

    # Accélération très légère et progressive
    etat["vitesse_defilement"] += 0.002


# --------------------------------------------------------------
# 5. FONCTIONS DE DESSIN (AFFICHAGE)
# --------------------------------------------------------------
def dessiner_route(surface, positions_lignes):
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


def dessiner_game_over(surface, valeur_score):
    """
    Affiche un écran de fin de partie semi-transparent par-dessus
    le jeu, avec le score final et l'invite à rejouer.
    """
    # Un calque sombre semi-transparent par-dessus tout le jeu
    calque = pygame.Surface((LARGEUR_FENETRE, HAUTEUR_FENETRE))
    calque.set_alpha(180)  # 0 = invisible, 255 = totalement opaque
    calque.fill((0, 0, 0))
    surface.blit(calque, (0, 0))

    titre = police_titre.render("GAME OVER", True, COULEUR_GAME_OVER)
    surface.blit(titre, titre.get_rect(center=(LARGEUR_FENETRE // 2, 300)))

    score_final = police.render(f"Score final : {valeur_score}", True, COULEUR_TEXTE)
    surface.blit(score_final, score_final.get_rect(center=(LARGEUR_FENETRE // 2, 380)))

    rejouer = police.render("Appuyez sur ESPACE pour rejouer", True, COULEUR_TEXTE)
    surface.blit(rejouer, rejouer.get_rect(center=(LARGEUR_FENETRE // 2, 440)))


# --------------------------------------------------------------
# 6. BOUCLE PRINCIPALE
# --------------------------------------------------------------
horloge = pygame.time.Clock()
etat = nouvelle_partie()
en_cours = True

while en_cours:
    # --- 1. Gestion des événements ---
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False

        # On ne relance une partie QUE si le jeu est en Game Over
        # ET que le joueur appuie sur la touche ESPACE.
        if evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_SPACE and etat["game_over"]:
                etat = nouvelle_partie()

    # --- 2. Logique du jeu (seulement si la partie n'est pas finie) ---
    if not etat["game_over"]:
        gerer_clavier(etat)
        deplacer_decor(etat)
        deplacer_obstacles_et_compter_points(etat)
        mettre_a_jour_score_et_difficulte(etat)
        detecter_collision(etat)

    # --- 3. Affichage ---
    dessiner_route(fenetre, etat["positions_lignes"])
    dessiner_obstacles(fenetre, etat["obstacles"])
    dessiner_voiture_joueur(fenetre, etat["voiture_joueur"])
    dessiner_score(fenetre, etat["score"])

    if etat["game_over"]:
        dessiner_game_over(fenetre, etat["score"])

    pygame.display.flip()
    horloge.tick(60)

pygame.quit()
