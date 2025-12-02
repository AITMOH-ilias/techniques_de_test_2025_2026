# from triangulator.core import triangulate
import pytest

def test_triangulation_simple_triangle():
    # 3 points forment 1 triangle.
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    # result = triangulate(points)
    # assert len(result) == 1
    # assert result == (0, 1, 2) # indices des sommets
    pass

def test_triangulation_square():
    # 4 points en carré forment 2 triangles.
    points = [(0,0), (1,0), (1,1), (0,1)]
    # result = triangulate(points)
    # assert len(result) == 2
    pass

def test_collinear_points():
    # Cas limite: 3 Points alignés.
    points = [(0,0), (1,1), (2,2)]
    # (soit 0 triangles, soit erreur gérée)
    # result = triangulate(points)
    # assert len(result) == 0
    pass

def test_triangulation_pas_assez_de_points():

    # Moins de 3 points.

    # Cas avec 2 points
    points = [(0.0, 0.0), (1.0, 1.0)]
    # result = triangulate(points)
    # assert len(result) == 0
    
    # cas avec liste vide
    # result_empty = triangulate([])
    # assert len(result_empty) == 0
    pass

def test_triangulation_points_dupliques():

#   points dupliqués.

    # un triangle avec un point en double 4 points en entrée, mais géométriquement 3
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0), (0.0, 0.0)]
    
    # result = triangulate(points)
    
    # Doit résulter en 1 triangle valide en ignorant le doublons
    # assert len(result) >= 1
    pass

def test_triangulation_large_shape():
    # test sur plus de 4 points.
    # 5 points 
    points = [
        (0.0, 0.0), (2.0, 0.0), # Base
        (2.0, 2.0), (0.0, 2.0), # Carré
        (1.0, 3.0)              # Toit
    ]
    
    # result = triangulate(points)  
    # Ici 5 sommets donc 3 triangles attendus
    # assert len(result) == 3
    pass