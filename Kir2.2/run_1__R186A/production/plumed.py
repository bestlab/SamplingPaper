from MDAnalysis import Universe
import numpy as np

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i+n]

def plumed_ids(ag):
    #return  ",".join([str(a.number+1) for a in ag])
    return  "{}-{}".format(ag[0].number + 1, ag[-1].number + 1)

u = Universe("conf.gro")
p = u.select_atoms("protein")
l = u.select_atoms("resname PIP2")

proteins = chunks(p, len(p)//4)
lipids = list(chunks(l, len(l)//4))
lipids = lipids[2], lipids[3], lipids[0], lipids[1]

if False:
    chains = ["A", "B", "C", "D"]
    for p, c in zip(proteins, chains): p.set_segids(c)
    for l, c in zip(lipids, chains): l.set_segids(c)
    u.select_atoms("protein or resname PIP2").write("kir22_together.pdb")

ids = [ plumed_ids(p) for p in proteins ] + [ plumed_ids(l) for l in lipids ]
#print(ids)
header = """#RESTART

WHOLEMOLECULES STRIDE=1 ENTITY0={} ENTITY1={} ENTITY2={} ENTITY3={}
WHOLEMOLECULES STRIDE=1 ENTITY0={} ENTITY1={} ENTITY2={} ENTITY3={}
""".format(*ids )

atoms = """

# protein COMs
pA: COM ATOMS={}
pB: COM ATOMS={}
pC: COM ATOMS={}
pD: COM ATOMS={}

# lipids COMs
lA: COM ATOMS={}
lB: COM ATOMS={}
lC: COM ATOMS={}
lD: COM ATOMS={}

# this is the distance between center of mass a and b
dA: DISTANCE ATOMS=pA,lA
dB: DISTANCE ATOMS=pB,lB
dC: DISTANCE ATOMS=pC,lC
dD: DISTANCE ATOMS=pD,lD

""".format(*ids)

footer = """


drmsA: INTERDRMSD REFERENCE=kir22_together-A.pdb LOWER_CUTOFF=0.1 UPPER_CUTOFF=0.6
drmsB: INTERDRMSD REFERENCE=kir22_together-B.pdb LOWER_CUTOFF=0.1 UPPER_CUTOFF=0.6
drmsC: INTERDRMSD REFERENCE=kir22_together-C.pdb LOWER_CUTOFF=0.1 UPPER_CUTOFF=0.6
drmsD: INTERDRMSD REFERENCE=kir22_together-D.pdb LOWER_CUTOFF=0.1 UPPER_CUTOFF=0.6

#restraint: RESTRAINT ARG=drmsA,drmsB,drmsC,drmsD AT={},{},{},{} KAPPA=1e2,1e2,1e2,1e2
PRINT STRIDE=1000 ARG=* FILE=COLVAR
"""

windows = np.linspace(0.0,2.5,16)
for i, e in enumerate(windows):
	open("plumed.dat".format(i), "w").write(header+atoms+footer.format(windows[i], windows[i], windows[i], windows[i]))
