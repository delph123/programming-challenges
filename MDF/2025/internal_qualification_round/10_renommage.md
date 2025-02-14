# Renommage collectif

Une fois par an, un examen spécial a lieu : les étudiants robots doivent se trouver un nouveau nom, et pas n'importe lequel. Il faut que ce soit un nom à la fois unique et parfait, à partir d'un certain nombre de lettres données. Pour cela, il faut respecter certaines règles bien précises !

Ces règles sont les suivantes :

1. Le nom ne doit pas être plus long que celui qu'on lui a donné.
2. Le nom doit être un palindrome, c'est-à-dire qu'il se lit pareil dans les deux sens, comme "radar" ou "civic".
3. Ce nom spécial doit être formé à partir de deux parties : la concaténation du début des lettres qu'on lui a donné (le préfixe), et de la fin de ces mêmes lettres (le suffixe). Ces parties peuvent être vides.
4. Si plusieurs noms de même longueur sont possibles, on donne prioriété au préfixe le plus grand.

Tous les étudiants de l'école doivent changer leur nom, pouvez-vous les aider à trouver leurs nouveaux noms ?

## Données en entrée :

* une première ligne qui contient un entier : le nombre de robots qui doivent choisir un nouveau nom
* une ligne pour chaque robot : les lettres qui doivent être utilisées pour trouver chaque nom

## Résultat attendu :

la liste des nouveaux noms séparés par des espaces

## Exemple pour deux robots :

### Entrée :

3  
xyztechyx  
techxyzyx  
mdf  

### Sortie :

xyzyx xyzyx m

**Explications :** Vous avez trouvé les trois noms suivants : "xyzyx", "xyzyx" et "m". En suivant les règles, vous formez :

* "xyzyx", qui commence par "xyz" et finit par "yx"
* "xyzyx", qui commence par vide et finit par "xyzyx"
* "m" qui commence par "m" et finit par vide.