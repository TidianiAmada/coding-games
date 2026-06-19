"""
====================================================================
03_concepts_pygame.py
====================================================================
Pygame ajoute par-dessus Python des outils spécialisés pour les
jeux : une fenêtre, une Surface (la zone où dessiner), un Rect
(rectangle) pour représenter chaque objet, une boucle de jeu, et
la détection des événements.

Pour ne PAS avoir besoin d'installer Pygame ici, on recrée une
mini-version maison du rectangle de Pygame : la classe MiniRect.
Elle fonctionne EXACTEMENT comme pygame.Rect pour ce qui nous
intéresse (la position et la détection de collision).

Lancez ce fichier avec :   python3 03_concepts_pygame.py
====================================================================
"""


# --------------------------------------------------------------
# 1. LA CLASSE MiniRect (équivalent maison de pygame.Rect)
# --------------------------------------------------------------
class MiniRect:
    """
    Une version simplifiée de pygame.Rect : un rectangle qui connaît
    sa position (x, y) et sa taille (largeur, hauteur), et qui sait
    répondre à une question essentielle :
        "est-ce que je touche cet autre rectangle ?"
    grâce à sa méthode colliderect().

    Dans le vrai jeu, on utilise directement pygame.Rect, qui
    fonctionne sur EXACTEMENT ce principe (Pygame fait ce calcul
    pour nous, pas besoin de le réécrire).
    """

    def __init__(self, x, y, largeur, hauteur):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur

    def colliderect(self, autre):
        """Renvoie True si ce rectangle touche 'autre'."""
        return (
            self.x < autre.x + autre.largeur
            and self.x + self.largeur > autre.x
            and self.y < autre.y + autre.hauteur
            and self.y + self.hauteur > autre.y
        )

    def __repr__(self):
        return f"MiniRect(x={self.x}, y={self.y})"


print("=" * 60)
print("1. Le Rect : la brique de base de tout objet du jeu")
print("=" * 60)

voiture = MiniRect(150, 600, 50, 90)
obstacle_loin = MiniRect(150, 100, 50, 90)
obstacle_proche = MiniRect(160, 620, 50, 90)

print("Voiture            :", voiture)
print("Obstacle loin       :", obstacle_loin)
print("Obstacle proche     :", obstacle_proche)
print()
print("Voiture vs obstacle loin   ->", voiture.colliderect(obstacle_loin))
print("Voiture vs obstacle proche ->", voiture.colliderect(obstacle_proche))

print("""
Dans le VRAI fichier etape3_evenements.py, c'est très exactement
le même principe, mais avec le vrai objet Pygame (qui fait ce
calcul pour nous) :

    voiture = pygame.Rect(150, 600, 50, 90)
    obstacle = pygame.Rect(160, 620, 50, 90)

    if voiture.colliderect(obstacle):
        etat["game_over"] = True
""")


# --------------------------------------------------------------
# 2. LA FENETRE, LA SURFACE, ET LA BOUCLE DE JEU (explication)
# --------------------------------------------------------------
print("=" * 60)
print("2. La fenêtre, la Surface, et la boucle de jeu")
print("=" * 60)

print("""
Voici le code réel de Pygame (on ne l'exécute pas ici, car il
ouvre une vraie fenêtre graphique) :

    fenetre = pygame.display.set_mode((600, 800))  # crée la fenêtre

    horloge = pygame.time.Clock()
    en_cours = True

    while en_cours:                            # boucle de jeu : elle
        for evenement in pygame.event.get():   # tourne sans arrêt,
            if evenement.type == pygame.QUIT:   # ~60 fois par seconde
                en_cours = False

        # ... mise à jour de la logique (déplacer, collisions) ...
        # ... dessiner tout sur la fenêtre ...

        pygame.display.flip()    # affiche réellement l'image
        horloge.tick(60)         # limite à 60 images par seconde

Trois idées importantes :
  - 'while en_cours:' est une boucle infinie : elle continue tant
    que 'en_cours' vaut True.
  - 'pygame.event.get()' renvoie la liste de tout ce qui s'est
    passé depuis la dernière fois (clic, touche, fermeture...).
  - 'horloge.tick(60)' est ce qui transforme une suite d'images
    fixes en une animation fluide à l'oeil humain.
""")

print("Passez maintenant au fichier 04_zoom_decor.py")
