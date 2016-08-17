#!/usr/bin/env python 

from MDAnalysis import Universe
import argparse

parser = argparse.ArgumentParser(description='Demo')
parser.add_argument("input_file")
parser.add_argument("output_file")

args = parser.parse_args()

protein = Universe(args.input_file)  
protein.atoms.align_principalAxis(0, [0,0,1])
protein.atoms.positions = protein.atoms.positions - protein.atoms.positions.mean(axis=0) 
protein.atoms.write(args.output_file)

