"""
Nom : Nieto Navarrete
Prenom : Matias
Matricule : 502920

Projet INFO-F103 : Cycles eulériens et assemblage de plasmides

Le programme se lance avec la ligne de commande : python3 projet3.py -f <fichier> -k <k>

Bonus :
    > python3 projet3.py -f bonus_reads.txt -k 10
    > Taille du plasmide : 26 086
    
    J'ai remarqué que pour le plasmide pBR322 et pUC19. Que pour k = 14, j'obtenais leurs tailles exactes.
    Mais si j'augmentais le k, j'obtenais aussi leurs bonnes tailles. 
    Donc j'ai écrit un code pour verifier cette hypothèse.
    Ensuite après avoir vérifié l'hypothèse, je l'ai testée sur le bonus et j'ai obtenu 26 086.
    Voir ligne 146.

       
Remarque :
    Je n'ai pas utilisé de liste chainée dans ma class SpareCSCMatric() car je ne parvenais pas à la visualiser.
    J'ai donc créé la class SpareceCSCMatrix() à l'aide de listes classiques.
    
"""

import argparse
from graph import Graph


class Stack:
    
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        self.items.pop()

    def len(self):
        return len(self.items)
    
    def top(self):
        return self.items[-1]
 
    
def arg():
    parse = argparse.ArgumentParser()
    parse.add_argument("-f", "--fichier", help="fichier de reads")
    parse.add_argument("-k", "--k", help="k-graphe")
    fichier = parse.parse_args().fichier
    k = parse.parse_args().k
    return fichier,int(k)

def  load_reads(path):
    """
    Renvoi une liste contenant les reads du fichier
    
    :param path: chemin du fichier reads
    :return: liste des reads
    """
    with open(path, 'r') as f:
        reads = [line.strip() for line in f]
    return reads

def construct_graph(reads, k):
    """
    Construit le graphe des reads
    
    :param reads: liste retourner par load_reads
    :param k: un entier 
    :return: instance de G
    """
    return Graph(reads,k)

def eulerian_cycle(G):
    """
    Renvoi le cycle eulerian de G
    
    :param G: instance de Graph()
    :return: cycle eulerian
    """
    
    v = G.sommet_indegree() 
    P = []
    S = Stack()
    S.push(v)
    
    while S.len() != 0:
        v = S.top()
        
        for (u,y) in G.arc:
            if y == v:
                G.arc.remove((u,y))
                S.push(u)
                break
        else:
            S.pop()
            if S.len() > 0:
                P.append(v)
        
    return P
     
def reconstruct_plasmid(cycle):
    """
    Construit le plasmid à partir du cycle eulerian
    
    :param cycle: cycle eulérien
    :return: str
    """
    plasmid = ""
    for i in cycle:
        plasmid += i[0]
    return plasmid

def verifie(mon_str,fichier):
    """ Verifie si le plasmide trouver corespond à celui du fichier """
    
    fichier_test = fichier.replace("_reads", "")
    son_str = load_reads(fichier_test)[2]
    if len(mon_str) != len(son_str):
        return False
    for i in range(len(mon_str)):
        mon_str = mon_str[-1] + mon_str[:-1]
        if mon_str == son_str:
            return True
    return False


if __name__ == "__main__":

    fichier,k = arg()
    if fichier == None or k == None:
        print("Erreur : fichier ou k non renseigné")
        exit(1)
    

    reads = load_reads(fichier)
    G = construct_graph(reads, k)
    cycle = eulerian_cycle(G)
    plasmide = reconstruct_plasmid(cycle)
    print(plasmide)

    """ Code Bonus
    if fichier == 'bonus_reads.txt': # trouve la taille exacte du plasmide du bonus
        taille = set()
        for i in range(k,90,10):

            reads = load_reads(fichier)
            G = construct_graph(reads, i)
            cycle = eulerian_cycle(G)
            plasmide = reconstruct_plasmid(cycle)
            taille_p = len(plasmide)
            
            if taille_p in taille:
                len_plasmide = len(plasmide)
                
            else:
                taille.add(taille_p)
        
        print(f"Taille du plasmide : {len_plasmide}") 

    else: # m'a permis de verifier mon hypothese
        taille = set()
        for i in range(k,90,2):
            reads = load_reads(fichier)
            G = construct_graph(reads, i)
            cycle = eulerian_cycle(G)
            plasmide = reconstruct_plasmid(cycle)
            taille_p = len(plasmide)
            if taille_p in taille:
                len_plasmide = len(plasmide)
            else:
                taille.add(taille_p)
        
            print(f"plasmide trouvé : {verifie(plasmide,fichier)}, taille k = {i}")
            
        print(f"Taille du plasmide : {len_plasmide}") # taille exacte du plasmide
    """