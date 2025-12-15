import struct

class PointSet:
    def __init__(self, points):
        self.points = points  # Liste de tuples (x, y)

    @staticmethod
    def from_bytes(data: bytes):
        """Désérialise le format binaire """
        if len(data) < 4:
            raise ValueError("Données incomplètes (header manquant)")
            
        # Lecture du header : 4 bytes, unsigned long (>I pour Big-Endian)
        nb_points = struct.unpack('>I', data[:4])[0]
        
        expected_size = 4 + (nb_points * 8)
        if len(data) != expected_size:
            raise ValueError(f"Taille des données incohérente. Attendu: {expected_size}, Reçu: {len(data)}")

        points = []
        offset = 4
        # Lecture des points : 2 floats (x, y) par point
        for _ in range(nb_points):
            x, y = struct.unpack('>ff', data[offset:offset+8])
            points.append((x, y))
            offset += 8
            
        return PointSet(points)

class Triangles:
    def __init__(self, points, triangles):
        self.points = points      # Liste de coords (x, y)
        self.triangles = triangles # Liste de tuples d'indices (i, j, k)

    def to_bytes(self) -> bytes:
        """Sérialise au format binaire"""
        # Partie 1 : Vertices (Même format que PointSet)
        nb_points = len(self.points)
        binary = struct.pack('>I', nb_points)
        for x, y in self.points:
            binary += struct.pack('>ff', x, y)
            
        # Partie 2 : Triangles
        nb_triangles = len(self.triangles)
        binary += struct.pack('>I', nb_triangles)
        for t in self.triangles:
            # 3 indices unsigned long par triangle
            binary += struct.pack('>III', t[0], t[1], t[2])
            
        return binary
