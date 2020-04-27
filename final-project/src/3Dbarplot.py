
#!/usr/bin/env python3

"""
Computer Graphics. Course 2019/2020. ESI UCLM.
Final Project. Antonio Manjavacas.
3D Barplot generator aimed to ease COVID-19 data visualization.
"""

import csv

from sys import argv

from utils import Vector, Vertex, Face
from country import Country

"""
Get list of countries and their stats from .csv file
"""
def parse_csv(csv_file):

    countries = []

    with open(csv_file, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader, None)  # skip header
        for row in reader:
            countries.append(Country(
                name=row[0],
                cases=row[1], 
                deaths=row[2],
                recovered=row[3]))

    return countries

def plot(countries):
    pass

def add_tags():
    pass

def save_obj(obj_file):
    pass

def run(input_file, output_file):
    
    # Get data from .csv file
    countries = parse_csv(input_file)
    
    # Create barplots from data
    plot(countries)

    # Add country names to barplot
    add_tags()

    # Generate final .obj file
    save_obj(output_file)

if __name__ == '__main__':
    if len(argv) != 3:
        print('Usage: ./3Dbarplot <input.csv> <output.obj>')
        exit()
    elif argv[1].endswith('.csv') and argv[2].endswith('.obj'):
        print('\n================ CREATING 3D BARPLOTS ================\n')
        run(argv[1], argv[2])
        print('\nDone and saved in ' + argv[2])
        print('\n======================================================\n')
    else:
        print('Error: input must be a .csv file and output file be an .obj file')
        exit()
