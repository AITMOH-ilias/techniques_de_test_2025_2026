import math

class Triangle:
    """
    3 sommets et 3 voisins
    """
    def __init__(self, a, b, c, points_ref):
        # a, b, c les indices des points
        self.a = a
        self.b = b
        self.c = c
        
        # pointeurs vers les triangles voisins par chaque arête.
        self.nab = None 
        self.nbc = None
        self.nca = None
        
        # marqueur pour les algorithmes de parcours (BFS) pour éviter de traiter 2 fois le même triangle.
        self.visited_mark = -1 
        
        # le triangle fait partie du maillage actuel.
        self.active = True 
        
        # cercle circonscrit (centre et rayon au carré).
        self.center, self.r_sq = self._calc_circumcircle(points_ref)
        
    def _calc_circumcircle(self, points):
        """
        calcule les propriétés du cercle circonscrit (cercle passant par les 3 sommets).
        retourne ((x, y), rayon^2)
        """
        A, B, C = points[self.a], points[self.b], points[self.c]
        D = 2 * (A[0] * (B[1] - C[1]) + B[0] * (C[1] - A[1]) + C[0] * (A[1] - B[1]))
        
        if abs(D) < 1e-12: 
            return (A, 0.0)
            
        Ux = ((A[0]**2 + A[1]**2) * (B[1] - C[1]) + (B[0]**2 + B[1]**2) * (C[1] - A[1]) + (C[0]**2 + C[1]**2) * (A[1] - B[1])) / D
        Uy = ((A[0]**2 + A[1]**2) * (C[0] - B[0]) + (B[0]**2 + B[1]**2) * (A[0] - C[0]) + (C[0]**2 + C[1]**2) * (B[0] - A[0])) / D
        
        return ((Ux, Uy), (Ux - A[0])**2 + (Uy - A[1])**2)

    def is_in_circumcircle(self, p):
        """
        vérifie si le point p se trouve à l'intérieur du cercle circonscrit.
        """
        d_sq = (p[0] - self.center[0])**2 + (p[1] - self.center[1])**2
        return d_sq < self.r_sq - 1e-8 

