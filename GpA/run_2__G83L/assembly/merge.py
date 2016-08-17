#!/usr/bin/env python

from MDAnalysis import Universe, Merge
import argparse 

parser = argparse.ArgumentParser(description='Demo')
parser.add_argument('-i', '--input', nargs="+")
parser.add_argument('-o', '--output')
args = parser.parse_args()


universes = [Universe(f).atoms for f in  args.input]

#u1 = Universe("frame.gro")
#u2 = Universe("bilayer.gro")

u = Merge(*universes)
u.atoms.write(args.output)


