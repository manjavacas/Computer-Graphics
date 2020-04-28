
#!/usr/bin/env python3

"""
Computer Graphics. Course 2019/2020. ESI UCLM.
Final Project. Antonio Manjavacas.
3D Barplot generator aimed to ease COVID-19 data visualization.
"""

import csv

from sys import argv

from utils import Vertex, Face, Bar
from country import Country

SCALE = 1000 # scale factor

X_SEPARATION = 30 # distance between countries
Y_SEPARATION = 30 # distance between bars
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
        bar_deaths = plot(name, xi, country.deaths, Y_SEPARATION)
        
        # third dimension
        name = country.name + '_recovered'
        bar_recovered = plot(name, xi, country.recovered, Y_SEPARATION * 2)
        
        xi += X_SEPARATION

        bar_groups[country.name] = [bar_cases, bar_deaths, bar_recovered]
    
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

def add_tags():
    pass

"""
Saves the set of barplots into an .obj file
"""
def save_obj(obj_file, bar_groups):

    with open(obj_file, 'w') as f:
        for name in bar_groups:
            f.write(str(bar_groups[name][0]))
            f.write(str(bar_groups[name][1]))
            f.write(str(bar_groups[name][2]))

def run(input_file, output_file):
    
    # Get data from .csv file
    countries = parse_csv(input_file)
    
    # Create barplots from data
    bar_groups = plot_countries(countries)

    # Add country names to barplot
    # add_tags()

    # Generate final .obj file
    save_obj(output_file, bar_groups)

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
