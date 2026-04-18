import random

scorePieces = {'K':0, 'Q':10, 'R':5, 'B':3, 'N':3, 'p':1}

scoreCavalier = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

scoreFou = [[4, 3, 2, 1, 1, 2, 3, 4],
            [3, 4, 3, 2, 2, 3, 4, 3],
            [2, 3, 4, 3, 3, 4, 3, 2],
            [1, 2, 3, 4, 4, 3, 2, 1],
            [1, 2, 3, 4, 4, 3, 2, 1],
            [2, 3, 4, 3, 3, 4, 3, 2],
            [3, 4, 3, 2, 2, 3, 4, 3],
            [4, 3, 2, 1, 1, 2, 3, 4]]

scoreReine =  [[1, 1, 1, 3, 1, 1, 1, 1],
                [1, 2, 3, 3, 3, 1, 1, 1],
                [1, 4, 3, 3, 3, 4, 2, 1],
                [1, 2, 3, 3, 3, 2, 2, 1],
                [1, 2, 3, 3, 3, 2, 2, 1],
                [1, 4, 3, 3, 3, 4, 2, 1],
                [1, 1, 2, 3, 3, 1, 1, 1],
                [1, 1, 1, 3, 1, 1, 1, 1]]

scoreTour =  [ [4, 3, 4, 4, 4, 4, 3, 4],
                [4, 4, 4, 4, 4, 4, 4, 4],
                [1, 1, 2, 3, 3, 2, 1, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 1, 2, 2, 2, 2, 1, 1],
                [4, 4, 4, 4, 4, 4, 4, 4],
                [4, 3, 4, 4, 4, 4, 3, 4]]

scorePionsBlancs =  [[8, 8, 8, 8, 8, 8, 8, 8],
                    [8, 8, 8, 8, 8, 8, 8, 8],
                    [5, 6, 6, 7, 7, 6, 6, 5],
                    [2, 3, 3, 5, 5, 3, 3, 2],
                    [1, 2, 3, 4, 4, 3, 2, 1],
                    [1, 1, 2, 3, 3, 2, 1, 1],
                    [1, 1, 1, 0, 0, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0]]

scorePionsNoirs =  [[0, 0, 0, 0, 0, 0, 0, 0],
                    [1, 1, 1, 0, 0, 1, 1, 1],
                    [1, 1, 2, 3, 3, 2, 1, 1],
                    [1, 2, 3, 4, 4, 3, 2, 1],
                    [2, 3, 3, 5, 5, 3, 3, 2],
                    [5, 6, 6, 7, 7, 6, 6, 5],
                    [8, 8, 8, 8, 8, 8, 8, 8],
                    [8, 8, 8, 8, 8, 8, 8, 8]]

scoresPositionPieces = {'N': scoreCavalier, 'Q': scoreReine, 'B': scoreFou, 'R': scoreTour,
                        'wp': scorePionsBlancs, 'bp': scorePionsNoirs}

ECHEC_ET_MAT = 1000
PAT = 0
PROFONDEUR = 3

class IA():

    def trouverCoupAleatoire(coupsValides):
        return coupsValides[random.randint(0, len(coupsValides) - 1)]
    
    """ Méthode pour lancer la recherche du meilleur coup """
    def trouverMeilleurCoup(etatJeu, coupsValides):
        global prochainCoup, compteur
        prochainCoup = None
        compteur = 0
        trouverNegaMaxAlphaBeta(etatJeu, coupsValides, PROFONDEUR, -ECHEC_ET_MAT, ECHEC_ET_MAT, 1 if etatJeu.whiteToMove else -1)
        print(compteur)
        return prochainCoup

def trouverNegaMaxAlphaBeta(etatJeu, coupsValides, profondeur, alpha, beta, couleurTour):
    global prochainCoup, compteur
    compteur += 1
    if profondeur == 0:
        return couleurTour * evaluerPlateau(etatJeu)
    
    scoreMax = -ECHEC_ET_MAT
    for coup in coupsValides:
        etatJeu.make_move(coup)
        prochainsCoups = etatJeu.get_valid_moves()
        score = -trouverNegaMaxAlphaBeta(etatJeu, prochainsCoups, profondeur - 1, -beta, -alpha, -couleurTour)
        
        if score > scoreMax:
            scoreMax = score
            if profondeur == PROFONDEUR:
                prochainCoup = coup
        
        etatJeu.undo_move()
        
        if scoreMax > alpha:
            alpha = scoreMax
        if alpha >= beta:
            break
    
    return scoreMax
        
""" 
Un score positif avantage les blancs 
Un score négatif avantage les noirs
"""
def evaluerPlateau(etatJeu):
    if etatJeu.checkmate:
        if etatJeu.whiteToMove:
            return -ECHEC_ET_MAT  # les noirs gagnent
        else: 
            return ECHEC_ET_MAT  # les blancs gagnent
    elif etatJeu.stalemate:
        return PAT
    
    score = 0
    for ligne in range(len(etatJeu.board)):
        for colonne in range(len(etatJeu.board[ligne])):
            case = etatJeu.board[ligne][colonne]
            scorePosition = 0
            
            if case != "--":
                if case[1] != 'K':  # pas de table pour le roi
                    if case[1] == 'p':
                        scorePosition = scoresPositionPieces[case][ligne][colonne]
                    else:
                        scorePosition = scoresPositionPieces[case[1]][ligne][colonne]

                if case[0] == 'w':
                    score += scorePieces[case[1]] + scorePosition * 0.1
                elif case[0] == 'b':
                    score -= scorePieces[case[1]] + scorePosition * 0.1
            
    return score