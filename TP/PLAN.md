# TODO
Objectif du TP:
lister les tests que vous prévoyez de mettre en place et pourquoi/comment vous prévoyez de les mettre en place
tester entrée/sortie/performances/qualite du code

-Appel API:
    -Au lancement du serveur, verification de l'etat du serveur, du port sur lequel il tourne

    -Client -> Triangulator :
        - Test de la valeur(de pointSetId) reçu par le Triangulator (sur cette route /triangulation/{pointSetId}): 
            - Valeur manquante (pas de pointSetId) renvoie de l'erreur 404 The specified PointSetID was not found (as reported by the PointSetManager).
            - Valeur incorrecte ( pas au format UUID ) renvoie de l'erreur 400 Bad request, e.g., invalid PointSetID format.
            - Valeur correcte (UUID valide d'un valeur qui existe) renvoie  200 OK
                 
    -Triangulator -> Client  :
        - Test des valeurs envoyé(les triangles au format binaire) au client
            - Valeur manquante (aucun triangles) renvoie l'erreur 500 Internal server error, e.g., triangulation algorithm failed.
            - Valeur incorrecte (pas au format binaire) renvoie l'erreur 500 Internal server error, e.g., triangulation algorithm failed.
            - Valeur correcte (au format binaire) renvoie  200 OK
         
    -Triangulator -> PointSetManager:
        - Test de la valeur(de pointSetId) à envoyé à PointSetManager :
            - Valeur manquante (pas de pointSetId) 404 Not found, A PointSet with the specified ID was not found.
            - Valeur incorrecte ( pas au format UUID ) 400 Bad request, e.g., invalid PointSetID format.
            - Valeur correcte (UUID valide d'un valeur qui existe) 200 OK

    - PointSetManager -> Triangulator:
        - test de la gestion de la reception du set de points:
            - Valeur manquante (pas d'ensemble de points) renvoie de l'erreur 404 The specified PointSetID was not found (as reported by the PointSetManager).
            - Valeur incorrecte (reception d'un erreur / ou d'un mauvais formatage) renvoie de l'erreur 400 Bad request, e.g., invalid PointSetID format.
            - Valeur correcte (emsemble de point bien formaté) 200 OK

- Logique de la fonction:

    - Algorithms:
        - test de la gestion selon la valeur d'entrée (PointSet) quelle sortie on obtient:
            - bonne valeur en entrée(Formatage, et valeur) / bonne valeur de sortie (Format et valeur de sortie)
            - mauvaise valeur en entrée(Formatage, et valeur) / Erreur sortie: mauvais type d'entrée (exemple: moins de 3 points, pas de triangles)
            - aucune valeur en entrée / Erreur sortie: absence d'entrée 
    
     
-Qualite du code:

    on va utiliser l'outils ruff avec ses règles de base et en definir de nouvelles. on utilisera cette commande pour verifier si tout est ok 'ruff check'
    
    pdoc3 pour créer la doc du fichier 
    
-Test de performance:

    -Faire des test de temps sur l'excution de l'algorithms, la complexité de l'algo de base est de O(n^2) mais peut etre optimisée pour une complexité de O(nlog(n)) selon la complexité de l'algo faire un test avec plusieurs jeu de variables et voir si le temps trouvé est coherent par rapport à la taille du PointSet et ça complexité

    -Faire des test sur l'execution de la conversion vers/depuis le format binaire avec des plusieurs jeu de valeurs, grand set plus petit valeur similaire differentes et verifier le temps par rapport a la complexité de la conversion et de l'entrée

    


