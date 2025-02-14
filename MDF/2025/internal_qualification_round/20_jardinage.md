# Cours de jardinage

Aujourd’hui, vous assistez à un cours de jardinage magique où l’on apprend à cultiver des arbres magiques parfaitement équilibrés. Le professeur vous propose un exercice spécial pour tester vos compétences en suivant des règles bien définies.

Chaque arbre doit respecter les principes suivants :

1. Structure et essence magique :

    * Un arbre possède une racine et au plus deux sous-arbres : un sous-arbre gauche et un sous-arbre droit, jamais plus.
    * Chaque noeud contient une essence magique unique (un entier).
    * Les essences du sous-arbre gauche doivent être strictement inférieures à celle du noeud parent.
    * Les essences du sous-arbre droit doivent être strictement supérieures à celle du noeud parent.

2. Équilibre magique :

    * L’arbre doit être parfaitement équilibré, c’est-à-dire organisé de manière à minimiser la somme des profondeurs de ses sous-abres.

3. Règle de rayures :

    * Si un noeud parent possède un sous-arbre gauche, la parité (pair ou impair) de l'essence magique de la racine de ce sous-abre doit être différente de la parité de l'essence magique du noeud parent.
    * Si un noeud parent possède un sous-arbre droit, la parité (pair ou impair) de l'essence magique de la racine de ce sous-abre doit être identique de la parité de l'essence magique du noeud parent.

Votre mission est d’écrire un programme permettant de compter le nombre d’arbres respectant ces règles en utilisant des essences distinctes comprises entre 1 et n, où n est le nombre de noeuds (racine incluse).

Le résultat doit être donné modulo 998244353 car le nombre d’arbres magiques possibles peut être très grand.

L'exercice d'aujourd'hui consiste à trouver ce résultat pour 8 cas différents.

Vous posez tout de même la question de ce qu'est un arbre équilibré. Le robot professeur vous donne la réponse suivante. Un arbre est équilibré lorsque la somme des profondeurs de ses noeuds est minimale. Cela signifie que l'arbre est bien organisé et compact.

### Exemples d'arbres :

        2
       /  \  
      1    4
          /
         3

L'abre ci-dessus structure bien ses noeuds, est équilibré et est rayé. Il respecte les 3 règles.

       1
        \
         3
         /
        2  

L'abre ci-dessus structure bien ses noeuds et est rayé. Cependant, il n'est pas équilibré car il y a un autre agencement qui limite la profondeur.

        2
      /   \  
     1     3

L'abre ci-dessus structure bien ses noeuds et est équilibré. Cependant, il n'est pas rayé à cause de la parité des noeuds.

        3
      /   \  
     2     1

L'abre ci-dessus ne structure pas bien ses noeuds. (2<3 mais 1 devrait etre supérieur à 3)

## Données en entrée :

8 entiers séparés par des espaces : le nombre de branches (ou essences magiques) à organiser dans l'arbre pour chacun des 8 cas demandés.

## Résultat attendu :

8 entiers séparés par des espaces : le nombre d’arbres magiques possibles respectant toutes les règles, modulo ( 998244353 ), pour chacun des 8 cas demandés.

## Exemple pour deux cas :

Entrée :

4 3

Sortie :

1 0

**Explication :** Pour le cas 1, avec 4 branches, il n'existe qu'un seul arbre qui respecte les règles d'équilibre et de rayures. Pour le cas 2, avec 3 branches, il est impossible de respecter toutes les règles en même temps.