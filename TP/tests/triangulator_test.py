# test de conversion binary vers PointSet 
# test de l'algo entrée sortie (nombre de triangles)
# faire des mocks pour les fonctions de triangulation


def test_binary_to_pointset_empty(): 
    # variable binaire vide 
    bin = '0'
    conv = binary_to_pointset(bin)
    #  on verifie si conv est vide 
    assert conv == []
    
def test_pointset_to_binary_empty():   
    points = []
    conv = pointset_to_binary(points)
    #  on verifie si conv == 0 en binaire
    assert conv == b'\x00\x00\x00\x00'
        
def test_triangulation_algorithm():
    pass

def test_triangulation_output():
    pass

def test_triangulation_with_mocks():
    pass


