# Les cadeaux perdus

C'est la fête de Noel de l'université. Chaque robot a tiré un numéro, et ils doivent tous se mettre en ligne pour recevoir leur cadeau. Mais les cadeaux du Père Noël apparaissent dans un ordre bien précis. Chaque robot doit donc essayer de se placer exactement à la bonne position correspondant à son numéro pour être sûr de recevoir le bon cadeau.

Au début, les robots sont tous mélangés dans la file (ce désordre correspond à une permutation des numéros des robots). Les robots ont une règle stricte : au lieu de changer de place individuellement (parce qu'ils ont des roues trop lourdes), ils peuvent seulement se déplacer en groupe en faisant des rotations cycliques de leur file. Cela signifie que tous les robots reculent d’une place, et celui qui était à la fin de la fille passe en tête.

Le but des robots est de trouver le meilleur décalage cyclique vers la droite qui permettra à la file d’être le plus proche possible de l’ordre idéal, où chaque robot est aligné avec son numéro. L'ordre idéal est : Robot 1 en première position, Robot 2 en deuxième, et ainsi de suite.
Ils cherchent la déviation minimale, c'est-à-dire la somme des distances entre chaque robot et la position où il devrait idéalement se trouver. Autrement dit, chaque robot cherche à avoir la plus petite erreur possible entre son numéro et celui de son cadeau (sa position idéale).

## Données en entrée :

1. La première ligne est entier : le nombre de robots dans la file.
2. La seconde ligne est ne liste des numéros des robots : l’ordre initial de la file.

## Résultat attendu :

Deux entier séparés par un espace :

1. La déviation minimale atteinte grâce au bon décalage.
2. Le nombre de rotations nécessaires pour atteindre cette déviation.

## Exemple:

### Entrée :

3  
2 3 1

### Sortie :

0 1

**Explication :** Avec une seule rotation cyclique, la file devient [1, 2, 3], et tout le monde est à la bonne place. La déviation est donc 0.