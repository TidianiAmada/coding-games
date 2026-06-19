"""
====================================================================
07_reassemblage.py
====================================================================
Maintenant qu'on a décortiqué chaque pièce (fichiers 01 à 06, qui
ne nécessitent AUCUNE installation), il est temps de remettre tout
en place pour obtenir le VRAI jeu, jouable au clavier.

Contrairement aux fichiers précédents, le jeu complet a BESOIN de
Pygame, car c'est Pygame qui sait ouvrir une vraie fenêtre
graphique et lire le clavier en temps réel -- chose qu'on ne peut
pas faire avec uniquement la bibliothèque standard de Python.

Les 3 fichiers du jeu complet sont :
    etape1_decor.py
    etape2_animations.py
    etape3_evenements.py

Lancez ce fichier avec :   python3 07_reassemblage.py
====================================================================
"""

import os

print("""
============================================================
 RE-ASSEMBLAGE DU JEU COMPLET
============================================================

On a vu, pièce par pièce, comment fonctionnent :
   - le DECOR        (fichier 04)
   - les ANIMATIONS    (fichier 05)
   - les EVENEMENTS    (fichier 06)

Le vrai jeu, lui, combine les trois dans une seule grande boucle
de jeu, en utilisant Pygame pour la fenêtre et le clavier. Pour
le lancer chez vous :
""")

print("""
    1) Installer Pygame UNE SEULE FOIS (nécessite une connexion
       internet) :

           pip install pygame

    2) Lancer chaque étape dans un terminal (pas dans ce fichier !) :

           python etape1_decor.py
           python etape2_animations.py
           python etape3_evenements.py
""")

# On vérifie simplement si les 3 fichiers du jeu sont présents
# dans le même dossier, pour aider l'élève à s'organiser.
fichiers_attendus = ["etape1_decor.py", "etape2_animations.py", "etape3_evenements.py"]

print("Vérification de la présence des fichiers du jeu complet :\n")
for nom_fichier in fichiers_attendus:
    present = os.path.exists(nom_fichier)
    statut = "trouvé ✔" if present else "absent (à copier dans ce dossier)"
    print(f"  - {nom_fichier:<28} -> {statut}")

print("""
Si un fichier est marqué "absent", copiez-le simplement dans ce
même dossier (atelier_sans_modules) -- ce sont les fichiers que
nous avons créés ensemble lors de la toute première partie de
l'atelier (création du jeu).

Une fois les 3 fichiers réunis et Pygame installé, vous pourrez
jouer pour de vrai : flèches gauche/droite pour déplacer la
voiture, évitez les obstacles, et tentez de battre votre meilleur
score !

Passez maintenant au fichier 08_perspectives.py
""")
