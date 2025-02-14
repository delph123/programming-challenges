# Les repas de la cantine

Les robots étudiants de l'université sont connus pour être impatients. En arrivant à la cantine, vous voyez une file impressionnante d'étudiants attendant d'être servis.

Chacun de ces étudiants à un souhait particulier de repas, chacun de ces repas va prendre aux robots cuisiniers une durée fixe de préparation. Les robots étudiants n'ayant pas eu leur repas au bout de cette durée (le temps est dépassé strictement) atteindront la limite de leur programme de patience, et s'en iront. Le temps d’attente d’un robot étudiant correspond à la somme des durées de préparation des repas des robots étudiants devant lui dans la file. Les cuisiniers prennent le temps de préparer un repas pour chaque étudiant, même si ces derniers s'en vont. Par exemple, si les trois premiers étudiants robots de la file ont un temps respectif d'attente de 1, 2 et 3, alors le quatrieme devra attendre 6 avant de commander. Dans ce cas, si son temps d'attente est inférieur à 6 alors il s'en ira.

Vous vous souvenez avoir suivi cette année un cours de permutations, et vous vous demandez s'il n'est pas possible de réduire le nombre d'étudiants susceptibles de partir en les permutant dans la file, en prenant en compte la durée de préparation de leurs repas respectifs.

## Données en entrée :

* la première ligne est un entier : le nombre d'étudiants dans la file
* la seconde ligne est une suite d'entiers séparés par des espaces : le temps nécessaire de préparation de chaque repas

## Résultat attendu :

Un entier : le plus grand nombre possible d'étudiants servis

## Exemple :

### Entrée :

5  
19 2 5 1 3

### Sortie :

4

**Explication :** Après permutations, l'agencement optimal de cette file est le suivant : [1, 2, 3, 5, 19]

La solution pour cet exemple est 4, car le robot de valeur 5 s'en ira avant la fin de la préparation de son repas.