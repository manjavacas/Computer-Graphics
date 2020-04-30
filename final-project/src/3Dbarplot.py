#!/usr/bin/env python3

"""
Computer Graphics. Course 2019/2020. ESI UCLM.
Final Project. Antonio Manjavacas.
3D Barplot generator aimed to ease COVID-19 data visualization.
"""

import csv

from sys import argv

from utils import Vertex, Face, Letter_face, Tag, Bar
from country import Country


PATH_LETTERS = './letters/'

SCALE = 1000 # scale factor

COUNTRY_SEPARATION = 30 # distance between countries
BAR_SEPARATION = 30 # distance between bars
LETTER_SEPARATION = 10 # distance between letters

WIDTH = 10 # bar width

"""
Gets the list of countries and their stats from .csv file
"""
def parse_csv(csv_file):

    countries = []

    with open(csv_file, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader, None)  # skip header
        for row in reader:
            countries.append(Country(
                name=row[0],
                cases=float(row[1])/SCALE, 
                deaths=float(row[2])/SCALE,
                recovered=float(row[3])/SCALE))

    return countries

"""
Generates cases, deaths and recovered plots for each country
"""
def plot_countries(countries):

    xi = 0

    bar_groups = {}

    for country in countries:

        # first dimension
        name = country.name + '_cases'
        bar_cases = plot(name, xi, country.cases, 0)

        # second dimension
        name = country.name + '_deaths'
        bar_deaths = plot(name, xi, country.deaths, BAR_SEPARATION)
        
        # third dimension
        name = country.name + '_recovered'
        bar_recovered = plot(name, xi, country.recovered, BAR_SEPARATION * 2)

        # add country names to barplot
        tag = add_tag(country.name, xi, BAR_SEPARATION * 3)

        bar_groups[country.name] = [bar_cases, bar_deaths, bar_recovered, tag]

        xi += COUNTRY_SEPARATION

    return bar_groups

"""
Generates a single named barplot
"""
def plot(name, x, y, z):

    bar_faces = []

    v1 = Vertex(x, 0, z)
    v2 = Vertex(x + WIDTH, 0, z)
    v3 = Vertex(x + WIDTH, 0, z + WIDTH)
    v4 = Vertex(x, 0, z + WIDTH)

    v5 = Vertex(x, y, z)
    v6 = Vertex(x + WIDTH, y, z)
    v7 = Vertex(x + WIDTH, y, z + WIDTH)
    v8 = Vertex(x, y, z + WIDTH)

    # Lower face   
    bar_faces.append(Face(v1,v2,v3,v4))

    # Top face
    bar_faces.append(Face(v5,v6,v7,v8))
    
    # Side faces
    bar_faces.append(Face(v1,v5,v8,v4))
    bar_faces.append(Face(v3,v7,v8,v4))
    bar_faces.append(Face(v2,v6,v7,v3))
    bar_faces.append(Face(v2,v1,v5,v6))

    return Bar(name, bar_faces)

"""
Add a named tag to identify the barplot
"""
def add_tag(name, x, z):

    tag = Tag(name,[],[])

    i = 1
    letters = name[::-1]

    for letter in letters:
        
        # load letter getting its vertices and triangular faces
        letter_obj = PATH_LETTERS + letter.upper() + '.obj'
        letter_vertices, letter_faces = parse_obj(letter_obj)

        # apply vertex offset
        for vertex in letter_vertices:
            vertex.x += x
            vertex.z += z + i * LETTER_SEPARATION
        
        # add letter vertices and faces to tag
        tag.vertices.extend(letter_vertices)
        tag.faces.extend(letter_faces)

        i += 1

    return tag

"""
Parses an .obj file returning letter vertices and faces
"""
def parse_obj(obj_file):

    vertices = []
    faces = []

    # start from latest vertext id
    starting_id = Vertex.id - 1

    with open(obj_file, 'r') as f:
        for line in f:
            words = line.split()
            if words[0] == 'v':
                vertices.append(
                    Vertex(float(words[1]), float(words[2]), float(words[3])))
            elif words[0] == 'f':
                v1 = int(words[1]) + starting_id
                v2 = int(words[2]) + starting_id
                v3 = int(words[3]) + starting_id
                faces.append(Letter_face(v1, v2, v3))

    return vertices, faces

"""
Saves the set of barplots into an .obj file
"""
def save_obj(obj_file, countries, bar_groups):

    with open(obj_file, 'w') as f:
        for country in countries:
            f.write(str(bar_groups[country.name][0]))
            f.write(str(bar_groups[country.name][1]))
            f.write(str(bar_groups[country.name][2]))
            f.write(str(bar_groups[country.name][3]))

def run(input_file, output_file):
    
    # Get data from .csv file
    countries = parse_csv(input_file)
    
    # Create barplots from data
    bar_groups = plot_countries(countries)

    # Generate final .obj file
    save_obj(output_file, countries, bar_groups)

if __name__ == '__main__':
    if len(argv) != 3:
        print('Usage: ./3Dbarplot <input.csv> <output.obj>')
        exit()
    elif argv[1].endswith('.csv') and argv[2].endswith('.obj'):
        print('\n================ CREATING 3D BARPLOTS ================\n')
        run(argv[1], argv[2])
        print('Done and saved in ' + argv[2])
        print('\n======================================================\n')
    else:
        print('Error: input must be a .csv file and output file be an .obj file')
        exit()
