########### IMPORTS ###########
import csv

########### FONCTIONS ############

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
        for row in myReader:
            if row[0] not in dico.keys() : # si l'elem n'est pas dans le dico, ajouter l'entree correspondante
                dico[row[0]] = row[1]
    return dico

dico_categories = csvToDicCategories("./csv/data_sommets_categories.csv")




def BFS_dico_fav (dico_arcs:dict, racine:str) -> dict:
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
        if racine_courante in dico_arcs.keys():
            if 'favorise' in dico_arcs[racine_courante].keys():
                for elem in dico_arcs[racine_courante]['favorise']:
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




def plus_court_chemin(arrivee:str,dico_prec:dict) -> list|None:
    s=arrivee 
    chem=[]
    
    while s!=None:
        chem.insert(0,s)
        if s in dico_prec.keys():
            s=dico_prec[s]
        else :
            s = None
    if len(chem) == 1:
        var=None
    else:
        var=chem
    return var

# Version classique
def chemin_entre_2_elem(X:str, Y:str) -> list|None:
    """
        Trouve le plus court chemin entre X et Y (le moins de noeuds possible)
    """
    BFS = BFS_dico_fav (dico_arcs, X)
    chemin = plus_court_chemin(Y,BFS)
    return chemin

def chemin_entre_2_elem_en_boucle(X:str, Y:str) -> list|None:
    """
        Trouve le plus court chemin entre X et Y, puis entre Y et X pour renvoyer une boucle
        En utilisant BFS
    """
    chm1 = chemin_entre_2_elem(X, Y)
    chm2 = chemin_entre_2_elem(Y, X)
    if chm1==None or chm2==None:
        result= None
    else:
        chm1.pop()
        result=chm1+chm2
    return result

# Version Dijksrta
def chemin_entre_2_elem_dij(X:str, Y:str) -> list|None:
    """
        Trouve le chemin entre X et Y qui consomme le moins de compost
    """
    distances, dico_prec = dijkstra(dico_arcs, Y)
    chemin = plus_court_chemin(X,dico_prec)
    return chemin

def chemin_entre_2_elem_en_boucle_dij(X:str, Y:str) -> list|None:
    """
        Trouve le plus court chemin entre X et Y, puis entre Y et X pour renvoyer une boucle
        En utilisant dijskarta
    """
    chm1 = chemin_entre_2_elem_dij(X, Y)
    chm2 = chemin_entre_2_elem_dij(Y, X)
    if chm1==None or chm2==None:
        result=None
    else:
        chm1.pop()
        result=chm1+chm2
    return result

##########  AFFICHAGE #############

def affichage (chemin:list, chemin_du_fichier_dot:str)->None :
    def genere_dot (chemin : list, chemin_du_fichier_dot : str) -> None:
        """
            Genere un fichier .dot a partir d'un chemin
            '\n' permet de revenir a la ligne
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

            if chemin[i] not in noeuds_visites : # ecrit les liaisons d'attirance que si c'est la premiere fois que tu rencontres cette plante (pour eviter les doublons)
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
        
        style += f'{tab}node [color = green]\n' #la couleur pour les auxiliaires sera verte 
        for aux in auxiliaires:
            style += f'{tab}"{aux}"\n'
        style += f'{tab}node [color = red]\n' #la couleur pour les nuisibles sera rouge 
        for nui in nuisibles:
            style += f'{tab}"{nui}"\n'
        style += f'{tab}node [color = black]\n' #l'ensemble des éléments de notre recette seront en noir
     
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
            # Ecrit le code dot dans le fichier dot
            fichier.write(contenu_du_fichier_dot)

    def genere_image(chemin_du_fichier_dot:str) -> None:
        """
            permet de generer un image a partir du chemin du fichier dot
            cette fonction execute la commande donnee dans le TP pour generer le graph avec la librairir dot de Graphviz
        """
        commande = f'dot -T png -O {chemin_du_fichier_dot}'
        # deux manieres, ca:
        import subprocess # subprocess permet d'executer un programme externe a python, ici on veut executer la ligne de commande ci dessus
        subprocess.run(commande, shell = True, executable="/bin/bash") # lance un terminal (situé ici : /bin/bash) avec la commande 'commande'
        # ou ca
        # import os
        # os.system(f'dot -T png -O {chemin_du_fichier_dot}')
    
    if chemin!=None: #si le chemin entre les deux plantes choisies pour la recette existe, alors
        genere_dot(chemin, chemin_du_fichier_dot)
        genere_image(chemin_du_fichier_dot)

    else:
        print("Impossible d'afficher le graphique de plus court chemin car le chemin est inexistant!")

