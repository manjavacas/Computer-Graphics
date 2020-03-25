#!/usr/bin/env python

# Spin algorithm implementation
# Usage: ./spin <input.obj> <output.obj> <steps> <angle> <X/Y/Z>
# Antonio Manjavacas


from sys import argv
from math import pow, sqrt

FILE_HEADER = ''
OBJ_NAME = ''
SMOOTH_SHADING = ''

ID_COUNTER = 1


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


def create_output(vertices, faces, output_file):

    with open(output_file, 'w') as file:
        file.write(FILE_HEADER)
        file.write(OBJ_NAME)

        for v in vertices:
            file.write(str(v) + '\n')

        file.write(SMOOTH_SHADING)

        for f in faces:
            file.write(str(f) + '\n')

def parse_obj(obj_file):

    global ID_COUNTER
    global FILE_HEADER
    global OBJ_NAME
    global SMOOTH_SHADING

    vertices = []
    faces = []

    with open(obj_file) as file:
        for line in file:
            words = line.split()
            if words[0] == 'v':
                vertices.append(
                    Vertex(ID_COUNTER, float(words[1]), float(words[2]), float(words[3])))
                ID_COUNTER += 1
            elif words[0] == 'f':
                v1 = [v for v in vertices if v.id == int(words[1])][0]
                v2 = [v for v in vertices if v.id == int(words[2])][0]
                v3 = [v for v in vertices if v.id == int(words[3])][0]
                faces.append(Face(v1, v2, v3))
            elif words[0] == '#':
                FILE_HEADER += line
            elif words[0] == 'o':
                OBJ_NAME = line
            elif words[0] == 's':
                SMOOTH_SHADING = line

    return vertices, faces

def apply_spin(vertices, faces, steps, angle, axis):
    # TODO
    pass


def spin(input_file, output_file, steps, angle, axis):
    
    # Get data from .obj file
    vertices, faces = parse_obj(input_file)

    # Apply spin
    new_vertices, new_faces = apply_spin(vertices, faces, steps, angle, axis)

    vertices += new_vertices
    faces += new_faces

    # Generate new .obj file
    create_output(vertices, faces, output_file)


if __name__ == '__main__':
    if len(argv) != 6:
        print('Usage: ./spin <input.obj> <output.obj> <steps> <angle> <axis>')
        exit()
    elif argv[1].endswith('.obj') and argv[2].endswith('.obj'):
        try:
            steps = int(argv[3])
            angle = float(argv[4])
        except:
            print('Error: step and angle arguments must be numbers')
            exit()

        if argv[5] in ['X','Y','Z']:
            axis = argv[5]
        else:
            print('Error: axis argument must be one of the following: X, Y ,Z')
            exit()
        
        print('\n================ SPIN ================\n')
        print('Spinning ' + argv[1] + '...\nSteps: ' + steps + '\nAngle: ' + angle + '\nAxis: ' + axis)
        spin(argv[1], argv[2], steps, angle, axis)
        print('\nDone! Mesh saved in ' + argv[2])
        print('\n======================================\n')
    else:
        print('Error: input and output files must have .obj extension')
        exit()
