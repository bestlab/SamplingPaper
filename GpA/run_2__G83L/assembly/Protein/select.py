from MDAnalysis import Universe
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("-s","--selection", default="all")
    parser.add_argument("-c","--center", action="store_true")
    args = parser.parse_args()
    return args

def center(gr): 
    gr.positions = gr.positions - gr.positions.mean(axis=0)
  

def main():
  
    args = parse_args()
    u = Universe(args.input)
    gr = u.selectAtoms(args.selection)
    print(gr)
    if args.center:
        center(gr)    
    gr.write(args.output)
    
    #u = Universe("pore.gro")
    #center(u.atoms)
    #u.atoms.write("pore.gro")
    
if __name__ == "__main__":
    main()