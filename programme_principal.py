from Jardin_personnalise import chemin_entre_2_elem_en_boucle
from Jardin_personnalise import chemin_entre_2_elem_en_boucle_dij
from Jardin_personnalise import relatif_vers_absolu
from Jardin_personnalise import affichage

##########  PRINCIPAL #############
ingredients = ['genet', 'topinambour', 'pissenlit', 'cassis', 'lin', 'carotte sauvage', 'cumin', 'cerfeuil commun', 'melisse citronnelle', 'groseillier', 'sauge', 'moutarde', 'morelle de balbis', 'ciboulette chinoise', 'anis', 'panais', 'courgette', 'cornichon', 'bourrache officinale', 'sarriette', 'feve', 'melon', 'tournesol', 'echalote', 'thym', 'romarin', 'achillee millefeuille', 'prunier', 'framboisier', 'cerisier', 'rue fetide', 'navet', 'roquette', 'chicoree', 'epinard', 'artichaut', 'persil', 'agrume', 'lavande', 'rosier', 'tanaisie commune', 'courge', 'origan', 'vigne', 'poirier commun', 'trefle blanc', 'mache', 'potiron', 'mais', 'haricot', 'pasteque', 'cosmos', 'tomate', 'basilic', 'fenouil', 'celeri', 'betterave', 'coriandre', 'pois', 'camomille allemande', 'kiwi', 'pomme de terre', 'asperge', 'concombre', 'aneth', 'chou', 'laitue', 'oignon','fraisier des bois', 'souci', 'phacelie', 'pommier', 'ciboulette', 'pecher', 'ail', 'carotte', 'poireau', 'cresson', 'radis']

X = 'pissenlit'
Y = 'potiron'

X = 'ail'
Y = 'ciboulette chinoise'

# X = 'fenouil'
# Y = 'cosmos'

#X = 'basilic'
#Y = 'cresson'


# X = 'betterave'
# Y = 'capucine'

# X = "oeillet d'inde"
# Y = 'asperge'

chemin = chemin_entre_2_elem_en_boucle(X,Y) #chemin favorise standard
affichage(chemin, relatif_vers_absolu("./graph/graph_simple.dot"))
print(chemin)


chem2 = chemin_entre_2_elem_en_boucle_dij(X,Y) #chemin favorise avec algo de dijskarta
affichage(chem2, relatif_vers_absolu("./graph/graph_pondere_dijkstra.dot"))
print(chem2)
