# Auteurs: Samuel Pellerin
# Date: 1 décembre 2023.
#
# Ce programme constitue en une application Web qui implémente le jeu
# "Addiction Solitaire". Le but du jeu est d'ordonner les cartes de 2 à K (le 
# roi) sur chaque rangée, et ce, pour chaque couleur. Les as sont représentés
# par des cases vides, soit des cases où l'on peut déplacer d'autres cartes. 
# Les cartes que l'on peut déplacer sont coloriées en vert. Le joueur a le 
# droit de brasser les cartes non-ordonnées 3 fois dans la partie. Si le joueur
# n'a pas pu ordonner les cartes, qu'il n'a plus de brassage et qu'il ne peut
# plus déplacer de cartes, il a perdu. 


###############################################################################

# Importation des modules utilisés dans le programme.
import math
import random


###############################################################################

# Définition du style de la page web. On définit les paramètres de style reliés
# au jeu de carte qui sera affiché à l'écran.
css = """
    <style>
    #jeu table { float:none; }
    #jeu table td { border:0; padding:1px 2px; height:auto; width:auto; }
    #jeu table td img { height:140px; }
    </style>"""

# Définition de tableaux contenant les valeurs et les couleurs possibles pour
# les cartes. On associe les noms selon l'appellation des cartes en anglais et
# on définit l'as comme la valeur 'absent' puisque l'as ne sera pas affiché à
# l'écran.
valeurTab = ["absent", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q",\
"K"]
couleurTab = ["H", "D", "S", "C"]


###############################################################################

# La fonction trouverIndex prend en paramètre un élément du jeu de carte, et
# renvoie l'index auquel se trouve l'élément dans le jeu. Elle renvoit la
# valeur -1 si l'élément n'est pas trouvé
def trouverIndex(tab, element):
    for i in range(len(tab)):
        if tab[i] == element:
            return i
    return -1


###############################################################################

# La procédure modifierHTML prend un message en argument et modifie le contenu
# du message1 (Message relié au brassage des cartes et autres évènements) qui
# est affiché sur le site Web. Elle initialise également le reste de la page,
# soit la grille de cartes et le message2 (Le bouton nouvelle partie).
def modifierHTML(msg1):
    # Définition du bouton Nouvelle partie.
    msg2 = "<button onclick=init()>Nouvelle partie</button>"

    # Modification du fichier HTML.
    racine = document.querySelector("#cb-body")
    racine.innerHTML = (css + divId("jeu", table(list(map\
    (rangee, [0, 1, 2, 3])))) + "<br>" + msg1 + "<br>" + "<br>" + msg2)


###############################################################################

# La procédure move prend en paramètre l'index correspondant au numéro d'une
# case, et déplace la carte se trouvant à cette position à l'endroit approprié.
# Elle modifie également le code HTML de la page Web afin d'afficher les
# messages appropriés quand l'utilisateur gagne, perd ou il ne peut plus
# brasser les cartes en faisant appel aux procédures testerProgression et
# bonsMessages.
def move(i):
    # On fait appel aux variables globales qui seront utilisées par move.
    global enVert
    global compteurBrasser
    global jeuHTML
    global jeu

    # On commence par enlever la couleur et l'attribut onclick de tous le jeu.
    decolorier(enVert)

    # Ensuite on trouve l'indice j de la case à laquelle on doit envoyer
    # la carte qui a été choisie.
    carte = jeu[i]  # Numéro de 0 à 51 correspondant à la carte à échanger.
    if carte // 4 == 1:  # Cas lorsqu'on clique sur un 2.
        indexCol1 = []
        for j in range(0, 40, 13):
            # On ajoute les indices des cases vides dans la colonne 1.
            # On ajoute également l'indice de la case qui contient la carte
            # d'intéret, si elle se trouve sur la première colonne.
            if jeu[j] // 4 == 0 or jeu[j] == carte:
                indexCol1.append(j)

        # Si le 2 n'est pas déjà dans la colonne 1, on trouve l'index de la
        # première case vide dans la colonne 1.
        if i not in list(range(0, 40, 13)):
            j = indexCol1[0]
        # Si le 2 est déjà dans la colonne 1, on trouve l'index de la première
        # case vide où il peut se déplacer.
        else:
            k = trouverIndex(indexCol1, i)
            j = indexCol1[(k + 1) % len(indexCol1)]

    # On trouve l'index où il faut déplacer la carte si ce n'est pas un 2.
    else:
        j = trouverIndex(jeu, carte - 4) + 1

    # On doit échanger la carte à la position i avec celle à la position j. On
    # modifie le code HTML du site Web afin que les cartes s'affichent au bon
    # endroit.
    carteVide = jeu[j]

    nouv = document.querySelector("#case" + str(j))
    nouv.innerHTML = convertirCarteHTML(carte)

    old = document.querySelector("#case" + str(i))
    old.innerHTML = '<img src="cards/absent.svg">'

    # On échange les cartes dans le tableau correspondant au jeu.
    jeu[j] = carte
    jeu[i] = carteVide

    # On retrouve les cartes à mettre en vert et on redéfinit la variable
    # jeuHTML avec la position des cartes à jour.
    enVert = elemVert(jeu)
    jeuHTML = convertirHTML(jeu)

    # On teste si le joueur a gagné et on affiche le bon message pour le bouton
    # Brasser les cartes.
    testerProgression()
    bonsMessages()

    # On colorie les cartes qui peuvent être déplacées.
    colorier(enVert)


###############################################################################

# La procédure testerProgression vérifie si le joueur a gagné ou non. Elle ne 
# prend pas de paramètres. On initialise une variable booléenne qui est associé 
# à la condition pour gagner le jeu. Quand il n'y a plus de cartes que l'on 
# peut bouger (len(enVert)=0), on test la condition en brassant les cartes qui 
# ne sont pas en ordre. S'il y a seulement 4 cartes à brasser et que ces cartes
# correspondent aux 4 as, cela veut dire que les cartes sont bien ordonnées
# et que le joueur a gagné. Les 4 as sont toujours à la fin de chaque
# rangée quand le jeu est bien ordonné, ce qui implique qu'ils doivent être
# brassés selon notre définition de la procédure shuffleRangee.
def testerProgression():
    # Appel aux variables globales.
    global gagnerCondition
    global enVert 

    gagnerCondition = False
    if len(enVert) == 0:
        cartesABrasserPourGagner=[]
        for i in range(1, 5):  # On itère sur chaque colonne.
            shuffleRangee(jeu, i, cartesABrasserPourGagner)

        if len(cartesABrasserPourGagner) == 4:
            for _ in cartesABrasserPourGagner:
                # Les valeurs 12,25,38,51 correspondent à la position des as
                # quand l'utilisateur a gagné, soit chaque fin de ligne.
                if _ in [12, 25, 38, 51]:
                    gagnerCondition = True

                else:
                    gagnerCondition = False
                    break


###############################################################################

# La procédure bonsMessages affiche les messages secondaires à l'endroit du 
# bouton Brasser les cartes. Elle ne prend pas de paramètre. On affiche le 
# message approprié quand l'utilisateur a perdu, soit quand la condition pour 
# gagner n'est pas remplie, le joueur ne peut plus déplacer de cartes et il ne 
# peut plus brasser les cartes.
def bonsMessages():
    # Appel aux variables globales.
    global enVert
    global compteurBrasser
    global gagnerCondition

    if len(enVert) == 0 and compteurBrasser == 0 and gagnerCondition == \
    False:
        msg1 = "Vous n'avez pas réussi à placer toutes les cartes... \
        Essayez à nouveau!"

        modifierHTML(msg1)

    # On affiche le message approprié quand l'utilisateur n'a pas gagné, qu'il
    # ne peut plus déplacer de cartes mais qu'il peut encore brasser les
    # cartes.
    elif len(enVert) == 0 and compteurBrasser != 0 and gagnerCondition == \
    False:
        msg1 = "Vous devez <button onclick=shuffle()>Brasser les cartes\
        </button>"

        modifierHTML(msg1)

    # On affiche le message approprié quand l'utilisateur a gagné.
    elif gagnerCondition == True:
        msg1 = "Vous avez gagné! Bravo!"

        modifierHTML(msg1)


###############################################################################

# Cette fonction permet de mélanger le jeu de carte de façon aléatoire. La
# fonction prend un tableau (que l'on va indexer avec les indices des éléments
# à échanger), une valeur initiale d'itération pour la boucle for et le tableau
# des cartes. Si le tableauIndice correspond à la valeur None, on veut mélanger 
# un paquet de carte complet, ce qui correspond à ce qui se produit quand on 
# crée une nouvelle partie. Elle retourne un jeu de carte aléatoire. On mélange 
# le jeu de carte en utilisant la logique suivante:On choisit un élément au 
# hasard, et on l'échange avec le dernier élément.On recommence avec l'avant 
# dernier (sauf qu'on ne touche pas au dernier élément). On recommence avec 
# l'avant avant dernier (sans toucher aux 2 derniers), et ainsi de suite.
def jeuAleatoire(tableauIndice, valeurInitialeRange, jeuCartes):
    if tableauIndice != None:
        for i in range(valeurInitialeRange, -1, -1):
            indice = math.floor(random.random() * i)
            # Cas si on échange l'élément avec lui même.
            if indice == i:
                continue
            # Sélectionner un élément au hasard et le retirer.
            elemAleatoire = jeuCartes.pop(tableauIndice[indice])
            # Retirer le 'dernier' élément.
            elemFin = jeuCartes.pop(tableauIndice[i] - 1)
            # Mettre le dernier élément à l'indice aléatoire.
            jeuCartes.insert(tableauIndice[indice], elemFin)
            # Mettre l'élement aléatoire à la fin.
            jeuCartes.insert(tableauIndice[i], elemAleatoire)

        return jeuCartes

    else:
        # On initialise la variable jeuMelange à un jeu de cartes en ordre.
        jeuMelange = list(range(52))
        for i in range(valeurInitialeRange, -1, -1):
            indice = math.floor(random.random() * i)
            if indice == i:
                continue
            elemAleatoire = jeuMelange.pop(indice)
            elemFin = jeuMelange.pop(i - 1)
            jeuMelange.insert(indice, elemFin)
            jeuMelange.insert(i, elemAleatoire)

        return jeuMelange


###############################################################################

# Procédure qui prend le jeu de carte et le numéro de la rangée et un tableau
# vide qui va contenir les index des cartes à brasser. Elle ajoute au tableau
# les index des cartes que l'on doit brasser sur la rangée correspondante.
def shuffleRangee(jeu, numRangee, cartesABrasserRangee):

    # On itère sur toutes les cartes dans la rangée correspondante.
    for i in range(13 * (numRangee - 1), numRangee * 13):

        # Si la première carte de la rangée n'est pas un 2, on ajoute toutes 
        # les cartes de la rangée au tableau des cartes à brasser.
        if i % 13 == 0 and jeu[i] // 4 != 1:
            for _ in range(i, numRangee * 13):
                cartesABrasserRangee.append(_)
            break

        # Si l'index de la carte n'est pas celui de la première carte de la 
        # rangée, et que la carte précédente n'est pas de la même couleur ou 
        # qu'elle n'a pas une valeur correspondant à la valeur de (la carte à 
        # l'index i) -1, on ajoute toutes les cartes de la rangée à partir de 
        # l'index i au tableau des cartes à brasser.
        elif (i % 13 != 0) and (jeu[i] % 4 != jeu[i - 1] % 4 or \
        jeu[i] // 4 != (jeu[i - 1] // 4) + 1):
            for _ in range(i, numRangee * 13):
                cartesABrasserRangee.append(_)
            break
        # Si les conditions précédentes ne sont pas remplies, la carte ne doit 
        # pas être brassée et on passe à la carte suivante.
        else:
            continue


###############################################################################

# Procédure qui ne prend pas de paramètre et qui brasse les cartes qui ne sont
# pas bien placées dans la grille. Cette procédure met à jour l'affichage des
# cartes une fois qu'elles sont brassées.
def shuffle():
    # On fait appel aux variables globales qui seront utilisées par shuffle.
    global jeu
    global enVert
    global jeuHTML
    global compteurBrasser

    # On identifie les index des cartes à brasser et on les ajoute au tableau
    # cartesABrasser
    cartesABrasser=[]
    for i in range(1, 5):
        shuffleRangee(jeu, i,cartesABrasser)

    # On modifie la variable jeu afin d'avoir un jeu de carte brassé.
    jeu = jeuAleatoire(cartesABrasser, len(cartesABrasser) - 1, jeu)

    # Après le brassage, on colorie en vert les cartes que l'on peut déplacer
    # et on met à jour le jeu de carte brassé (dans sa version HTML).
    enVert = elemVert(jeu)

    jeuHTML = convertirHTML(jeu)

    # On met à jour la valeur du compteur pour brasser les cartes, ce compteur
    # commence à 3.
    compteurBrasser -= 1

    # On modifie le message1 selon le nombre de fois que l'on peut brasser les
    # cartes une fois le brassage terminé.
    if compteurBrasser > 0:
        msg1 = ("Vous pouvez encore <button onclick=shuffle()>Brasser les \
        cartes</button> " + str(compteurBrasser) + " fois")
    else:
        msg1 = "Vous ne pouvez plus brasser les cartes"

    # On met à jour l'affichage des cartes sur le site Web avec la couleur lime
    # pour les cartes qui peuvent être déplacées.
    modifierHTML(msg1)
    colorier(enVert)


###############################################################################

# La fonction elemVert prend en paramètre un tableau qui correspond à un jeu de
# carte et renvoies un tableau des index des éléments qui vont être affiché en 
# vert, et donc qui peuvent être déplacés.
def elemVert(jeu):
    # On initialise un tableau qui va contenir les index des cartes à colorier 
    # en vert.
    aColorer = []

    # Pour chaque case vide dans le jeu.
    for x in range(4):
        i = trouverIndex(jeu, x)

        # Si l'indice d'avant est sur une autre rangée.
        if i // 13 != (i - 1) // 13:
            continue 

        gaucheVide = jeu[i - 1]     # Numéro de la carte à gauche.

        # Si c'est un trou à la gauche.
        if gaucheVide // 4 == 0:
            continue                
        
        # Numéro de la carte qui peut aller dans le vide.
        carteVerte = gaucheVide + 4 
        aColorer.append(trouverIndex(jeu, carteVerte) if carteVerte < 52 \
        else None)

    # Ajouter les 2 si une rangée commence par un espace vide.
    for i in range(0, 40, 13):
        if jeu[i] // 4 == 0:
            for j in range(4, 8):
                aColorer.append(trouverIndex(jeu, j))
            break

    aColorer = list(filter(lambda x: x != None, aColorer))

    return aColorer


###############################################################################

# La fonction colorier prend en paramètre un tableau, et colorie les éléments 
# aux index correspodants aux éléments du tableau. La fonction ajoute aussi le 
# traitement d'événement 'onclick' avec la fonction move, ce qui permet de 
# faire le bon traitement lorsque l'on clic sur une carte verte.
def colorier(tableau):
    for i in tableau:
        case = document.querySelector("#case" + str(i))
        case.setAttribute("style", "background-color: lime")
        case.setAttribute("onclick", "move(" + str(i) + ")")


###############################################################################

# La fonction decolorier prend en paramètre un tableau, et enlève la couleur 
# des cartes aux index correspodants aux éléments du tableau. La fonction 
# enlève aussi le traitement d'événement, ce qui permet d'empêcher les cartes
# qui ne peuvent plus bouger de se déplacer.
def decolorier(tableau):
    for i in tableau:
        case = document.querySelector("#case" + str(i))
        case.removeAttribute("style")
        case.removeAttribute("onclick")


###############################################################################

# La fonction convertirHTML convertit le tableau de nombres en texte html, ce 
# qui permet d'aller chercher l'URL de chaque image. Ici, on attribue à 
# 0,1,2,3 la valeur As, à 4,5,6,7 la valeur 2, et ainsi de suite. La fonction
# prend le jeu de cartes et retourne sa version en html.
def convertirHTML(jeuCarte):
    jeuCarteComplet = []
    for x in jeuCarte:
        jeuCarteComplet.append(convertirCarteHTML(x))
    return jeuCarteComplet


###############################################################################

# La fonction convertirCarteHTML prend le numéro correspondant à une carte en 
# paramètre et retourne le texte HTML correspondant à l'image de cette carte. 
# L'image des as correspond à une case vide.
def convertirCarteHTML(x):
    valeur = valeurTab[x // 4]
    couleur = couleurTab[x % 4]
    if valeur == "absent":
        return '<img src="cards/absent.svg">'
    else:
        return '<img src="cards/' + valeur + couleur + '.svg">'


###############################################################################

# Les 5 fonctions suivantes permettent de mettre un texte entre des bornes 
# afin d'être interprété par un fichier HTML. Elle prennent un tableau ou autre
# contenu en paramètre, et retourne un texte HTML qui lui correspond.
def table(tab):
    return '<table>' + tabEnTexte(tab) + '</table>'


def tr(contenu):
    return '<tr>' + contenu + '</tr>'


def td(i, contenu):
    return '<td id="case' + str(i) + '">' + contenu + '</td>'


def divId(id, contenu):
    return '<div id="' + id + '">' + contenu + '</div>'


def tabEnTexte(tab):
    return ''.join(tab)


###############################################################################

# La fonction rangee prend en paramètre un nombre entre 0 et 3, et renvoie un 
# texte entre les bornes <> correspondant au contenu de la rangée du tableau de 
# carte ayant comme indice le numéro entré en paramètre.
def rangee(num):
    debutRangee = num * 13
    texte = ""
    # On insère les images des cartes au bon endroit dans le tableau HTML.
    for i in range(debutRangee, debutRangee + 13):
        texte += td(i, jeuHTML[i])
    return tr(texte)


###############################################################################

# Procédure de tests unitaires pour les différentes fonctions utilisées dans le
# programme.
def tests():
    assert len(jeuAleatoire(None, 51, None)) == 52
    assert len(jeuAleatoire([1,2,3],2,[1,2,3,4])) == 4
    assert trouverIndex([0, 1, 2, 3], 2) == 2
    assert trouverIndex([], 2) == -1
    assert trouverIndex([2, 3, 4], 5) == -1
    assert trouverIndex([7, "pomme", True], "pomme") == 1
    assert tr('allo') == "<tr>allo</tr>"
    assert tr('') == "<tr></tr>"
    assert td(2, 'allo') == '<td id="case2">allo</td>'
    assert td(0,'') == '<td id="case0"></td>'
    assert divId('oui','non') == '<div id="oui">non</div>'
    assert divId('','') == '<div id=""></div>'
    assert tabEnTexte(['je','suis','gentil']) == 'jesuisgentil'
    assert tabEnTexte(['je','','gentil']) == 'jegentil'
    assert table(['je','suis','gentil']) == '<table>jesuisgentil</table>'
    assert table(['je','','gentil']) == '<table>jegentil</table>'
    assert convertirCarteHTML(21) == '<img src="cards/6D.svg">'
    assert convertirCarteHTML(38) == '<img src="cards/10S.svg">'
    assert convertirCarteHTML(0) == '<img src="cards/absent.svg">'
    assert convertirHTML([21,38,0]) == ['<img src="cards/6D.svg">',\
    '<img src="cards/10S.svg">', '<img src="cards/absent.svg">']
    assert convertirHTML([]) == []
    assert elemVert([51, 35, 40, 23, 41, 20, 28, 37, 19, 8, 47, 24, 34, 27, 9,\
    21, 39, 44, 33, 2, 7, 38, 32, 46, 18, 16, 45, 31, 50, 26, 48, 10, 15, 1,\
    13, 43, 22, 6, 14, 49, 5, 30, 4, 36, 11, 0, 12, 42, 17, 29, 25, 3]) == \
    [32, 8, 7, 49]
    assert elemVert([0, 35, 40, 23, 41, 20, 28, 37, 19, 8, 47, 24, 34, 27, 9,\
    21, 39, 44, 33, 2, 7, 38, 32, 46, 18, 16, 45, 31, 50, 26, 48, 10, 15, 1,\
    13, 43, 22, 6, 14, 49, 5, 30, 4, 36, 11, 51, 12, 42, 17, 29, 25, 3]) == \
    [8, 7, 49, 42, 40, 37, 20]
    assert elemVert([51, 0, 40, 23, 41, 20, 28, 37, 19, 8, 47, 24, 34, 27, 9,\
    21, 39, 44, 33, 5, 7, 38, 32, 46, 18, 16, 45, 31, 50, 1, 48, 3, 15, 26,\
    13, 43, 22, 6, 14, 49, 2, 30, 4, 36, 11, 35, 12, 42, 17, 29, 25, 10]) == []
    assert elemVert([0, 1, 2, 23, 41, 20, 28, 37, 19, 8, 47, 24, 34, 3, 9,\
    21, 39, 44, 33, 40, 7, 38, 32, 46, 18, 16, 45, 31, 50, 26, 48, 10, 15, 35,\
    13, 43, 22, 6, 14, 49, 5, 30, 4, 36, 11, 51, 12, 42, 17, 29, 25, 27]) == \
    [42,40,37,20]


###############################################################################

# La procédure init initialise la page Web quand on charge le site Web ou quand
# on clique sur le bouton Nouvelle partie.
def init():
    # On définit les variables globales reliées au jeu de carte.
    global jeu
    global enVert
    global jeuHTML
    global compteurBrasser

    # On assigne un jeu de carte aléatoire à la variable jeu et on convertit le
    # jeu de carte en images. On initialise la variable enVert afin d'afficher
    # les cartes que l'on peut déplacer au début de la partie.
    jeu = jeuAleatoire(None, 51,None)
    jeuHTML = convertirHTML(jeu)
    enVert = elemVert(jeu)

    # On initialise le compteur de brassage à 3.
    compteurBrasser = 3

    # Message initial pour le bouton de brassage.
    msg1 = ("Vous pouvez encore <button onclick=shuffle()>Brasser les cartes\
    </button> " + str(compteurBrasser) + " fois")

    # On modifie le code HTML pour que la page Web affiche le jeu de carte 
    # aléatoire et les boutons de brassage et de nouvelle partie. On colorie 
    # les cartes que l'on peut déplacer en vert.
    modifierHTML(msg1)
    colorier(enVert)


###############################################################################

# On fait appel à la fonction init pour charger la page Web quand l'utilisateur
# se connecte au site Web.
init()

# On fait appel à la procédure de tests unitaires.
tests()