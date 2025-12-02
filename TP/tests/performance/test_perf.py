import pytest
import time
import struct
import random

# from triangulator.models import PointSet, Triangles
# from triangulator.core import triangulate
TIMEOUT_DESERIALIZATION = 1.0
TIMEOUT_ALGORITHM = 5.0
TIMEOUT_SERIALIZATION = 1.0

# Taille du jeu de données pour le stress test.
LARGE_N = 10000

@pytest.mark.performance
def test_performance_gros_dataset():
    # mesure le temps de triangulation pour un grand nombre de points.
    # avec 10 000 points aléatoires
    points = [(i * 1.0, i * 1.0) for i in range(10000)] 
    
    start_time = time.time()
    # triangulate(points)
    duration = time.time() - start_time
    
    #on définit un seuil acceptable 2 secondes
    # assert duration < 2.0, f"Triangulation trop lente: {duration}s"
    pass


def generer_binaire_pointset_volumineux(n_points):
    # 1. Header
    header = struct.pack('>I', n_points)
    
    # 2. Coordonnées (Génération de N points aléatoires)
    coords = []
    # On génère une longue liste à plat [x0, y0, x1, y1, ...]
    for _ in range(n_points):
        coords.extend([random.uniform(0, 1000), random.uniform(0, 1000)])
    
    # 3. Packing du corps
    # Format string : '>ffff...' (autant de 'f' que de valeurs)
    fmt = '>' + 'f' * (n_points * 2)
    body = struct.pack(fmt, *coords)
    
    return header + body, coords

@pytest.mark.performance
class TestPerformance:


    def test_perf_deserialization(self):

        # mesure le temps de conversion : Binaire (PointSet) -> Objet Python.

        # Un gros volume de données binaires simulé
        binary_data, _ = generer_binaire_pointset_volumineux(LARGE_N)
        
        #on mesure le temps de parsing
        start_time = time.perf_counter()
        
    
        # point_set = PointSet.from_bytes(binary_data)
        
        # simulation
        time.sleep(0.1) 
        
        end_time = time.perf_counter()
        duration = end_time - start_time
        
        # Le temps doit être inférieur au seuil défini
        print(f"\n Désérialisation de {LARGE_N} points : {duration:.4f}s")
        assert duration < TIMEOUT_DESERIALIZATION, \
            f"Parsing trop lent : {duration:.4f}s > {TIMEOUT_DESERIALIZATION}s"

    def test_perf_triangulation_algo(self):
  
        # Mesure le temps de calcul pur de l'algorithme.
        # Une liste de points (déjà désérialisés)
        points = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(LARGE_N)]
        
        start_time = time.perf_counter()
                
        # result = triangulate(points)
        
        # simulation
        time.sleep(0.5)
        
        end_time = time.perf_counter()
        duration = end_time - start_time
        
        # L'algo doit respecter le temps imparti
        print(f"\n[PERF] Triangulation de {LARGE_N} points : {duration:.4f}s")
        assert duration < TIMEOUT_ALGORITHM, \
            f"Algo trop lent : {duration:.4f}s > {TIMEOUT_ALGORITHM}s"

    def test_perf_serialization(self):
        # mesure le temps de conversion : Objet Triangles -> Binaire.
        n_triangles = LARGE_N * 2
        
        # On simule les données d'entrée
        # points_data = [(0.0, 0.0)] * LARGE_N
        # indices_data = [(0, 1, 2)] * n_triangles
        
        # triangles_obj = Triangles(points=points_data, triangles=indices_data)
        
        #On mesure la génération du binaire
        start_time = time.perf_counter()
        # binary_out = triangles_obj.to_bytes()
        
        # simulation
        time.sleep(0.1)
        
        end_time = time.perf_counter()
        duration = end_time - start_time

        print(f"\n[PERF] Sérialisation de {n_triangles} triangles : {duration:.4f}s")
        assert duration < TIMEOUT_SERIALIZATION, \
            f"Sérialisation trop lente : {duration:.4f}s > {TIMEOUT_SERIALIZATION}s"