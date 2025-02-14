# Jour de repos

C'est dimanche et vous n'avez pas cours. Vous avez décidé de passer la journée avec votre ami humain, pour jouer à un jeu de carte que vous adorez. Les règles de ce jeu sont les suivantes. Vous avez chacun exactement 8 cartes, et chaque carte a un nombre entier compris entre 0 et 4. À chaque tour, vous ou votre ami choisissez chacun deux cartes, une du joueur actuel, et une de l'adversaire. Appelons-les c1 et c2, où c1 représente le nombre sur la carte du joueur et c2 représente le nombre sur la carte de l'adversaire. Une seule règle pour ce choix : il est nécessaire que c1 * c2 ≠ 0. Il faut ensuite déterminer c = (c1 + c2) modulo 5 et remplacer le nombre c1 par la valeur c calculée. Le joueur qui réussit à mettre à zéro les 8 cartes en premier gagne. Si une boucle se forme, il y a égalité car aucun joueur n'arrivera à avoir toutes ses cartes à 0.

Vous souhaitez mettre vos cours en pratique et souhaitez savoir qui gagne dans certaines situations si les deux joueurs choisissent les meilleures opérations à chaque tour. Pour chaque situation, vous savez qui commence à jouer et vous connaissez les 8 cartes de chacun des deux joueurs.

## Données en entrée :

* La première ligne contient un entier représentant le nombre de situations à considérer.
* Les lignes suivantes décrivent ces situations. Pour chaque situation :

  1. La première ligne contient un entier : 0 si vous jouez en premier, 1 si c'est votre ami humain qui joue en premier
  2. La deuxième ligne contient 8 entiers, représentant vos cartes.
  3. La troisième ligne contient 8 entiers représentant les cartes de votre ami.

## Résultat attendu :

* une liste de caractères en majuscule séparés par des espaces :

  1. "R" (sans les guillemets) si vous gagnez.
  2. "H" (sans les guillemets) si votre ami gagne.
  3. "E" (sans les guillemets) si c'est une égalité, c'est-à-dire que personne ne gagne.

## Exemple :

### Entrée :

3  
0  
1 0 0 0 0 0 0 0   
0 0 0 4 0 0 2 0  
1  
1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1  
1  
0 0 0 1 0 0 0 0  
0 0 0 0 4 0 0 0  

### Sortie :

R
E
H

### Explication des exemples :

1. Dans la première situation, vous choisissez les cartes 1 et 4 et gagnez après cette opération.
2. Dans la deuxième situation, on peut prouver qu'une boucle se forme et que personne ne gagne, il s'agit donc d'une égalité.
3. Dans la troisième situation, votre ami choisit les cartes 4 et 1. Comme (4 + 1) modulo 5 = 0, il gagne après cette opération.