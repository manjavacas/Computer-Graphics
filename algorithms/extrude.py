#!/usr/bin/env python

# Extrusion algorithm implementation
# Usage: ./extrude <input.obj> <output.obj> <length>
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


def apply_extrusion(vertices, faces, length):

    global ID_COUNTER

    new_vertices = []
    new_faces = []

    for face in faces:

        # Translation vector
        t = Vector(length * face.normal.x,
                   length * face.normal.y,
                   length * face.normal.z)

        # Transformation matrix
        TM = [[1, 0, 0, t.x],
              [0, 1, 0, t.y],
              [0, 0, 1, t.z],
              [0, 0, 0, 1]]

        # GENERATE NEW VERTICES
        new_face_vertices = []

        for v in face.vertices:

            vertex = [v.x, v.y, v.z, 1]
            new_vertex_coords = [0, 0, 0, 0]

            for i in range(len(TM)):
                for j in range(len(TM[0])):
                    new_vertex_coords[i] += TM[i][j] * vertex[j]

            new_vertex = Vertex(
                None, new_vertex_coords[0], new_vertex_coords[1], new_vertex_coords[2])

            # Check if the vertex was already created
            if new_vertex not in new_vertices:
                new_vertex.id = ID_COUNTER
                ID_COUNTER += 1
                new_vertices.append(new_vertex)
            else:
                new_vertex = [v for v in new_vertices if v == new_vertex][0]

            new_face_vertices.append(new_vertex)

        # GENERATE NEW FACES
        v1 = face.v1
        v2 = face.v2
        v3 = face.v3

        new_v1 = new_face_vertices[0]
        new_v2 = new_face_vertices[1]
        new_v3 = new_face_vertices[2]

        # New frontal face
        new_face = Face(new_v1, new_v2, new_v3)
        if new_face not in new_faces:
            new_faces.append(new_face)

        # Additional lateral faces
        new_faces.append(Face(v1, v2, new_v2))
        new_faces.append(Face(v1, new_v1, new_v2))
        new_faces.append(Face(v2, v3, new_v3))
        new_faces.append(Face(v2, new_v2, new_v3))
        new_faces.append(Face(v1, v3, new_v3))
        new_faces.append(Face(v1, new_v1, new_v3))

    return new_vertices, new_faces


def create_output(vertices, faces, output_file):

    with open(output_file, 'w') as file:
        file.write(FILE_HEADER)
        file.write(OBJ_NAME)

        for v in vertices:
            file.write(str(v) + '\n')

        file.write(SMOOTH_SHADING)

        for f in faces:
            file.write(str(f) + '\n')


def extrude(input_file, output_file, length):

    # Get data from .obj file
    vertices, faces = parse_obj(input_file)

    # Apply extrusion
    new_vertices, new_faces = apply_extrusion(vertices, faces, length)

    vertices += new_vertices
    faces += new_faces

    # Generate new .obj file
    create_output(vertices, faces, output_file)


if __name__ == '__main__':
    if len(argv) != 4:
        print('Usage: ./extrude <input.obj> <output.obj> <length>')
        exit()
    elif argv[1].endswith('.obj') and argv[2].endswith('.obj'):
        try:
            length = float(argv[3])
        except:
            print('Error: third argument must be a number')
            exit()
        print('\n================ EXTRUSION ================\n')
        print('Extruding ' + argv[1] + ' with length = ' + argv[3] + ' ...')
        extrude(argv[1], argv[2], length)
        print('\nDone! Mesh saved in ' + argv[2])
        print('\n===========================================\n')
    else:
        print('> Error: input and output files must have .obj extension')
        exit()
