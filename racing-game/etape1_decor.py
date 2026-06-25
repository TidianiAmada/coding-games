"""
====================================================================
ÉTAPE 1 : CRÉER LE DÉCOR (VERSION AMÉLIORÉE - DÉCOR RÉALISTE)
====================================================================

Cette version reprend exactement la même logique que la première
version (la route, la voiture, les obstacles, le score), mais avec
un rendu beaucoup plus soigné :

    - une route avec bande d'urgence et ligne jaune continue
    - des arbres décoratifs sur le bas-côté
    - des voitures dessinées en détail (vitres, roues, phares, ombre)
    - la possibilité d'utiliser de VRAIES IMAGES (PNG) si vous en
      ajoutez, sans rien casser si elles sont absentes

------------------------------------------------------------------
COMMENT AJOUTER DE VRAIES IMAGES (recommandé pour un rendu pro) :
------------------------------------------------------------------
1. Créez un dossier "assets" À CÔTÉ de ce fichier .py
2. Téléchargez des icônes "vue de dessus" (top view) de voitures et
   d'arbres sur un site d'icônes/images libres, par exemple :
       - https://www.freepik.com   (filtrez par licence gratuite)
       - https://www.flaticon.com
   Vérifiez toujours la licence affichée sur la page de téléchargement :
   certaines images gratuites demandent de citer l'auteur ("attribution
   required"), d'autres peuvent être utilisées librement. Ne sont
   utilisables sans condition que les images que LA LICENCE autorise
   pour votre usage (perso, scolaire ou commercial selon le cas).
3. Renommez vos fichiers exactement comme ceci et placez-les dans
   "assets/" :
       assets/voiture_joueur.png
       assets/voiture_obstacle_1.png
       assets/voiture_obstacle_2.png
       assets/voiture_obstacle_3.png
       assets/arbre.png
4. Relancez le jeu : si un fichier est trouvé, il est utilisé
   automatiquement à la place du dessin vectoriel. Sinon, le jeu
   continue de fonctionner avec son décor dessiné "à la main".
====================================================================
"""

import os
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
LARGEUR_BANDE_URGENCE = 18  # bande claire le long de chaque bord de route

# Couleurs (R, V, B)
COULEUR_GAZON_1 = (45, 130, 45)
COULEUR_GAZON_2 = (39, 120, 39)     # une 2e nuance pour casser la monotonie
COULEUR_ROUTE = (58, 58, 62)
COULEUR_BANDE_URGENCE = (90, 88, 80)
COULEUR_LIGNE_JAUNE = (235, 195, 40)
COULEUR_LIGNE_BLANCHE = (235, 235, 235)
COULEUR_TEXTE = (255, 255, 255)
COULEUR_OMBRE = (0, 0, 0)

# Quelques couleurs de carrosserie pour varier les voitures
COULEURS_VOITURES = [
    (200, 35, 35),    # rouge
    (35, 90, 200),     # bleu
    (235, 200, 40),    # jaune
    (40, 150, 90),      # vert
    (230, 230, 230),    # blanc/gris clair
]
COULEUR_VOITURE_JOUEUR = (200, 35, 35)

DOSSIER_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
pygame.display.set_caption("Mon Jeu de Course - Étape 1 : Le Décor (version réaliste)")

police = pygame.font.SysFont("Arial", 30, bold=True)
police_petite = pygame.font.SysFont("Arial", 16)


# --------------------------------------------------------------
# 3. CHARGEMENT D'IMAGES OPTIONNEL (ne casse rien si absent)
# --------------------------------------------------------------
def charger_image(nom_fichier, taille=None):
    """
    Essaie de charger une image PNG depuis le dossier 'assets/'.
    - Si le fichier n'existe pas : renvoie None, sans erreur.
    - Si le fichier existe mais est corrompu : prévient gentiment
      et renvoie None aussi.
    Le reste du jeu sait dessiner une version "vectorielle" de secours
    chaque fois que l'image renvoyée est None : on ne casse jamais le jeu.
    """
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


# Tailles cibles, pour que toutes les images (si fournies) aient une
# taille cohérente avec le dessin vectoriel.
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
# 4. LA VOITURE DU JOUEUR
# --------------------------------------------------------------
largeur_voiture, hauteur_voiture = TAILLE_VOITURE

voiture_joueur = pygame.Rect(
    LARGEUR_FENETRE // 2 - largeur_voiture // 2,
    HAUTEUR_FENETRE - 160,
    largeur_voiture,
    hauteur_voiture,
)

# --------------------------------------------------------------
# 5. LES OBSTACLES
# --------------------------------------------------------------
largeur_obstacle, hauteur_obstacle = TAILLE_VOITURE

def image_aleatoire_obstacle():
    """Choisit une image au hasard parmi celles disponibles (ou None s'il
    n'y en a aucune) : appelée UNE SEULE FOIS à la création de chaque
    obstacle, pour qu'il garde toujours la même apparence."""
    return random.choice(images_obstacles) if images_obstacles else None


