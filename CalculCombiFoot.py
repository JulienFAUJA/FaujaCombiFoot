import pickle
import glob
import itertools

"""
Script qui permet de demander plusieurs scores par Matches
et qui calcule toutes les combinaisons des tickets à remplir
"""

class Score:
    """
    Contient le score d'un Match et son nom
    """
    def __init__(self, match_name, score):
        self.match_name = match_name
        self.score = score

    def __str__(self):
        return self.match_name + ' : \n' + self.score


class Match:
    """
    Contient tous les scores du Match et son nom
    """
    def __init__(self, name):
        self.name = name
        self.scores = []

    def __add__(self, other):
        if type(other) == Score:
            self.scores.append(other)
        elif type(other) == str:
            score = Score(self.name, other)
            self.scores.append(score)

    def __str__(self):
        scores_list = [s.score for s in self.scores]
        return self.name+' : \n'+' / '.join(scores_list)


class Combinaison:
    """
    C'est en fait la classe Ticket à remplir
    """
    def __init__(self, num_combi, result):
        self.numero_ticket = num_combi
        self.affichage = result

    def __str__(self):
        ticket = "Ticket N°"+str(self.numero_ticket)+'\n'
        return ticket+self.affichage



def cartesian_product_of_matches(*args):
    """
    Retourne la combinaison de tous les matches
    :param args: Liste de listes avec le symbole
    * avant l'argument
    :return: Les combinaisons de toutes les
    possibilités entre les listes
    """

    res_list = []
    for element in itertools.product(*args):
        res_list.append(element)
    return res_list


def SetMatch(match_index):
    """
    Parametre un nouveau Match
    :param match_index: L'index du Match
    :return: Le Match, mais pas utilise
    """
    with open('Match0'+str(match_index)+'.match', 'wb') as f:
        is_match_id_setted = False
        while is_match_id_setted == False:
            print("Entrez le texte pour indentifier le Match : \n")
            print("Ex : \"OM-PSG (Score Mi-Temps)\"\n ")
            match_identifier = input()
            choice = MatchIdentifierValidation(match_identifier)
            if choice == "1":
                match_identifier = input()
            if choice == "2":
                is_match_id_setted = True
                m = Match(match_identifier)
        add_score = True
        # Sortie du While
        while add_score:
            print("[ 1 ] Ajouter un Score / Côte ")
            print("[ 2 ] Retour au Menu principal ")
            action_choice = input()
            if action_choice == "1":
                m+EntrerScore()
            elif action_choice == "2":
                data = pickle.Pickler(f)
                data.dump(m)
                add_score = False
        return m


def EntrerScore():
    """
    Fonction qui demande d'entrer le score du match
    et qui le renvoie
    :return: le score du match (Str)
    """
    score_valider = "1"
    while score_valider == str(1):
        print("Entrez le Score séparé par un tiret (-)\n")
        print("Ex : 2-1\n")
        score = input()
        print("Vous avez choisi : \n " + str(score))
        print("[ 1 ] Recommencer \n[ 2 ] Valider ")
        score_valider = input()
    return score



def MatchIdentifierValidation(match_identifier):
    """
    Demande confirmation du nom du Match
    :param match_identifier: Nom du Match
    :return: Le choix
    """
    print("Vous avez choisi : \n")
    print(str(match_identifier) + "\n")
    print("[ 1 ] Choisir un autre\n[ 2 ] Valider\n ")
    choice = input()
    return choice


def Recup_Tous_Les_Matches():
    """
    Recupere tous les Matches depuis les
    fichiers binaires
    :return: Les Matches (type Match)
    """
    les_matches = []
    for fichier in glob.glob('Match0*'):
        with open(fichier, 'rb') as fichier:
            data = pickle.Unpickler(fichier)
            match = data.load()
            les_matches.append(match)
    return les_matches


# Commencer par un menu qui demande quoi faire
def MainMenu():
    """
    Fonction du Menu principal qui boucle tant que ça
    n'est pas finir et qu'il y a des Matches à ajouter
    :return: None
    """
    print("Que voulez-vous faire :\n")
    print("[ 1 ] Paramétrer un Match \n")
    print("[ 2 ] Calculer toutes les combinaisons \n")

    choix_menu = input()
    if choix_menu == str(1):
        # Si choix == parametrer un Match:
        # Demander l'index du Match et ouvrir
        # la fonction SetMatch en lui envoyant l'index
        print("Quel est le numéro du match : \n ")
        print("[ 1 ] C'est le premier \n ")
        print("[ 2 ] C'est le deuxième \n ")
        print("[ 3 ] Le Troisième : ATTENTION !!!")
        print("Ca fait beaucoup de tickets à remplir \n")
        match_index = input()
        if 0 < int(match_index) < 5:
            SetMatch(match_index)
            # Afficher le Menu en cas de retour et jusqu'à
            # ce que l'utilisateur demande de sortir
            MainMenu()
    elif choix_menu == str(2):
        liste_de_matches = Recup_Tous_Les_Matches()
        [print(x) for x in liste_de_matches]
        produit_cart = cartesian_product_of_matches(*[x.scores for x in liste_de_matches])

        for i, combi in enumerate(produit_cart):
            print(20 * '*')
            ticket = Combinaison(i + 1, "")
            for n, score in enumerate(combi):
                end = '\n'
                if n == 1:
                    end = ''
                ticket.affichage += str(score) + end
            print(ticket)


MainMenu()
