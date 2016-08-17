from MDAnalysis import Universe
from MDAnalysis.analysis.distances import self_distance_array, distance_array, contact_matrix
import numpy as np
import pandas as pd
import glob, sys

u = Universe("conf.gro")
gr = u.select_atoms("protein and resid 4-27")
gr1 = gr[:len(gr)/2]
gr2 = gr[len(gr)/2:]
print(gr1, gr2)

header = """#RESTART

WHOLEMOLECULES STRIDE=1 ENTITY0={} ENTITY1={}
""".format(  ",".join([str(a.number+1) for a in gr1]), ",".join([str(a.number+1) for a in gr2]) )

atoms = """
a: COM ATOMS={}
b: COM ATOMS={}

t: TORSION ATOMS={},{},{},{}

# this is the distance between center of mass a and b
d: DISTANCE ATOMS=a,b


""".format(",".join([str(a.number+1) for a in gr1]),
	   ",".join([str(a.number+1) for a in gr2]),
			  gr1[0].number + 1,
			  gr1[-1].number +1 ,
			  gr2[0].number +1 ,
			  gr2[-1].number +1)

footer = """
#drmsA: DRMSD REFERENCE=gpa_together_bb-A.pdb LOWER_CUTOFF=0.1 UPPER_CUTOFF=0.8
#drmsB: DRMSD REFERENCE=gpa_together_bb-B.pdb LOWER_CUTOFF=0.1 UPPER_CUTOFF=0.8
#restr: RESTRAINT ARG=drmsA,drmsB KAPPA=1e3,1e3

#drms: INTERDRMSD REFERENCE=gpa_together_tm.pdb LOWER_CUTOFF=0.1 UPPER_CUTOFF=0.6
restraint: RESTRAINT ARG=d AT={} KAPPA=1e2
PRINT STRIDE=1000 ARG=* FILE=COLVAR
"""

# 0.9 nm is the native helix-helix distance
windows = np.linspace(0.9,0.9,2)
for i, e in enumerate(windows):
	open("plumed.{}.dat".format(i), "w").write(header+atoms+footer.format(windows[i]))
