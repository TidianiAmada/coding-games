"""
====================================================================
06_zoom_evenements_et_regles.py
====================================================================
C'est cette partie qui transforme une simple animation en véritable
jeu vidéo : le joueur doit pouvoir AGIR, et le jeu doit RÉAGIR.

On va illustrer trois règles essentielles :
   1. Le clavier déplace la voiture
   2. La collision décide si la partie continue ou s'arrête
   3. Le score récompense le joueur qui évite les obstacles

Lancez ce fichier avec :   python3 06_zoom_evenements_et_regles.py
====================================================================
"""

import utils_affichage as ui
from utils_affichage import CARACTERE_VOITURE, CARACTERE_OBSTACLE, CARACTERE_COLLISION


def section(titre):
    print("\n" + "=" * 60)
    print(titre)
    print("=" * 60)


# --------------------------------------------------------------
# 1. LE CLAVIER
# --------------------------------------------------------------
section("1. Le clavier")

print("""
Dans le vrai jeu, pygame.key.get_pressed() nous dit quelles
touches sont actuellement enfoncées. Ici, on simule une touche
avec un simple texte ("GAUCHE", "DROITE") pour comprendre la
logique sans avoir besoin d'un vrai clavier de jeu.
""")


def deplacer_voiture(x, touche, vitesse=1, x_min=0, x_max=ui.LARGEUR_ROUTE - 1):
    """
    Simule ce que fait gerer_clavier() dans le vrai jeu : on reçoit
    la position actuelle x (relative à la route) et la touche
    appuyée, et on renvoie la nouvelle position x.
    """
    if touche == "GAUCHE":
        x -= vitesse
    elif touche == "DROITE":
        x += vitesse

    # on empêche de sortir de la route
    x = max(x_min, min(x_max, x))
    return x


x_voiture = ui.LARGEUR_ROUTE // 2
sequence_touches = ["DROITE", "DROITE", "DROITE", "RIEN", "GAUCHE"]

for touche in sequence_touches:
    x_voiture = deplacer_voiture(x_voiture, touche)
    print(f"Touche appuyée : {touche:<7} -> nouvelle position x (sur la route) = {x_voiture}")


# --------------------------------------------------------------
# 2. LA COLLISION : LA REGLE LA PLUS IMPORTANTE DU JEU
# --------------------------------------------------------------
section("2. La collision : la règle la plus importante du jeu")

print("""
C'est colliderect() (vu dans 03_concepts_pygame.py) qui décide si
la partie continue ou si c'est le Game Over. On réutilise notre
classe MiniRect pour illustrer les deux situations possibles, et
on les affiche en ASCII :
""")


class MiniRect:
    def __init__(self, x, y, largeur, hauteur):
        self.x, self.y, self.largeur, self.hauteur = x, y, largeur, hauteur

    def colliderect(self, autre):
        return (
            self.x < autre.x + autre.largeur
            and self.x + self.largeur > autre.x
            and self.y < autre.y + autre.hauteur
            and self.y + self.hauteur > autre.y
        )


voiture_rect = MiniRect(5, 13, 1, 1)
situations = [
    ("Pas de collision", MiniRect(2, 3, 1, 1)),
    ("COLLISION !", MiniRect(5, 13, 1, 1)),
]

for titre, obstacle_rect in situations:
    en_collision = voiture_rect.colliderect(obstacle_rect)

    grille = ui.construire_grille()
    ui.placer(grille, voiture_rect.x, voiture_rect.y, CARACTERE_VOITURE)
    caractere_obstacle = CARACTERE_COLLISION if en_collision else CARACTERE_OBSTACLE
    ui.placer(grille, obstacle_rect.x, obstacle_rect.y, caractere_obstacle)

    ui.afficher(grille, f"{titre}  (colliderect -> {en_collision})")
    print()


# --------------------------------------------------------------
# 3. LE SCORE : LA RECOMPENSE DU JOUEUR
# --------------------------------------------------------------
section("3. Le score : la récompense du joueur")

print("""
Chaque fois qu'un obstacle est évité avec succès (il sort de
l'écran sans avoir touché la voiture), on ajoute des points. Si
une collision se produit, la partie s'arrête.
""")

score = 0
obstacles_evites = ["obstacle1", "obstacle2", "obstacle3", "obstacle4"]
obstacle_qui_a_touche_la_voiture = "obstacle5"

for obstacle in obstacles_evites:
    score += 5  # +5 points chaque fois qu'on évite un obstacle
    print(f"{obstacle} évité ! Score = {score}")

game_over = True
print(f"\nGAME OVER -> {obstacle_qui_a_touche_la_voiture} a touché la voiture.")
print(f"Score final : {score}")

print("""
On retrouve cette logique presque mot pour mot dans
etape3_evenements.py :

    def deplacer_obstacles_et_compter_points(etat):
        for i in range(len(obstacles)):
            obstacles[i].y += vitesse
            if obstacles[i].y > HAUTEUR_FENETRE:
                obstacles[i] = creer_obstacle(y=-hauteur_obstacle)
                etat["score"] += 5     # bonus pour avoir évité l'obstacle

    def detecter_collision(etat):
        for obstacle in etat["obstacles"]:
            if voiture.colliderect(obstacle):
                etat["game_over"] = True

Passez maintenant au fichier 07_perspectives.py
""")
