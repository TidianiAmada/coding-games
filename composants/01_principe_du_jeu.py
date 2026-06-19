"""
====================================================================
01_principe_du_jeu.py
====================================================================
Premier fichier de l'atelier : on ne touche encore à aucun code de
jeu. On explique simplement le PRINCIPE qui se cache derrière
TOUS les jeux vidéo, du plus simple au plus compliqué.

Lancez ce fichier avec :   python3 01_principe_du_jeu.py
====================================================================
"""

print("""
============================================================
 LE PRINCIPE UNIVERSEL DE CREATION D'UN JEU VIDEO
============================================================

Que ce soit un jeu de course, un jeu de plateforme ou un jeu
d'aventure, TOUS les jeux vidéo reposent sur les trois mêmes
piliers :

   1) LE DECOR        : de quoi la scène est-elle faite ? 
   2) L'ANIMATION      : comment les choses bougent-elles ?
   3) LES EVENEMENTS   : comment le joueur agit-il sur le jeu ?

Avec des DECORS seul, nous avons un ou des dessins. Avec des ANIMATIONS on obtient des dessins animés,
      Et avec la gestions des EVENEMENTS ça devient un jeu vidéo.
      
""")

# Un petit schéma dessiné avec du texte, pour visualiser le
# "pipeline" (l'enchaînement) d'une boucle de jeu.
schema = r"""
   +-----------+        +--------------+        +--------------+
   |  DECOR    |  --->  |  ANIMATION   |  --->  |  EVENEMENTS   |
   | (le quoi) |        | (le mouvement)|       | (l'interaction)|
   +-----------+        +--------------+        +--------------+
        |                                              |
        +------------------- boucle de jeu ------------+
                  (répétée ~60 fois par seconde)
"""
print(schema)

print("""
Dans notre jeu de course automobile, ces trois piliers
correspondent à :

   DECOR        -> la route, la voiture, les obstacles, le score
   ANIMATION    -> la route qui défile, les obstacles qui tombent
   EVENEMENTS   -> les touches du clavier, les collisions,
                   les points gagnés, le Game Over

Dans les fichiers suivants de cet atelier, on va prendre une
LOUPE et observer chacun de ces piliers en détail, en recréant
les mêmes mécanismes avec du Python "tout simple" (sans Pygame), pour bien comprendre ce qui se passe à
l'intérieur du jeu.
""")
