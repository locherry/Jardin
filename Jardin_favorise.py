import csv

########### FONCTIONS ############
def csvToDic(fic):  
    dico = {
        'qsdf' : ['qzdf', 'qdf']
    }
    # Dictionnaire contenant comme clefs les plantes et
    # comme valeurs la liste des plantes pouvant etre favorisee
    # par la plante designee par la clef.
    # Seuls les arcs non nuls sont retenus ici.        
    with open(fic) as f:
        myReader = csv.reader(f,delimiter = ";")
        sommet = 0
        for row in myReader:
            if row[1] == "favorise" :
                if row[0] not in dico.keys() :
                    dico[row[0]] = []
                dico[row[0]].append(row[2])
    return dico

dico_favorise = csvToDic("./csv/data_arcs.csv")

def BFS_dico_fav (dico_favorise, racine) :
    a_traiter = [racine]
    dico_prec = {}
    dico_prec[racine] = None
    deja_traites = []

    while len(a_traiter) > 0: 
        racine_courante = a_traiter.pop(0)
        deja_traites.append(racine_courante)
        if racine_courante in dico_favorise:
            for elem in dico_favorise[racine_courante]:
                if elem not in deja_traites and elem not in a_traiter:
                    a_traiter.append(elem)
                    dico_prec[elem]=racine_courante
    return dico_prec 

def plus_court_chemin(arrivee,dico_prec):
    s=arrivee 
    chem=[]
    while s!=None:
        chem.insert(0,s)
        s=dico_prec[s]
    return chem

def chemin_entre_2_elem(racine, arrivee):
    BFS = BFS_dico_fav (dico_favorise, racine)
    chemin = plus_court_chemin(arrivee,BFS)
    return chemin

def chemin_entre_2_elem_en_boucle(X, Y):
    chm1 = chemin_entre_2_elem(X, Y)
    chm2 = chemin_entre_2_elem(Y, X)
    chm1.pop()
    return chm1+chm2

##########  PRINCIPAL #############

X = 'pissenlit'
Y = 'potiron'

chemin = chemin_entre_2_elem_en_boucle(X, Y)

print(chemin)