obstacles = [
    {"rect": pygame.Rect(BORD_ROUTE + 30, 150, largeur_obstacle, hauteur_obstacle),
     "couleur": random.choice(COULEURS_VOITURES), "image": image_aleatoire_obstacle()},
    {"rect": pygame.Rect(BORD_ROUTE + LARGEUR_ROUTE - 90, 350, largeur_obstacle, hauteur_obstacle),
     "couleur": random.choice(COULEURS_VOITURES), "image": image_aleatoire_obstacle()},
    {"rect": pygame.Rect(BORD_ROUTE + 120, 550, largeur_obstacle, hauteur_obstacle),
     "couleur": random.choice(COULEURS_VOITURES), "image": image_aleatoire_obstacle()},
]

# --------------------------------------------------------------
# 6. LES ARBRES DÉCORATIFS (sur le bas-côté, statiques pour l'étape 1)
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

# --------------------------------------------------------------
# 7. SCORE
# --------------------------------------------------------------
score = 0


# --------------------------------------------------------------
# 8. FONCTIONS DE DESSIN DU DÉCOR
# --------------------------------------------------------------
def dessiner_fond_et_route(surface):
    """Dessine le gazon (avec une légère variation de teinte) et la route
    avec ses bandes d'urgence et sa ligne jaune continue."""
    # Le gazon : on alterne 2 nuances de vert par bandes horizontales pour
    # casser l'effet "aplat de couleur unique", beaucoup plus réaliste.
    hauteur_bande = 40
    for y in range(0, HAUTEUR_FENETRE, hauteur_bande):
        couleur = COULEUR_GAZON_1 if (y // hauteur_bande) % 2 == 0 else COULEUR_GAZON_2
        pygame.draw.rect(surface, couleur, (0, y, LARGEUR_FENETRE, hauteur_bande))

    # La route (asphalte)
    pygame.draw.rect(surface, COULEUR_ROUTE, (BORD_ROUTE, 0, LARGEUR_ROUTE, HAUTEUR_FENETRE))

    # Les bandes d'urgence claires, à l'intérieur de chaque bord de route
    pygame.draw.rect(surface, COULEUR_BANDE_URGENCE, (BORD_ROUTE, 0, LARGEUR_BANDE_URGENCE, HAUTEUR_FENETRE))
    pygame.draw.rect(surface, COULEUR_BANDE_URGENCE,
                      (BORD_ROUTE + LARGEUR_ROUTE - LARGEUR_BANDE_URGENCE, 0, LARGEUR_BANDE_URGENCE, HAUTEUR_FENETRE))

    # Les lignes jaunes continues, juste à côté des bandes d'urgence
    epaisseur_ligne_jaune = 4
    x_jaune_gauche = BORD_ROUTE + LARGEUR_BANDE_URGENCE
    x_jaune_droite = BORD_ROUTE + LARGEUR_ROUTE - LARGEUR_BANDE_URGENCE - epaisseur_ligne_jaune
    pygame.draw.rect(surface, COULEUR_LIGNE_JAUNE, (x_jaune_gauche, 0, epaisseur_ligne_jaune, HAUTEUR_FENETRE))
    pygame.draw.rect(surface, COULEUR_LIGNE_JAUNE, (x_jaune_droite, 0, epaisseur_ligne_jaune, HAUTEUR_FENETRE))


def dessiner_lignes_centrales(surface):
    """Dessine la ligne blanche centrale, en pointillés."""
    largeur_ligne = 7
    hauteur_pointille = 38
    espace = 28
    x_ligne = LARGEUR_FENETRE // 2 - largeur_ligne // 2

    y = 0
    while y < HAUTEUR_FENETRE:
        pygame.draw.rect(surface, COULEUR_LIGNE_BLANCHE, (x_ligne, y, largeur_ligne, hauteur_pointille))
        y += hauteur_pointille + espace


def dessiner_arbre(surface, x, y, echelle=1.0, image=None):
    """Dessine un arbre, soit avec une image fournie, soit en vectoriel
    (tronc marron + 3 cercles verts qui se superposent pour donner du
    volume au feuillage)."""
    if image is not None:
        rect_image = image.get_rect(center=(x, y))
        surface.blit(image, rect_image)
        return

    rayon = int(20 * echelle)
    largeur_tronc = max(4, int(8 * echelle))
    hauteur_tronc = int(16 * echelle)

    # ombre au sol de l'arbre (légère ellipse sombre)
    pygame.draw.ellipse(surface, (20, 70, 20), (x - rayon, y + rayon - 6, rayon * 2, 12))
    # tronc
    pygame.draw.rect(surface, (96, 64, 40), (x - largeur_tronc // 2, y, largeur_tronc, hauteur_tronc))
    # feuillage (3 cercles décalés pour un effet "buisson" plutôt qu'un cercle plat)
    pygame.draw.circle(surface, (24, 100, 35), (x, y - int(6 * echelle)), rayon)
    pygame.draw.circle(surface, (34, 130, 45), (x - int(9 * echelle), y - int(11 * echelle)), int(rayon * 0.78))
    pygame.draw.circle(surface, (46, 150, 55), (x + int(9 * echelle), y - int(11 * echelle)), int(rayon * 0.78))


def dessiner_voiture(surface, rect, couleur_carrosserie, image=None):
    """
    Dessine une voiture (joueur ou obstacle) vue de dessus.
    Si une image est fournie, on l'utilise directement. Sinon, on
    dessine une voiture vectorielle détaillée : ombre, carrosserie
    arrondie, toit/vitres, 4 roues, phares avant, feux arrière.
    """
    if image is not None:
        surface.blit(image, rect)
        return

    x, y, largeur, hauteur = rect.x, rect.y, rect.width, rect.height

    # --- Ombre portée au sol (légèrement décalée), pour donner du volume ---
    ombre_rect = pygame.Rect(x + 4, y + 6, largeur, hauteur)
    surface_ombre = pygame.Surface((largeur + 12, hauteur + 12), pygame.SRCALPHA)
    pygame.draw.ellipse(surface_ombre, (0, 0, 0, 80), surface_ombre.get_rect())
    surface.blit(surface_ombre, (ombre_rect.x - 6, ombre_rect.y - 6))

    # --- Roues (4 petits rectangles noirs qui dépassent légèrement de la carrosserie) ---
    largeur_roue, hauteur_roue = 8, 20
    for decalage_y in (10, hauteur - 30):
        pygame.draw.rect(surface, (20, 20, 20), (x - 3, y + decalage_y, largeur_roue, hauteur_roue), border_radius=2)
        pygame.draw.rect(surface, (20, 20, 20), (x + largeur - largeur_roue + 3, y + decalage_y, largeur_roue, hauteur_roue), border_radius=2)

    # --- Carrosserie (corps principal arrondi) ---
    pygame.draw.rect(surface, couleur_carrosserie, rect, border_radius=14)
    # un léger reflet (bande plus claire) pour donner un effet de brillance
    couleur_reflet = tuple(min(255, c + 45) for c in couleur_carrosserie)
    pygame.draw.rect(surface, couleur_reflet, (x + 5, y + 4, largeur - 10, 6), border_radius=3)

    # --- Toit / vitres (pare-brise avant + lunette arrière) ---
    couleur_vitre = (35, 40, 55)
    pare_brise = pygame.Rect(x + 8, y + 16, largeur - 16, 22)
    lunette_arriere = pygame.Rect(x + 8, y + hauteur - 38, largeur - 16, 18)
    pygame.draw.rect(surface, couleur_vitre, pare_brise, border_radius=6)
    pygame.draw.rect(surface, couleur_vitre, lunette_arriere, border_radius=6)

    # --- Phares avant (blanc/jaune pâle) et feux arrière (rouges) ---
    pygame.draw.circle(surface, (255, 250, 210), (x + 9, y + 6), 4)
    pygame.draw.circle(surface, (255, 250, 210), (x + largeur - 9, y + 6), 4)
    pygame.draw.rect(surface, (200, 30, 30), (x + 6, y + hauteur - 6, 10, 4), border_radius=2)
    pygame.draw.rect(surface, (200, 30, 30), (x + largeur - 16, y + hauteur - 6, 10, 4), border_radius=2)


def dessiner_score(surface, valeur_score):
    """Affiche le score dans un petit encadré semi-transparent, plus
    lisible qu'un texte posé directement sur le décor."""
    texte = police.render(f"Score : {valeur_score}", True, COULEUR_TEXTE)
    largeur_cadre = texte.get_width() + 24
    hauteur_cadre = texte.get_height() + 14

    cadre = pygame.Surface((largeur_cadre, hauteur_cadre), pygame.SRCALPHA)
    pygame.draw.rect(cadre, (0, 0, 0, 120), cadre.get_rect(), border_radius=10)
    surface.blit(cadre, (14, 14))
    surface.blit(texte, (14 + 12, 14 + 7))


# --------------------------------------------------------------
# 9. BOUCLE PRINCIPALE
# --------------------------------------------------------------
horloge = pygame.time.Clock()
en_cours = True

while en_cours:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False

    # --- Affichage : on dessine dans l'ordre, du fond vers le premier plan ---
    dessiner_fond_et_route(fenetre)

    # arbres derrière la route (décor de fond)
    for arbre in arbres:
        dessiner_arbre(fenetre, arbre["x"], arbre["y"], arbre["echelle"], image_arbre)

    dessiner_lignes_centrales(fenetre)

    for obstacle in obstacles:
        dessiner_voiture(fenetre, obstacle["rect"], obstacle["couleur"], obstacle["image"])

    dessiner_voiture(fenetre, voiture_joueur, COULEUR_VOITURE_JOUEUR, image_voiture_joueur)
    dessiner_score(fenetre, score)

    pygame.display.flip()
    horloge.tick(60)

pygame.quit()
