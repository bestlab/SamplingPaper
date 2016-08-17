from MDAnalysis import Universe
import numpy as np

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i+n]

def plumed_ids(ag):
    #return  ",".join([str(a.number+1) for a in ag])
    return  "{}-{}".format(ag[0].number + 1, ag[-1].number + 1)

def scramble(ag):
    #return ag[1], ag[2], ag[0], ag[3]
    return ag[3], ag[1], ag[2], ag[0]

u = Universe("conf.gro")
p = u.select_atoms("protein")
l = u.select_atoms("resname PIP2")
h = u.select_atoms("resname PIP2 and (name PO* or name RP*)")

# split into chunks
proteins = list(chunks(p, len(p)//4))
lipids = list(chunks(l, len(l)//4))
headgroups = list(chunks(h, len(h)//4))

# reorder
lipids = scramble(lipids)
headgroups = scramble(headgroups)

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

ids = [ plumed_ids(p) for p in proteins ] + [ plumed_ids(h) for h in headgroups ]

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

cA: DISTANCE ATOMS=pA,lA COMPONENTS
cB: DISTANCE ATOMS=pB,lB COMPONENTS
cC: DISTANCE ATOMS=pC,lC COMPONENTS
cD: DISTANCE ATOMS=pD,lD COMPONENTS

#posre: RESTRAINT ARG=cA.x,cB.y,cC.x,cD.y AT=1.4,1.4,-1.4,-1.4 KAPPA=1e2,1e2,1e2,1e2

""".format(*ids)

footer = """

#drmsA: INTERDRMSD REFERENCE=kir22_together-A.pdb LOWER_CUTOFF=0.1 UPPER_CUTOFF=0.6
#drmsB: INTERDRMSD REFERENCE=kir22_together-B.pdb LOWER_CUTOFF=0.1 UPPER_CUTOFF=0.6
#drmsC: INTERDRMSD REFERENCE=kir22_together-C.pdb LOWER_CUTOFF=0.1 UPPER_CUTOFF=0.6
#drmsD: INTERDRMSD REFERENCE=kir22_together-D.pdb LOWER_CUTOFF=0.1 UPPER_CUTOFF=0.6

#restraint: RESTRAINT ARG=dA,dB,dC,dD AT={},{},{},{} KAPPA=1e2,1e2,1e2,1e2
PRINT STRIDE=1000 ARG=* FILE=COLVAR
"""

windows = np.linspace(3.0,3.0+1.5,16)
for i, e in enumerate(windows):
	open("plumed.dat".format(i), "w").write(header+atoms+footer.format(windows[i], windows[i], windows[i], windows[i]))
