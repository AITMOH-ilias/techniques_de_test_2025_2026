# TODO
- Plan :mal fait:
         - pas assez pris de temps sur le choix de l'algo 
           donc mon choix de test n'etait pas assez precis dès le début
         - pas penser aux test unitaire pour le formatage 
         - manque les test pour la gestion des erreurs serveurs 
        bien fait:
         - bonne separation des tests
         - une base correcte avec peu voir pas de tests inutiles
         - 
- Implementation des tests:
        mal fait:
        - j'aurais du penser à l'architecture des tests dès le début
        bien fait:
        - ajout des test manquant 
        - modification/suppression des tests qui ne convenait pas avec l'implementation du code 
- Implementation du code:
        mal fait:
        - algo de triangulation choisi au début trop lent
        - beacoup de temps perdu sur le choix et le changement d'algo
        - comme on fait les tests et le code, j'ai parfois anticipés certains tests 
        bien fait:
        - gestion des erreurs adapté aux tests

Test en plus (par rapport au plan initial):
        - Robustesse API :
            - Validation du header `Accept` (406 Not Acceptable)
            - Gestion des timeouts et erreurs de connexion au PointSetManager (503)
            - Validation stricte du `Content-Type` reçu du Manager (rejet si HTML/Text)
            - Gestion des réponses tronquées ou incomplètes venant du Manager
        - Logique & Algorithme :
            - Vérification d'intégrité des indices de sortie (bornes [0, N-1])
            - Gestion de la précision flottante et fusion des points quasi-identiques
            - Vérification de l'enveloppe convexe (utilisation correcte des points externes)
        - Formats :
            - Vérification stricte de l'Endianness (Big-Endian) pour la portabilité 