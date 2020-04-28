
"""
Computer Graphics. Course 2019/2020. ESI UCLM.
Final Project. Antonio Manjavacas.
3D Utils: Vertex, Vector and Face classes
"""

class Vertex:

    id = 1

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        self.id = Vertex.id
        Vertex.id += 1

    def __str__(self):
        return 'v ' + str(self.x) + ' ' + str(self.y) + ' ' + str(self.z)

    def __eq__(self, v):
        if isinstance(v, Vertex):
            return self.x == v.x and self.y == v.y and self.z == v.z
        else:
            return False

class Face:
    def __init__(self, v1, v2, v3, v4):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.v4 = v4

        self.vertices = [v1,v2,v3,v4]

    def __str__(self):
        return 'f ' + str(self.v1.id) + ' ' + str(self.v2.id) + ' ' + str(self.v3.id) + ' ' + str(self.v4.id)


class Bar:
    def __init__(self, name, faces):
        self.name = name
        self.faces = faces

    def __str__(self):
        
        header = '\no ' + self.name + '\n'
        
        vertices = []
        text_vertices = ''
        for face in self.faces:
            if(face.v1 not in vertices):
                text_vertices += str(face.v1) + '\n'
                vertices.append(face.v1)
            if(face.v2 not in vertices):
                text_vertices += str(face.v2) + '\n'
                vertices.append(face.v2)
            if(face.v3 not in vertices):
                text_vertices += str(face.v3) + '\n'
                vertices.append(face.v3)
            if(face.v4 not in vertices):
                text_vertices += str(face.v4) + '\n'
                vertices.append(face.v4)
        
        text_faces = ''
        for face in self.faces:
            text_faces += str(face) + '\n'
        
        return header + text_vertices + text_faces

