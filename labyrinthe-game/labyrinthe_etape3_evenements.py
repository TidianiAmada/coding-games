"""
====================================================================
LABYRINTHE - ÉTAPE 3 : GÉRER LES ÉVÉNEMENTS (JEU COMPLET)
====================================================================

C'est le fichier final, à lancer pour JOUER pour de vrai. Il reprend
le décor et les animations des étapes 1 et 2, et ajoute :

    - le déplacement du personnage avec les flèches (ou Z/Q/S/D)
    - la détection de collision avec les murs (le personnage ne peut
      pas traverser un mur)
    - le ramassage des pièces (+10 points, petite gerbe de particules)
    - un chronomètre
    - un écran de VICTOIRE quand toutes les pièces sont ramassées,
      avec un nouveau labyrinthe généré si on rejoue (touche ESPACE)

(Voir labyrinthe_etape1_decor.py pour les explications détaillées
sur la génération du labyrinthe et le chargement d'images.)
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
TAILLE_PERSONNAGE = 26
VITESSE_PERSONNAGE = 4
POINTS_PAR_PIECE = 10

COULEUR_SOL_1 = (214, 192, 150)
COULEUR_SOL_2 = (198, 176, 134)
COULEUR_MUR = (95, 72, 55)
COULEUR_MUR_CLAIR = (135, 105, 80)
COULEUR_MUR_FONCE = (60, 44, 33)
COULEUR_PERSONNAGE = (40, 120, 210)
COULEUR_PIECE = (250, 200, 40)
COULEUR_TEXTE = (255, 255, 255)
COULEUR_FLAMME = (250, 150, 40)
COULEUR_VICTOIRE = (255, 215, 60)

DOSSIER_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
pygame.display.set_caption("Labyrinthe - Étape 3 : Le Jeu Complet")

police = pygame.font.SysFont("Arial", 26, bold=True)
police_titre = pygame.font.SysFont("Arial", 48, bold=True)


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
# 3. GÉNÉRATION DU LABYRINTHE (identique aux étapes précédentes)
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
        torches.append({"x": x, "y": y, "phase": random.uniform(0, math.tau)})
    return torches


# --------------------------------------------------------------
# 4. CRÉATION / RÉINITIALISATION D'UNE PARTIE
# --------------------------------------------------------------
def nouvelle_partie():
    """
    Construit un TOUT NOUVEAU labyrinthe (différent à chaque partie)
    et range tout l'état du jeu dans un seul dictionnaire, pour
    pouvoir relancer facilement une partie après une victoire.
    """
    grille = generer_labyrinthe(LIGNES, COLONNES)
    murs = construire_murs(grille)
    torches = choisir_torches(grille, NOMBRE_TORCHES)

    x_depart, y_depart = case_vers_pixel(0, 0)
    personnage = pygame.Rect(0, 0, TAILLE_PERSONNAGE, TAILLE_PERSONNAGE)
    personnage.center = (x_depart, y_depart)

    cases_libres = [case for case in cases_praticables(grille) if case != (0, 0)]
    cases_pieces = random.sample(cases_libres, min(NOMBRE_PIECES, len(cases_libres)))
    pieces = []
    for (r, c) in cases_pieces:
        x, y = case_vers_pixel(r, c)
        pieces.append({"x": x, "y": y, "phase": random.uniform(0, math.tau), "ramassee": False})

    poussieres = []
    for _ in range(NOMBRE_POUSSIERES):
        poussieres.append({
            "x": random.uniform(0, LARGEUR_FENETRE),
            "y": random.uniform(HAUTEUR_HUD, HAUTEUR_FENETRE),
            "vitesse_y": random.uniform(-0.3, -0.1),
            "taille": random.uniform(1, 2.5),
            "opacite": random.randint(40, 110),
        })

    return {
        "murs": murs,
        "torches": torches,
        "personnage": personnage,
        "pieces": pieces,
        "poussieres": poussieres,
        "particules_ramassage": [],  # petites étincelles dorées
        "score": 0,
        "pieces_restantes": len(pieces),
        "victoire": False,
        "debut_partie_ms": pygame.time.get_ticks(),
        "temps_final_secondes": None,
    }


# --------------------------------------------------------------
# 5. FONCTIONS DE MISE À JOUR (LOGIQUE DU JEU)
# --------------------------------------------------------------
def deplacer_avec_collision(rect, dx, dy, murs):
    """
    Déplace 'rect' de (dx, dy), en empêchant de traverser un mur.
    On déplace d'abord sur l'axe X, on vérifie les collisions, PUIS
    on déplace sur l'axe Y et on vérifie à nouveau : en séparant les
    deux axes, le personnage peut "glisser" le long d'un mur au lieu
    de se bloquer complètement en biais.
    """
    rect.x += dx
    for mur in murs:
        if rect.colliderect(mur["rect"]):
            if dx > 0:
                rect.right = mur["rect"].left
            elif dx < 0:
                rect.left = mur["rect"].right

    rect.y += dy
    for mur in murs:
        if rect.colliderect(mur["rect"]):
            if dy > 0:
                rect.bottom = mur["rect"].top
            elif dy < 0:
                rect.top = mur["rect"].bottom


def gerer_clavier(etat):
    touches = pygame.key.get_pressed()
    dx = dy = 0
    if touches[pygame.K_LEFT] or touches[pygame.K_q] or touches[pygame.K_a]:
        dx -= VITESSE_PERSONNAGE
    if touches[pygame.K_RIGHT] or touches[pygame.K_d]:
        dx += VITESSE_PERSONNAGE
    if touches[pygame.K_UP] or touches[pygame.K_z] or touches[pygame.K_w]:
        dy -= VITESSE_PERSONNAGE
    if touches[pygame.K_DOWN] or touches[pygame.K_s]:
        dy += VITESSE_PERSONNAGE

    deplacer_avec_collision(etat["personnage"], dx, dy, etat["murs"])


def emettre_particules_ramassage(etat, x, y):
    """Crée une petite gerbe d'étincelles dorées au moment où une pièce
    est ramassée, pour une sensation de récompense plus satisfaisante."""
    for _ in range(10):
        angle = random.uniform(0, math.tau)
        vitesse = random.uniform(1.5, 3.5)
        etat["particules_ramassage"].append({
            "x": x, "y": y,
            "vx": math.cos(angle) * vitesse,
            "vy": math.sin(angle) * vitesse,
            "vie": 20,
        })


def mettre_a_jour_particules_ramassage(etat):
    for particule in etat["particules_ramassage"]:
        particule["x"] += particule["vx"]
        particule["y"] += particule["vy"]
        particule["vie"] -= 1
    etat["particules_ramassage"][:] = [p for p in etat["particules_ramassage"] if p["vie"] > 0]


def detecter_ramassage_pieces(etat):
    """Vérifie si le personnage touche une pièce non encore ramassée.
    Si oui : on la marque comme ramassée, on ajoute des points, et on
    déclenche les étincelles. Si toutes les pièces sont ramassées,
    c'est la victoire !"""
    personnage = etat["personnage"]
    for piece in etat["pieces"]:
        if piece["ramassee"]:
            continue
        distance = math.hypot(personnage.centerx - piece["x"], personnage.centery - piece["y"])
        if distance < (TAILLE_PERSONNAGE // 2 + 10):
            piece["ramassee"] = True
            etat["score"] += POINTS_PAR_PIECE
            etat["pieces_restantes"] -= 1
            emettre_particules_ramassage(etat, piece["x"], piece["y"])

    if etat["pieces_restantes"] <= 0 and not etat["victoire"]:
        etat["victoire"] = True
        etat["temps_final_secondes"] = (pygame.time.get_ticks() - etat["debut_partie_ms"]) / 1000


def animer_poussieres(etat):
    for grain in etat["poussieres"]:
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
    temps = pygame.time.get_ticks() / 1000
    vacillement = math.sin(temps * 6 + phase) * 3 + random.uniform(-1, 1)

    pygame.draw.rect(surface, (70, 50, 35), (x - 3, y - 4, 6, 14), border_radius=2)

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
    temps = pygame.time.get_ticks() / 1000
    decalage_y = math.sin(temps * 3 + phase) * 4
    intensite_reflet = (math.sin(temps * 5 + phase) + 1) / 2
    position_y = y + decalage_y

    if image is not None:
        surface.blit(image, image.get_rect(center=(x, position_y)))
        return

    pygame.draw.circle(surface, (150, 110, 10), (x, int(position_y)), 9)
    pygame.draw.circle(surface, COULEUR_PIECE, (x, int(position_y)), 8)
    couleur_reflet = tuple(int(COULEUR_PIECE[i] + (255 - COULEUR_PIECE[i]) * intensite_reflet) for i in range(3))
    pygame.draw.circle(surface, couleur_reflet, (x - 2, int(position_y) - 2), 3)


def dessiner_particules_ramassage(surface, particules):
    for particule in particules:
        opacite = max(0, min(255, particule["vie"] * 12))
        etincelle = pygame.Surface((6, 6), pygame.SRCALPHA)
        pygame.draw.circle(etincelle, (255, 215, 90, opacite), (3, 3), 3)
        surface.blit(etincelle, (particule["x"] - 3, particule["y"] - 3))


def dessiner_poussieres(surface, liste_poussieres):
    for grain in liste_poussieres:
        particule = pygame.Surface((6, 6), pygame.SRCALPHA)
        pygame.draw.circle(particule, (255, 230, 190, grain["opacite"]), (3, 3), grain["taille"])
        surface.blit(particule, (grain["x"] - 3, grain["y"] - 3))


def dessiner_hud(surface, etat):
    pygame.draw.rect(surface, (30, 24, 20), (0, 0, LARGEUR_FENETRE, HAUTEUR_HUD))

    texte_score = police.render(f"Score : {etat['score']}", True, COULEUR_TEXTE)
    pieces_ramassees = len(etat["pieces"]) - etat["pieces_restantes"]
    texte_pieces = police.render(f"Pièces : {pieces_ramassees} / {len(etat['pieces'])}", True, COULEUR_TEXTE)

    if etat["temps_final_secondes"] is not None:
        secondes = etat["temps_final_secondes"]
    else:
        secondes = (pygame.time.get_ticks() - etat["debut_partie_ms"]) / 1000
    texte_temps = police.render(f"Temps : {secondes:0.1f} s", True, COULEUR_TEXTE)

    surface.blit(texte_score, (20, HAUTEUR_HUD // 2 - texte_score.get_height() // 2))
    surface.blit(texte_temps, (LARGEUR_FENETRE // 2 - texte_temps.get_width() // 2,
                                HAUTEUR_HUD // 2 - texte_temps.get_height() // 2))
    surface.blit(texte_pieces, (LARGEUR_FENETRE - texte_pieces.get_width() - 20,
                                 HAUTEUR_HUD // 2 - texte_pieces.get_height() // 2))


def dessiner_victoire(surface, etat):
    calque = pygame.Surface((LARGEUR_FENETRE, HAUTEUR_FENETRE), pygame.SRCALPHA)
    calque.fill((0, 0, 0, 170))
    surface.blit(calque, (0, 0))

    titre = police_titre.render("BRAVO !", True, COULEUR_VICTOIRE)
    surface.blit(titre, titre.get_rect(center=(LARGEUR_FENETRE // 2, HAUTEUR_FENETRE // 2 - 70)))

    sous_titre = police.render("Toutes les pièces sont ramassées !", True, COULEUR_TEXTE)
    surface.blit(sous_titre, sous_titre.get_rect(center=(LARGEUR_FENETRE // 2, HAUTEUR_FENETRE // 2 - 10)))

    texte_score = police.render(f"Score final : {etat['score']}  -  Temps : {etat['temps_final_secondes']:0.1f} s",
                                 True, COULEUR_TEXTE)
    surface.blit(texte_score, texte_score.get_rect(center=(LARGEUR_FENETRE // 2, HAUTEUR_FENETRE // 2 + 30)))

    texte_rejouer = police.render("Appuyez sur ESPACE pour un nouveau labyrinthe", True, COULEUR_TEXTE)
    surface.blit(texte_rejouer, texte_rejouer.get_rect(center=(LARGEUR_FENETRE // 2, HAUTEUR_FENETRE // 2 + 70)))


# --------------------------------------------------------------
# 7. BOUCLE PRINCIPALE
# --------------------------------------------------------------
horloge = pygame.time.Clock()
etat = nouvelle_partie()
en_cours = True

while en_cours:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False
        if evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_SPACE and etat["victoire"]:
                etat = nouvelle_partie()

    if not etat["victoire"]:
        gerer_clavier(etat)
        detecter_ramassage_pieces(etat)

    animer_poussieres(etat)
    mettre_a_jour_particules_ramassage(etat)

    # --- Affichage ---
    dessiner_sol(fenetre)
    dessiner_murs(fenetre, etat["murs"])
    dessiner_poussieres(fenetre, etat["poussieres"])

    for torche in etat["torches"]:
        dessiner_torche(fenetre, torche["x"], torche["y"], torche["phase"])

    for piece in etat["pieces"]:
        if not piece["ramassee"]:
            dessiner_piece(fenetre, piece["x"], piece["y"], piece["phase"], image_piece)

    dessiner_particules_ramassage(fenetre, etat["particules_ramassage"])
    dessiner_personnage(fenetre, etat["personnage"], image_personnage)
    dessiner_hud(fenetre, etat)

    if etat["victoire"]:
        dessiner_victoire(fenetre, etat)

    pygame.display.flip()
    horloge.tick(60)

pygame.quit()
