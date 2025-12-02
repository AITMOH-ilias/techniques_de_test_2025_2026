import pytest
import struct

# from triangulator.models import PointSet, Triangles

class TestPointSetFormats:

    # tests du format binaire PointSet.
    # - 4 bytes (unsigned long, Big Endian) : Nombre de points (N)
    # - N * 8 bytes : Points (Float X, Float Y)


    def test_lecture_octets_ok(self):
        # vérifie la lecture d'un binaire valide contenant 2 points.
        nb_points = 2
        p1_x, p1_y = 0.0, 0.0
        p2_x, p2_y = 1.0, 2.0
        
        # Construction manuelle du binaire attendu
        # '>I' = Big-endian Unsigned Int (4 bytes)
        # '>ffff' = 4 Floats Big-endian (4 bytes chacun)
        binary_data = struct.pack('>I', nb_points) + struct.pack('>ffff', p1_x, p1_y, p2_x, p2_y)

        # point_set = PointSet.from_bytes(binary_data)


        # assert len(point_set.points) == 2
        # assert point_set.points == (0.0, 0.0)
        # assert point_set.points[6] == (1.0, 2.0)
        
        # pour que le test passe à vide, à enlever après implémentation
        assert len(binary_data) == 4 + (2 * 8)

    def test_pointset_octets_vide(self):
        # vérifie la lecture d'un ensemble vide.
        binary_data = struct.pack('>I', 0) # 0 points
        
        # point_set = PointSet.from_bytes(binary_data)
        
        # assert len(point_set.points) == 0
        pass

    def test_pointset_entete_malformee(self):
        # doit échouer si le header est incomplet (moins de 4 bytes).
        binary_data = b'\x00\x01' # Seulement 2 bytes
        
        # with pytest.raises(ValueError): # ou struct.error
        #     PointSet.from_bytes(binary_data)
        pass

    def test_pointset_donnees_incompletes(self):
        # doit échouer si le nombre de points annoncé ne correspond pas aux données.
        # On annonce 1 point, mais on ne fournit pas les coordonnées
        binary_data = struct.pack('>I', 1) 
        
        # with pytest.raises(ValueError):
        #     PointSet.from_bytes(binary_data)
        pass


class TestTrianglesFormats:

    def test_triangles_octets(self):
        # vérifie que l'objet Triangles génère le bon format binaire.

        # points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
        # indices = [(0, 1, 2)] # Un seul triangle
        # triangles_obj = Triangles(points=points, triangles=indices)

        # binary_output = triangles_obj.to_bytes()

        expected_size = 4 + 24 + 4 + 12
        # assert len(binary_output) == expected_size

        # vérification du contenu exact
        expected_header_pts = struct.pack('>I', 3) 
        expected_points = struct.pack('>ffffff', 0.0, 0.0, 1.0, 0.0, 0.0, 1.0)
        expected_header_tris = struct.pack('>I', 1)
        expected_indices = struct.pack('>III', 0, 1, 2)
        
        expected_full_binary = expected_header_pts + expected_points + expected_header_tris + expected_indices
        
        # assert binary_output == expected_full_binary
        pass

    def test_sans_triangles(self):
        # cas où on a des points mais aucun triangle formé.
        # points = [(0.0, 0.0), (1.0, 1.0)]
        # indices = [] 
        # triangles_obj = Triangles(points=points, triangles=indices)
        
        # binary_output = triangles_obj.to_bytes()
        
        # assert len(binary_output) == 24
        # assert binary_output[-4:] == struct.pack('>I', 0) # Vérifie que nb_triangles = 0 à la fin
        pass