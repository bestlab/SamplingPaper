import numpy as np
header = """
#RESTART

pro: COM ATOMS=48,292,499
card: COM ATOMS=645

d1: DISTANCE ATOMS=pro,card
d2: DISTANCE ATOMS=pro,card COMPONENTS
"""

footer = """

posre: RESTRAINT ARG=d2.y AT=0.248333 KAPPA=1000.0

restraint: RESTRAINT ARG=d1 AT={} KAPPA=1000.0
PRINT STRIDE=1000 ARG=* FILE=COLVAR
"""
centers = np.linspace(1.6,4.5,32)
nwindows=32
for i, e in enumerate(range(nwindows)):
	open("plumed.dat.{}".format(i), "w").write(header + footer.format(centers[i]))
