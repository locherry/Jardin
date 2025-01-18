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
                poids_favorise : [poids_plante1, poids_plante2, ...]

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
                if row[1] == 'favorise' : # si la plante possede une interaction favorise il cree une clef poids_favorise
                    dico[row[0]]['poids_favorise'] = []
            if row[1] == 'favorise' :
                dico[row[0]]['poids_favorise'].append(row[3])

            dico[row[0]][row[1]].append(row[2])
    return dico

dico_arcs = csvToDicArcs("./csv/data_arcs_poids.csv")

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

def dijkstra (dico_arcs_poids:dict, racine:str) -> dict:
    """
        https://en.wikipedia.org/wiki/Dijkstra's_algorithm


        1. Initialize the graph with the source node to take the value of 0 and all other nodes infinity. Start with the source as the “current node”.
        2. Visit all neighboring nodes of the current node and update their values to the cumulative sum of weights (distances) from the source. 
           If a neighbor’s current value is smaller than the cumulative sum, it stays the same. Mark the “current node” as finished.
        3. Mark the unfinished minimum-value node as the “current node”.
        4. Repeat steps 2 and 3 until all nodes are finished.
    """
    def obtient_min(queue:list[tuple]) -> int :
        """ renvoie l'index du minimum de la liste de priorite"""
        nums = [queue[i] for i in range(len(queue))]
        return nums.index(min(nums))
    
    distances = {}
    dernier_sommet_visite = {} # genere un dico de precedents pour retrouver le chemin d'origine
    distances[racine] = 0
    queue_de_priorite = [(distances[racine], racine)]

    while len(queue_de_priorite) > 0 :
        dist_courante, noeud_courant = queue_de_priorite.pop(obtient_min(queue_de_priorite))
        
        if noeud_courant not in dico_arcs_poids.keys() or 'favorise' not in dico_arcs_poids[noeud_courant].keys() :
            continue

        voisins = dico_arcs_poids[noeud_courant]['favorise']
        poids = dico_arcs_poids[noeud_courant]['poids_favorise']

        if dist_courante > distances[noeud_courant]:
            continue

        for i in range(len(voisins)) :
            distance = dist_courante + int(poids[i])
            if voisins[i] not in distances.keys() :
                distances[voisins[i]] = distance
                dernier_sommet_visite[voisins[i]] = noeud_courant
            elif distance < distances[voisins[i]]:
                dernier_sommet_visite[voisins[i]] = noeud_courant
            queue_de_priorite.append((distance, voisins[i]))
    return distances, dernier_sommet_visite



def plus_court_chemin(arrivee,dico_prec):
    s=arrivee 
    chem=[]
    
    while s!=None:
        chem.insert(0,s)
        if s in dico_prec.keys():
            s=dico_prec[s]
        else :
            s = None
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
# Version Dijksrta
def chemin_entre_2_elem_dij(racine, arrivee):
    distances, dico_prec = dijkstra(dico_arcs, racine)
    chemin = plus_court_chemin(arrivee,dico_prec)
    return chemin

def chemin_entre_2_elem_en_boucle_dij(X, Y):
    chm1 = chemin_entre_2_elem_dij(X, Y)
    chm2 = chemin_entre_2_elem_dij(Y, X)
    chm1.pop()
    return chm1+chm2

##########  AFFICHAGE #############

def affichage (chemin:list, chemin_du_fichier_dot:str)->None :
    def genere_dot (chemin : list, chemin_du_fichier_dot : str) -> None:
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

        noeuds_visites = []

        for i in range(len(chemin)-1):  
            index_de_lelem_favorise = dico_arcs[chemin[i]]['favorise'].index(chemin[i+1])
            poids_de_lelem_favorise = dico_arcs[chemin[i]]['poids_favorise'][index_de_lelem_favorise]

            chemin_en_dot += f'{tab}"{chemin[i]}" -> "{chemin[i+1]}" [label="{poids_de_lelem_favorise}"]\n'

            if chemin[i] not in noeuds_visites :
                if 'attire' in dico_arcs[chemin[i]].keys() :
                    for elem in dico_arcs[chemin[i]]['attire'] :                    
                        arcs_attire += f'{tab}"{elem}" -> "{chemin[i]}" [color=darkgreen, style=dotted]\n'
                        if dico_categories[elem] == 'nuisible' and elem not in nuisibles : nuisibles.append(elem)
                        elif dico_categories[elem] == 'auxiliaire' and elem not in auxiliaires : auxiliaires.append(elem)

                if 'repousse' in dico_arcs[chemin[i]].keys() :
                    for elem in dico_arcs[chemin[i]]['repousse'] :
                        arcs_repousse += f'{tab}"{chemin[i]}" -> "{elem}" [color=crimson, style=dotted]\n'
                        if dico_categories[elem] == 'nuisible' and elem not in nuisibles : nuisibles.append(elem)
                        elif dico_categories[elem] == 'auxiliaire' and elem not in auxiliaires : auxiliaires.append(elem)
            noeuds_visites.append(chemin[i])
        
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
    
    genere_dot(chemin, chemin_du_fichier_dot)
    genere_image(chemin_du_fichier_dot)

##########  PRINCIPAL #############
ingredients = ['genet', 'topinambour', 'pissenlit', 'cassis', 'lin', 'carotte sauvage', 'cumin', 'cerfeuil commun', 'melisse citronnelle', 'groseillier', 'sauge', 'moutarde', 'morelle de balbis', 'ciboulette chinoise', 'anis', 'panais', 'courgette', 'cornichon', 'bourrache officinale', 'sarriette', 'feve', 'melon', 'tournesol', 'echalote', 'thym', 'romarin', 'achillee millefeuille', 'prunier', 'framboisier', 'cerisier', 'rue fetide', 'navet', 'roquette', 'chicoree', 'epinard', 'artichaut', 'persil', 'agrume', 'lavande', 'rosier', 'tanaisie commune', 'courge', 'origan', 'vigne', 'poirier commun', 'trefle blanc', 'mache', 'potiron', 'mais', 'haricot', 'pasteque', 'cosmos', 'tomate', 'basilic', 'fenouil', 'celeri', 'betterave', 'coriandre', 'pois', 'camomille allemande', 'kiwi', 'pomme de terre', 'asperge', 'concombre', 'aneth', 'chou', 'laitue', 'oignon','fraisier des bois', 'souci', 'phacelie', 'pommier', 'ciboulette', 'pecher', 'ail', 'carotte', 'poireau', 'cresson', 'radis']

X = 'pissenlit'
Y = 'potiron'

# X = 'ail'
# Y = 'artichaut'

# X = 'fenouil'
# Y = 'cosmos'

# X = 'basilic'
# Y = "cresson"


chemin = chemin_entre_2_elem_en_boucle(X, Y) #chemin favorise standard
chem2 = chemin_entre_2_elem_en_boucle_dij(X,Y) #chemin favorise avec algo de dijskarta

print(chemin, '\n', chem2)

affichage(chemin, "./graph/graph_simple.dot")
affichage(chem2, "./graph/graph_pondere_dijkstra.dot")
