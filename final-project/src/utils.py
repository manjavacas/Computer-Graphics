
"""
Computer Graphics. Course 2019/2020. ESI UCLM.
Final Project. Antonio Manjavacas.
3D Utils: Vertex, Vector and Face classes
"""

from math import pow, sqrt

class Vertex:
    def __init__(self, id, x, y, z):
        self.id = id
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return 'v' + ' ' + str(self.x) + ' ' + str(self.y) + ' ' + str(self.z)

    def __eq__(self, v):
        if isinstance(v, Vertex):
            return self.x == v.x and self.y == v.y and self.z == v.z
        else:
            return False


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.module = sqrt(pow(self.x, 2) + pow(self.y, 2) + pow(self.z, 2))


class Face:
    def __init__(self, v1, v2, v3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.vertices = [v1, v2, v3]

        a = Vector(v2.x - v1.x, v2.y - v1.y, v2.z - v1.z)

        b = Vector(v3.x - v1.x, v3.y - v1.y, v3.z - v1.z)

        n = Vector((a.y * b.z - a.z * b.y),
                   (a.z * b.x - a.x * b.z),
                   (a.x * b.y - a.y * b.x))

        self.normal = Vector(n.x/n.module, n.y/n.module, n.z/n.module)

    def __str__(self):
        return 'f' + ' ' + str(self.v1.id) + ' ' + str(self.v2.id) + ' ' + str(self.v3.id)

    def __eq__(self, f):
        if isinstance(f, Face):
            other_vertices = [f.v1, f.v2, f.v3]
            return (self.v1 in other_vertices and
                    self.v2 in other_vertices and
                    self.v3 in other_vertices)
        else:
            return False