"""
Nom : Nieto Navarrete
Prenom : Matias
Matricule : 502920

"""

from matrix import SparseCSCMatrix


class Graph:
    
    def __init__(self,reads,k):
        self.k = k
        self.reads = reads
        self.matrix = SparseCSCMatrix(self.reads,self.k)
        self.node = self.matrix.node()
        self.arc = self.arcs()
        

    def arcs(self):
        """ Renvoi les arcs du graphe """
        arc = []
        for i in self.node:
            for j in i[1]:
                arc.append((i[0],j))
        return arc
    
    
    def sommet_indegree(self):
        """ Renvovi un sommet de degré non nul """
        if len(self.node[0][1]) < 1: 
            for i in range(len(self.node)):
                if len(self.node[i][1]) > 0 :
                    return self.node[i][0]
        else: 
            return self.node[0][0]

        

   
    
    
    