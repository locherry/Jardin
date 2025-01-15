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

def csvToDicBio(fic:str)->dict:
    """
        renvoie un Dictionnaire contenant comme clefs les plantes et
        comme valeurs la liste des bioindicateurs.
    """
    dico = {}
    
    with open(fic) as f:
        myReader = csv.reader(f,delimiter = ";")
        sommet = 0
        for row in myReader:
            dico[row[0]] = row[1:8]
    return dico

dico_bioindicateurs = csvToDicBio("./csv/data_sommets_bioindicateurs.csv")
# print(dico_bioindicateurs)

def csvToDicFav(fic:str)->dict:  
    dico = {}
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

dico_favorise = csvToDicFav("./csv/data_arcs.csv")

def csvToDicArcs(fic:str)->dict:
    """
        renvoie un dico selon l'architecture suivante :
        dico = {
            plante1 : {
                favorise : [plante1, plante2, ...],
                defavorise : [plante1, plante2, ...],
                attire: [elem1, elem2, ...],
                repousse : [elem1, elem2, ...],
            }
            plante2: {...},
            ...
        }
    """
    dico = {}
    with open(fic) as f:
        myReader = csv.reader(f,delimiter = ";")
        sommet = 0
        for row in myReader:
            if row[0] not in dico.keys() : # si la plante n'est pas dans le dico, ajouter l'entree correspondante
                dico[row[0]] = {}
            if row[1] not in dico[row[0]].keys() : # si l'interaction n'est pas dans le dico de la plante en cours, ajouter l'entree correspondante
                dico[row[0]][row[1]] = []
            dico[row[0]][row[1]].append(row[2])
    return dico

dico_arcs = csvToDicArcs("./csv/data_arcs.csv")

def csvToDicCategories(fic:str)->dict:
    """
        renvoie un dico selon l'architecture suivante :
        dico = {
            elem1 : cat1
            elem1: cat2,
            ...
        }
    """
    dico = {}
    with open(fic) as f:
        myReader = csv.reader(f,delimiter = ";")
        sommet = 0
        for row in myReader:
            if row[0] not in dico.keys() : # si l'elem n'est pas dans le dico, ajouter l'entree correspondante
                dico[row[0]] = row[1]
    return dico

dico_categories = csvToDicCategories("./csv/data_sommets_categories.csv")


# Ebauche d'implementation de filtre pour correspondre aux indicateurs, mais ne fonctionne pas car toutes les plantes ne sont pas renseignees
# def correspond_au_milieu(plante):
#     """
#         correspond_au_milieu est une fonction de 'callback' elle est
#         appellée pour filtrer le dictionaire des favorise
#     """
#     print("pair", dico_bioindicateurs[plante], '\n')
#     # if key in wanted_keys:
#     #     return True  # garde la paire en cours dans le dico filtré
#     # else:
#     #     return False  # supprime la paire du dico filtré
 
# dico_favorise_filtre = dict(filter(correspond_au_milieu, dico_favorise.keys()))




