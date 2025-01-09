########### IMPORTS ###########
import csv

########### INITIALISATION ########

milieu = {
    "lumiere" : {
        'valeur' : 8,
        'delta' : 2
    },
    "temperature" : {
        'valeur' : 7, #1 tres froid a 9 tres chaud
        'delta' : 1.5
    },
    "humidite" : {
        'valeur' : 7,
        'delta' : 1.5
    },
    "PH" : {
        'valeur' : 4, # de 1 a 9
        'delta' : 2
    },
    "niveau trophique" : {
        'valeur' : 4, 
        'delta' : .5
    },
    "texture" : {
        'valeur' : 4.5, 
        'delta' : 0.5
    },
    "matiere organique" : {
        'valeur' : 9,
        'delta' : 0.5
    },
}

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

def BFS_dico_fav (dico_favorise:dict, racine:str) -> dict:
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

##########  AFFICHAGE #############

def affichage (chemin:list)->None :
    def genere_dot (chemin : list, chemin_du_fichier_dot:str) -> None:
        """
            Genere un fichier .dot a partir d'un chemin
            '\\n' permet de revenir a la ligne
        """
        tab = '    '
        parram =  tab + 'layout="circo"\n'
        chemin_en_dot = ''
        for i in range(len(chemin)-1):
            chemin_en_dot += f'{tab}"{chemin[i]}" -> "{chemin[i+1]}"\n'
        
        contenu_du_fichier_dot = 'digraph {\n' + parram + chemin_en_dot + '}\n'

        with open(chemin_du_fichier_dot, 'w+') as fichier:
            # Ecris le code dot dans le fichier dot
            fichier.write(contenu_du_fichier_dot)

    def genere_image(chemin_du_fichier_dot:str) -> None:
        """
            |!| Ne marche pas dans le terminal de vs code, il faut l'executer avec un terminal externe (jsp pourquoi)
        """
        command = f'dot -T png -O {chemin_du_fichier_dot}'
        # deux manieres, ca:
        import subprocess
        subprocess.run(command, shell = True, executable="/bin/bash")
        # ou ca
        # import os
        # os.system(f'dot -T png -O {chemin_du_fichier_dot}')
    
    chemin_du_fichier_dot = "./graph/graph.dot"
    genere_dot(chemin, chemin_du_fichier_dot)
    genere_image(chemin_du_fichier_dot)

##########  PRINCIPAL #############

X = 'pissenlit'
Y = 'potiron'

chemin = chemin_entre_2_elem_en_boucle(X, Y)

print(chemin)

affichage(chemin)
