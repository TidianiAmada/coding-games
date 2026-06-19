"""
====================================================================
08_perspectives.py
====================================================================
Dernier fichier de l'atelier : maintenant que vous connaissez les
trois piliers (décor, animation, événements), vous pouvez inventer
N'IMPORTE QUEL jeu !

Lancez ce fichier avec :   python3 08_perspectives.py
====================================================================
"""

idees_de_projets = [
    {
        "nom": "Jeu de saut",
        "idee": "un personnage doit sauter par-dessus des obstacles avec la barre ESPACE",
        "notion": "événements (touche unique), gravité (animation)",
    },
    {
        "nom": "Évitement spatial",
        "idee": "un vaisseau évite des astéroïdes qui viennent de tous les côtés",
        "notion": "décor (fond étoilé), module random",
    },
    {
        "nom": "Collecte de pièces",
        "idee": "un personnage se déplace dans un labyrinthe et ramasse des pièces",
        "notion": "listes d'objets, score",
    },
    {
        "nom": "Système de vies",
        "idee": "le joueur a 3 vies au lieu d'un Game Over immédiat",
        "notion": "dictionnaires, conditions (if/elif)",
    },
    {
        "nom": "Vraies images",
        "idee": "remplacer les rectangles par des images de voitures (pygame.image.load)",
        "notion": "Pygame avancé",
    },
    {
        "nom": "Sons",
        "idee": "ajouter un bruit de moteur et un son de collision (pygame.mixer)",
        "notion": "Pygame avancé",
    },
    {
        "nom": "Meilleur score",
        "idee": "sauvegarder le meilleur score dans un fichier texte entre deux parties",
        "notion": "lecture/écriture de fichiers",
    },
    {
        "nom": "Deux joueurs",
        "idee": "deux voitures sur la même route, contrôlées par deux claviers différents",
        "notion": "événements multiples",
    },
    {
        "nom": "Niveaux de difficulté",
        "idee": "tous les 100 points, augmenter nettement la vitesse et le nombre d'obstacles",
        "notion": "logique de jeu, conditions",
    },
]

print("=" * 70)
print(" PERSPECTIVES ET IDEES DE MINI-PROJETS")
print("=" * 70)
print()

for i, projet in enumerate(idees_de_projets, start=1):
    print(f"{i}. {projet['nom']}")
    print(f"   Idée    : {projet['idee']}")
    print(f"   Notion  : {projet['notion']}")
    print()

print("""
Pour aller plus loin :
  - Essayez de changer une seule constante (VITESSE_DEFILEMENT,
    LARGEUR_ROUTE...) dans etape3_evenements.py et observez l'effet.
  - Choisissez UNE SEULE idée de la liste ci-dessus et ajoutez-la à
    votre jeu existant plutôt que de tout reconstruire : c'est
    comme ça que les vrais développeurs travaillent, petit à petit !

Bravo, vous savez maintenant comment un jeu vidéo est construit,
pièce par pièce -- à vous de jouer (et de coder) !
""")