def triangulate(points_entree: list) -> list:
    """
    prend une liste de points (x, y) et renvoie une liste de triangles (i, j, k).
    """
    if not points_entree or len(points_entree) < 3:
        return []

    # 1. nettoyage
    # si deux points sont pareils, on en garde un seul (le premier)
    liste_points_uniques = [] # stocke les points sans doublons
    idx_unique_vers_original = [] # pour savoir qui est qui a la fin 
    
    coords_vues = {} # dictionnaire pour reperer les doublons rapidement
    
    for indice_original, p in enumerate(points_entree):
        # on arrondit un peu pour eviter les bugs de precision
        coordonnees_arrondies = (round(p[0], 7), round(p[1], 7))
        
        if coordonnees_arrondies not in coords_vues:
            coords_vues[coordonnees_arrondies] = indice_original
            liste_points_uniques.append(p)
            idx_unique_vers_original.append(indice_original)
        # sinon on jette le doublon
    
    # check si on a assez de points
    if len(liste_points_uniques) < 3:
        return []
        

    # tri pour que ca aille plus vite (tri spatial x, y)
    # il faut garder la trace des indices pendant le mélange
    points_tries_avec_idx = sorted(enumerate(liste_points_uniques), key=lambda x: (x[1][0], x[1][1]))
    
    points_locaux = [p for (idx, p) in points_tries_avec_idx] # la liste de points triée qu'on va utiliser

    
    idx_trie_vers_unique = [idx for (idx, p) in points_tries_avec_idx] 
    
    nb_points_utiles = len(points_locaux) # Nombre de points réels (sans le super triangle)
    
    # 2. le super-triangle
    # on cherche les limites du nuage de points
    min_x = min(p[0] for p in points_locaux)
    max_x = max(p[0] for p in points_locaux)
    min_y = min(p[1] for p in points_locaux)
    max_y = max(p[1] for p in points_locaux)
    
    dx = max_x - min_x
    dy = max_y - min_y
    delta_max = max(dx, dy) if max(dx, dy) > 0 else 1.0 
    centre_x = (min_x + max_x) / 2
    centre_y = (min_y + max_y) / 2
    
    # on fait un triangle geant qui englobe tout le monde
    # on le fait tres grand (x20) pour etre tranquille
    pt_super_1 = (centre_x - 20 * delta_max, centre_y - delta_max)
    pt_super_2 = (centre_x, centre_y + 20 * delta_max)
    pt_super_3 = (centre_x + 20 * delta_max, centre_y - delta_max)
    
    points_locaux.extend([pt_super_1, pt_super_2, pt_super_3])
    
    # creation du premier triangle (le super triangle)
    triangle_racine = Triangle(nb_points_utiles, nb_points_utiles+1, nb_points_utiles+2, points_locaux)
    liste_triangles = [triangle_racine] # la liste de tous nos triangles
    dernier_triangle = triangle_racine # le dernier triangle créé (optimisation)
    
    # 3. algo (bowyer-watson)
    for i in range(nb_points_utiles):
        point_courant = points_locaux[i]
        
        # a. on cherche le premier triangle invalide
        triangle_depart = None # le triangle qui contient le point
        # test avec le dernier triangle créé
        if dernier_triangle.active and dernier_triangle.is_in_circumcircle(point_courant):
            triangle_depart = dernier_triangle
        else:
            # sinon on parcourt la liste des triangles
            for t in reversed(liste_triangles): 
                if t.active and t.is_in_circumcircle(point_courant):
                    triangle_depart = t
                    break
        
        if triangle_depart is None: continue
            
        # b. on trouve tous les triangles qui vont pas (ceux dont le cercle contient le point)
        mauvais_triangles = [] # liste des triangles à supprimer
        file_attente = [triangle_depart] # file pour le parcours en largeur (BFS)
        triangle_depart.visited_mark = i 
        mauvais_triangles.append(triangle_depart)
        
        idx_file = 0
        # parcours en largeur (BFS)
        while idx_file < len(file_attente):
            courant = file_attente[idx_file]
            idx_file += 1
            for voisin in [courant.nab, courant.nbc, courant.nca]:
                if voisin and voisin.active and voisin.visited_mark != i:
                    if voisin.is_in_circumcircle(point_courant):
                        voisin.visited_mark = i
                        mauvais_triangles.append(voisin)
                        file_attente.append(voisin)
        
        # c. on enlève les mauvais et on bouche le trou
        aretes_frontiere = [] # les bords du trou laissé par la suppression 
        for tri in mauvais_triangles:
            tri.active = False # marque comme supprimé
            if tri.nab is None or tri.nab.visited_mark != i:
                aretes_frontiere.append((tri.a, tri.b, tri.nab))
            if tri.nbc is None or tri.nbc.visited_mark != i:
                aretes_frontiere.append((tri.b, tri.c, tri.nbc))
            if tri.nca is None or tri.nca.visited_mark != i:
                aretes_frontiere.append((tri.c, tri.a, tri.nca))

        nouveaux_triangles = [] # liste des nouveaux triangles créés dans le trou
        dico_aretes = {} # pour connecter les voisins entre eux
        for (u, v, voisin_tri) in aretes_frontiere:
            nouveau_tri = Triangle(u, v, i, points_locaux)
            nouveaux_triangles.append(nouveau_tri)
            liste_triangles.append(nouveau_tri)
            
            nouveau_tri.nab = voisin_tri 
            if voisin_tri:
                # mise a jour du lien retour depuis le voisin existant
                if voisin_tri.nab and not voisin_tri.nab.active: voisin_tri.nab = nouveau_tri
                elif voisin_tri.nbc and not voisin_tri.nbc.active: voisin_tri.nbc = nouveau_tri
                elif voisin_tri.nca and not voisin_tri.nca.active: voisin_tri.nca = nouveau_tri
            
            # on connecte les nouveaux morceaux entre eux via le dico
            dico_aretes[(nouveau_tri.b, nouveau_tri.c)] = nouveau_tri
            dico_aretes[(nouveau_tri.c, nouveau_tri.a)] = nouveau_tri

        # d. on finit de recoudre (liens internes au trou)
        for t in nouveaux_triangles:
            inv_bc = (t.c, t.b)
            if inv_bc in dico_aretes: t.nbc = dico_aretes[inv_bc]
            inv_ca = (t.a, t.c)
            if inv_ca in dico_aretes: t.nca = dico_aretes[inv_ca]
        
        if nouveaux_triangles: dernier_triangle = nouveaux_triangles[0]

    # 4. Partie finale
    indices_finaux = []
    
    # nb_points_utiles c'est la limite, au dessus c'est le super-triangle
    # on veut pas garder les triangles qui touchent le bord artificiel
    
    for t in liste_triangles:
        if not t.active: continue
        
        # si ca touche le super-triangle, poubelle
        if t.a >= nb_points_utiles or t.b >= nb_points_utiles or t.c >= nb_points_utiles:
            continue
            
        # on remet les bons indices d'origine
        
        idx_a = idx_trie_vers_unique[t.a]
        idx_b = idx_trie_vers_unique[t.b]
        idx_c = idx_trie_vers_unique[t.c]
        
        vrai_a = idx_unique_vers_original[idx_a]
        vrai_b = idx_unique_vers_original[idx_b]
        vrai_c = idx_unique_vers_original[idx_c]
        
        indices_finaux.append((vrai_a, vrai_b, vrai_c))
            
    return indices_finaux
