# Au tableau !

Vous êtes en salle de classe, et aujourd'hui c'est à votre tour de passer au tableau. Vous vous approchez de l'estrade et remarquez une ligne de diodes colorés. Les couleurs sont représentées par des chiffres afin de simplifier la lecture.

Un ensemble connecté est composé de diodes de même couleur, toutes côte à côte. Vous voyez en haut du tableau deux exemples pour mieux comprendre ce qu'est un ensemble connecté. Par exemple :

* il n'y a qu'1 ensemble connecté dans la ligne suivante : [2,2,2,2]
* il y a 4 ensembles connectés dans la ligne suivante : [1,5,3,3,6,6,6]

Une opération consiste en un changement de couleur de tout un ensemble connecté. L'exercice au tableau d'aujourd'hui consiste à trouver le nombre minimum d'opérations nécessaires afin que toute la ligne soit de la même couleur.

## Données en entrée :

* la première ligne est un entier : le nombre de diodes de la ligne
* la seconde ligne est une suite d'entiers séparés par des espaces : la ligne des diodes colorées que vous avez recopié du tableau

## Résultat attendu :

Un entier : le nombre minimum d'opérations

## Exemple :

### Entrée :

7  
1 6 3 3 6 6 6

### Sortie :

2

**Explication :** Voici un déroulé possible :

* l'ensemble de couleur 3 devient un ensemble de couleur 6 : [1,6,6,6,6,6,6]
* l'ensemble de couleur 6 devient un ensemble de couleur 1 : [1,1,1,1,1,1,1]

La solution pour cet exemple est donc 2.