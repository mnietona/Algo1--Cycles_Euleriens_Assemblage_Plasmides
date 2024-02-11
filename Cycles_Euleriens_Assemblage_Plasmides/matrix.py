"""
Nom : Nieto Navarrete
Prenom : Matias
Matricule : 502920

"""

class SparseCSCMatrix:
    
    def __init__(self,reads,k):
        self.reads = reads
        self.k = k
    

    def k_mer(self):
        """ 
        Divise les reads en k-mer
        
        :param vrai: si True on veut les k-mers sommets
        :return: liste de k-mers
        """
        k_mers = set()
        for read in self.reads:
            for i in range(len(read)-(self.k)+1):
                (x,y) = (read[i:(self.k-1)+i],read[i+1:(self.k)+i:])
                k_mers.add((x,y))
        k_mer = [x for x in k_mers]
        return k_mer


    def node(self):
        """
        Liste ou chaque sous liste a comme premier element le sommet 
        et comme second element la liste de ses sommets suivants
        
        :return: liste de node
        """
        k_mer = self.k_mer()
        matrice, historique = [] , []
                
        for i in range(len(k_mer)):
            
            if k_mer[i][0] not in historique:
                historique.append(k_mer[i][0])
                matrice.append([k_mer[i][0],[k_mer[i][1]]])  
            else:
                indice = historique.index(k_mer[i][0])
                matrice[indice][1].append(k_mer[i][1])
                    
        return matrice
                
                
            
            
        
        





        
                        
                    