def BFS_dico_fav (dico_favorise:dict, racine:str) -> dict:
    """
        algo de parcours en largeur
    """
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
        # parram = ''
        chemin_en_dot = ''
        arcs_attire = ''
        arcs_repousse = ''
        style = ''
        nuisibles = []
        auxiliaires = []
        for i in range(len(chemin)-1):
            chemin_en_dot += f'{tab}"{chemin[i]}" -> "{chemin[i+1]}"\n'
            # print(dico_arcs[chemin[i]].keys())
            if 'attire' in dico_arcs[chemin[i]].keys() :
                for elem in dico_arcs[chemin[i]]['attire'] :
                    # arcs_attire += f'{tab}"{chemin[i]}" -> "{elem}" [color=darkgreen, style=dotted]\n'
                    arcs_attire += f'{tab}"{elem}" -> "{chemin[i]}" [color=darkgreen, style=dotted]\n'
                    if dico_categories[elem] == 'nuisible' and elem not in nuisibles : nuisibles.append(elem)
                    elif dico_categories[elem] == 'auxiliaire' and elem not in auxiliaires : auxiliaires.append(elem)

            if 'repousse' in dico_arcs[chemin[i]].keys() :
                for elem in dico_arcs[chemin[i]]['repousse'] :
                    arcs_repousse += f'{tab}"{chemin[i]}" -> "{elem}" [color=crimson, style=dotted]\n'
                    if dico_categories[elem] == 'nuisible' and elem not in nuisibles : nuisibles.append(elem)
                    elif dico_categories[elem] == 'auxiliaire' and elem not in auxiliaires : auxiliaires.append(elem)
        
        style += f'{tab}node [color = green]\n'
        for aux in auxiliaires:
            style += f'{tab}"{aux}"\n'
        style += f'{tab}node [color = red]\n'
        for nui in nuisibles:
            style += f'{tab}"{nui}"\n'
        style += f'{tab}node [color = black]\n'
        
        legende = """
    subgraph cluster_01 { 
        node [shape=plaintext]
        key [label=<<table border="0" cellpadding="2" cellspacing="0" cellborder="0">
            <tr><td align="right" port="i1">favorise</td></tr>
            <tr><td align="right" port="i2">attire</td></tr>
            <tr><td align="right" port="i3">repousse</td></tr>
            </table>>]
            key2 [label=<<table border="0" cellpadding="2" cellspacing="0" cellborder="0">
            <tr><td port="i1">&nbsp;</td></tr>
            <tr><td port="i2">&nbsp;</td></tr>
            <tr><td port="i3">&nbsp;</td></tr>
        </table>>]
        key:i1:e -> key2:i1:w [color=black]
        key2:i2:w -> key:i2:e [color=darkgreen, style=dotted]
        key:i3:e -> key2:i3:w [color=crimson, style=dotted]

        node [shape=circle]
    }\n"""
    #     legende = """
    # subgraph cluster1 {
    #     label = "Legende" ;
    #     shape = rectangle ;
    #     color = black ;
    #     a [style=invis] ;
    #     b [style=invis] ;
    #     c [style=invis] ;
    #     d [style=invis] ;
    #     c -> d [label="only ts", style=dashed, fontsize=20] ; 
    #     a -> b [label="ts and js", fontsize=20] ;
    #     gui -> controller [style=invis] ;
    #     view -> model [style=invis] ;
    #     builtins -> utilities [style=invis] ;

    #     gui [style=filled, fillcolor="#ffcccc"] ;
    #     controller [style=filled, fillcolor="#ccccff"] ;
    #     view [style=filled, fillcolor="#ccffcc"] ;
    #     model [style=filled, fillcolor="#ffccff"] ;
    #     builtins [style=filled, fillcolor="#ffffcc"] ;
    #     utilities ;
    #     "external libraries" [shape=rectangle] ;
    # }\n"""
        contenu_du_fichier_dot = 'digraph {\n' + parram + style + chemin_en_dot + arcs_repousse + arcs_attire + legende + '}\n'

        with open(chemin_du_fichier_dot, 'w+') as fichier:
            # Ecris le code dot dans le fichier dot
            fichier.write(contenu_du_fichier_dot)

    def genere_image(chemin_du_fichier_dot:str) -> None:
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
ingredients = ['genet', 'topinambour', 'pissenlit', 'cassis', 'lin', 'carotte sauvage', 'cumin', 'cerfeuil commun', 'melisse citronnelle', 'groseillier', 'sauge', 'moutarde', 'morelle de balbis', 'ciboulette chinoise', 'anis', 'panais', 'courgette', 'cornichon', 'bourrache officinale', 'sarriette', 'feve', 'melon', 'tournesol', 'echalote', 'thym', 'romarin', 'achillee millefeuille', 'prunier', 'framboisier', 'cerisier', 'rue fetide', 'navet', 'roquette', 'chicoree', 'epinard', 'artichaut', 'persil', 'agrume', 'lavande', 'rosier', 'tanaisie commune', 'courge', 'origan', 'vigne', 'poirier commun', 'trefle blanc', 'mache', 'potiron', 'mais', 'haricot', 'pasteque', 'cosmos', 'tomate', 'basilic', 'fenouil', 'celeri', 'betterave', 'coriandre', 'pois', 'camomille allemande', 'kiwi', 'pomme de terre', 'asperge', 'concombre', 'aneth', 'chou', 'laitue', 'oignon','fraisier des bois', 'souci', 'phacelie', 'pommier', 'ciboulette', 'pecher', 'ail', 'carotte', 'poireau', 'cresson', 'radis']

X = 'pissenlit'
Y = 'potiron'

X = 'ail'
Y = 'artichaut'

X = 'fenouil'
Y = 'cosmos'

X = 'basilic'
Y = "cresson"


chemin = chemin_entre_2_elem_en_boucle(X, Y)

print(chemin)

affichage(chemin)


# for i in dico_arcs.keys() :
#     if 'attire' in dico_arcs[i] :
#         for att in dico_arcs[i]['attire']:
#             print(dico_categories[att])
#             if dico_categories[att] == 'nuisible' :
#                 print(i, att)