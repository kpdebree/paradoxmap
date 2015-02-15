# -*- coding: utf-8 -*-

"""This script parses culture related data
Folders to check:
/history/provinces
"""
from os import listdir, path
import time, re, json

def read_culture_colours():
    start = time.clock()

    colours = {}

    f = open("00_cultures.txt")
    graph_re = re.compile('graphical')
    curly_re = re.compile('\s}')
    color_re = re.compile('color');

    for line in f:
        tabs = len(line) - len(line.lstrip('\t'))
        colour = None
        if tabs == 1 and not re.search(graph_re, line) and not re.match(curly_re, line):
            tmp = line.split(' = ')
            culture = tmp[0].strip()

        if tabs == 2 and re.search(color_re, line):
            tmp = line.split(' = ')
            s = tmp[1].strip()
            s = s.strip('{} ')
            cl = s.split(' ')
            colour = "rgb("
            colour = colour + str((int(255 * float(cl[0]))))
            colour = colour + "," + str((int(255 * float(cl[1]))))
            colour = colour + "," + str((int(255 * float(cl[2])))) + ")"

        if colour is not None:
            colours[culture] = colour

    with open('cultures_and_religions.js', 'w') as f:
        f.write("var culture_colours = ") 
        json.dump(colours, f, separators=(',',':'))

    delta = time.clock() - start
    print ("Culture colour parsing took %.3f seconds" %delta)

def read_cultures():
    start = time.clock()

    cult_re = re.compile('culture')
    
    cultures = {}

    for prov in listdir("history/provinces"):
        prov_id = int((prov.split(' '))[0])
        provp = path.join("history/provinces", prov)

        f = open(provp)

        culture = None

        for line in f:

            if re.search(cult_re, line):
                tmp = line.split(' = ')
                tmp = tmp[1].split('#')
                culture = tmp[0].strip()
                break

        if culture is not None:
            cultures[prov_id] = culture

    with open('cultures_and_religions.js', 'a') as f:
        f.write(";var cultures = ") 
        json.dump(cultures, f, separators=(',',':'))

    delta = time.clock() - start
    print ("Culture parsing took %.3f seconds" %delta)

def read_religions():
    start = time.clock()

    reli_re = re.compile('religion')
    
    religions = {}

    for prov in listdir("history/provinces"):
        prov_id = int((prov.split(' '))[0])
        provp = path.join("history/provinces", prov)

        f = open(provp)

        religion = None

        for line in f:

            if re.search(reli_re, line):
                tmp = line.split(' = ')
                tmp = tmp[1].split('#')
                religion = tmp[0].strip()
                break

        if religion is not None:
            religions[prov_id] = religion

    with open('cultures_and_religions.js', 'a') as f:
        f.write(";var religions = ") 
        json.dump(religions, f, separators=(',',':'))

    delta = time.clock() - start
    print ("Religion parsing took %.3f seconds" %delta)
                        
def generate():
    read_culture_colours()
    read_cultures()
    read_religions()

if __name__ == "__main__":
    start = time.clock()
    generate()
    delta = time.clock() - start
    print ("Generating cultures.js took %.3f seconds" %delta)
