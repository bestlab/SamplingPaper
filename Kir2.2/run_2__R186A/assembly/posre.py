from MDAnalysis import Universe

u = Universe("conf.gro")

atoms = [a.number+1 for a in u.select_atoms("name BB")]

lines = [ " {}   1   100    100     0".format(a) for a in atoms ]

data = """
[ position_restraints ]
;  i funct       fcx        fcy        fcz
{}
""".format("\n".join(lines))

open("posres_protein-cg.itp","w").write(data)
