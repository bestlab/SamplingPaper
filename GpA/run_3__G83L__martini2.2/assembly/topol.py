#!/usr/bin/env python
from MDAnalysis import Universe
import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input", default="conf.gro")
    args = parser.parse_args()
    return args

args = parse_args()

u = Universe(args.input)

import glob


template = """

; Include forcefield parameters
#include "martini_v2.2.itp"
#include "martini_v2.0_POPC_02.itp"
#include "martini_v2.2_aminoacids.itp"

{include}

[ system ]
; Name
TMs in DPPC bilayer

[ molecules ]
{topology}
"""

include, topology = [], []


if True:
    topology.append(("Protein_A", 1))
    include.append("Protein_A.itp")

if True:
    topology.append(("Protein_B", 1))
    include.append("Protein_B.itp")

gr = u.selectAtoms("resname POPC and name PO4")
if len(gr):
    topology.append(("POPC", len(gr)))

gr = u.selectAtoms("resname W")
if len(gr):
    topology.append(("W", len(gr)))



include_str = ['#include "./{0}"'.format(i) for i in include]
topology_str = ["{0}\t{1}".format(name, count) for name, count in topology]

print template.format(**{"topology": "\n".join(topology_str),
                       "include": "\n".join(include_str)})
