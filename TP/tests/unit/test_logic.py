from triangulator.core import triangulate, Triangle
import math
import pytest

def distance_carre(p1, p2):
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2

def obtenir_cercle_circonscrit(a, b, c):
    """retourne (center_x, center_y, radius_sq) du cercle circonscrit."""
    D = 2 * (a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1]))
    if abs(D) < 1e-9: # points colinéaires
        return None
    
    Ux = ((a[0]**2 + a[1]**2) * (b[1] - c[1]) + (b[0]**2 + b[1]**2) * (c[1] - a[1]) + (c[0]**2 + c[1]**2) * (a[1] - b[1])) / D
    Uy = ((a[0]**2 + a[1]**2) * (c[0] - b[0]) + (b[0]**2 + b[1]**2) * (a[0] - c[0]) + (c[0]**2 + c[1]**2) * (b[0] - a[0])) / D
    
    radius_sq = (Ux - a[0])**2 + (Uy - a[1])**2
    return (Ux, Uy, radius_sq)

def est_delaunay(points, triangles):
    """Vérifie la condition du cercle vide pour tous les triangles."""
    for tri in triangles:
        p1 = points[tri[0]]
        p2 = points[tri[1]]
        p3 = points[tri[2]]
        
        circum = obtenir_cercle_circonscrit(p1, p2, p3)
        if circum is None: continue # Ignorer triangles plats (ou gérer erreur)

        center_x, center_y, r_sq = circum
        
        # Vérifier qu'aucun autre point n'est dans ce cercle
        for i, p in enumerate(points):
            if i in tri: continue
            dist = (p[0] - center_x)**2 + (p[1] - center_y)**2
            # Tolérance epsilon pour les erreurs flottantes
            if dist < r_sq - 1e-5:
                return False
    return True


def test_triangulation_simple_triangle():
    # 3 points forment 1 triangle.
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    result = triangulate(points)
    assert len(result) == 1
    # L'ordre des indices peut varier mais doit être valide
    assert set(result[0]) == {0, 1, 2}

def test_triangulation_carre_delaunay():
    # 4 points en carré. Delaunay doit couper selon la diagonale la plus "courte" 
    # ou respecter le cercle vide.
    points = [(0,0), (1,0), (1,1), (0,1)]
    result = triangulate(points)
    
    assert len(result) == 2 # 2 triangles pour un carré
    assert est_delaunay(points, result)

def test_points_alignes():
    # 3 points alignés -> Pas de triangle 
    points = [(0,0), (1,1), (2,2)]
    result = triangulate(points)
    assert len(result) == 0

def test_triangulation_pas_assez_de_points():
    assert len(triangulate([])) == 0
    assert len(triangulate([(0,0)])) == 0
    assert len(triangulate([(0,0), (1,1)])) == 0

def test_triangulation_grand_nuage():
    # 5 points : Carré + 1 point au centre (0.5, 0.5)
    points = [(0,0), (1,0), (1,1), (0,1), (0.5, 0.5)]
    result = triangulate(points)
    
    assert len(result) == 4
    assert est_delaunay(points, result)

def test_enveloppe_convexe():
    points = [(0,0), (2,0), (1,3), (-1, 2)]
    result = triangulate(points)
    
    idxs = set()
    for t in result:
        idxs.update(t)
    
    assert len(idxs) == 4 # Tous les points sont utilisés
    assert est_delaunay(points, result)

def test_integrite_indices():
    # vérifie que les indices retournés sont strictement bornés à [0, N-1]
    points = [(0,0), (10,0), (0,10), (10,10), (5,5)]
    triangles = triangulate(points)
    
    N = len(points)
    for tri in triangles:
        assert len(tri) == 3
        for idx in tri:
            assert  0 <= idx < N, f"Indice {idx} hors bornes [0, {N-1}]"

def test_fusion_precision():
    # deux points quasi-identiques doivent être fusionnés

    points = [
        (0.0, 0.0),
        (1.0, 0.0),
        (0.0, 1.0),
        (0.5, 0.5),
        (0.5, 0.5000000001) # fusionné en (0.5, 0.5)
    ]
    
    try:
        triangles = triangulate(points)
    except ZeroDivisionError:
        pytest.fail("Division par zéro due à la précision float")
    

    assert len(triangles) > 0
    assert est_delaunay(points, triangles)

def test_triangle_collinear_circumcircle():
    # On crée 3 points alignés 
    points = [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)]

    t = Triangle(0, 1, 2, points)

    assert t.center == points[0]
    assert t.r_sq == 0.0

def test_triangulate_deduplication_under_3_points():
    # On fournit 3 points mais ils sont identiques ou doublons tels que unique < 3
    points = [(0.0, 0.0), (0.0, 0.0), (0.00000001, 0.00000001)] 
    
    result = triangulate(points)
    assert result == []
