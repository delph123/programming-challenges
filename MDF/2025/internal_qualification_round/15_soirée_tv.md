# Soirée TV

Les robots de l'internat ont une salle commune avec plusieurs téléviseurs pour regarder leurs émissions préférées. Cependant, un problème est survenu : plusieurs téléviseurs sont allumées en même temps, et ils occupent toutes les prises disponibles. Afin de libérer une prise pour pouvoir recharger leurs batteries, vous voulez éteindre un téléviseur. Mais attention ! Vous ne voulez pas éteindre un téléviseur si cela raccourcit la période pendant laquelle au moins un téléviseur est allumé. Ils doivent donc s’assurer que le téléviseur qu’ils éteignent est "redondant", c'est-à-dire qu’il ne contribue pas de manière significative à la durée pendant laquelle une télé est allumée dans la salle.

Votre objectif est de trouver l'indice du téléviseur redondant.

## Données en entrée :

* une première ligne qui contient un entier : le nombre de télévisions
* une ligne pour chaque télé qui décrit les horaires où chaque téléviseur est allumé sous la forme de 2 entiers.

## Résultat attendu :

un entier : l'indice du téléviseur redondant

## Exemple :

### Entrée :

4  
1 5  
2 6  
5 9  

### Sortie :

2

**Explications :** Dans cet exemple, la période pendant laquelle au moins un téléviseur est allumé est de [1;9]. Si l'on éteint le deuxieme téléviseur, la période reste [1;9], donc ce téléviseur est redondant.