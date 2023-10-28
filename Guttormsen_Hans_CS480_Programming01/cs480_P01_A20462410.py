import sys

pruning = False #bool to determine if we should prune the tree
human = True
i = 0

class TicTacToe :
    def __init__(self, board = [[2, 2, 2], [2, 2, 2], [2, 2, 2]], turn = 0, prune = 0) :
        self.board = board #board is a list of 3 lists of ints 0, 1, or 2. 0 is O, 1 is X, 
        self.turn = turn #0 = O and 1 = X
        self.prune = prune

    def __str__(self) : #create a str function for the board
        string = ""
        for j in range(3) :  #loop through the three lists that make the board
            row = self.board[j]  #grab the list
            line = ""            #reset the line (three lines per board)
            for i in range(3) :  #loop through the three symbols in row
                if i == 2 :      #if last symbol we dont need | to print
                    if j == 2 :  #and if last row we don't want \n (made it look weird)
                        line = line + " " + self.symbol(row[i])
                    else :
                        line = line + " " + self.symbol(row[i]) + " \n"
                else :
                    line = line + " " + self.symbol(row[i]) + " |"
            string = string + line #build the string line by line
            if not i == j :        #when the last row we don't need ---+---+---
                string = string + "---+---+---\n"
        return string 
    
    def moves(self) : #generate a list of allowed moves
        i = 0
        moves = []
        for row in self.board : #loop through rows
            for spot in row :   #loop through symbols
                i = i + 1
                if spot == 2 :  #if spot empty (2 is not O or X)
                    moves.append(i)  #its an available move
        return moves

    def terminal(self) :
        #need to check rows
        for row in self.board : 
            #if we check if spot 1 = 2 and 2 = 3 and make sure none of them are 2, we can determine row win
            if row[0] == row[1] and row[1] == row[2] and row[0] != 2 :
                #return the 0 or 1 for who won. makes it easier to determine the winner
                return row[0]
            
        #need to check cols
        for i in range(3) :
            #same logic as rows, but for columns
            if self.board[0][i] == self.board[1][i] and self.board[1][i] == self.board[2][i] and self.board[0][i] != 2 :
                #return winner
                return self.board[0][i]
                
        
        #need to check both diagnols
        #this is the top left to bottom right diagnol win
        if self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2] and self.board[0][0] != 2 :
            #return winner
            return self.board[0][0]
        
        #this is the top right to bottom left diagnol win
        if self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0] and self.board[0][2] != 2 :
            #return winner
            return self.board[0][2]
        
        if len(self.moves()) == 0 :
            return -1

        return 2 #this means no one has one and not a tie. ie not terminal

    def maxvalue(self) : #max value of node

        global i #i keeps track of trees. need it here to count root as well
        i = i + 1
        finalmove = 0 #this is just setting a default move
        v = -100      #v = -inf #v -100 is essentially -inf in this case

        #if terminal return utility, null pair
        if self.terminal() == 0 : #O wins is minimum
            return [-1, 0]
        elif self.terminal() == 1 : #X wins is max
            return [1, 0]
        elif self.terminal() == -1 : #ties is neutral
            return [0, 0]
        elif self.terminal() == 2:  #no winner or tie
            for move in self.moves() : #for each a in actions
                
                self.move(move) #simulate the move 

                utilitymove = self.minvalue()  #find utility of simulated move
                v2 = utilitymove[0] # get utility

                self.unmove(move) #un-simulate move

                if v2 > v : #if new utility is better than old utility, we have new move

                    finalmove = move #update move and utility
                    v = v2

        return [v, finalmove] #return utility move pair 

    def minvalue(self) : #min value of node

        global i #keep track of trees
        i = i + 1
        finalmove = 0
        v = 100 #basically inf
        
        #if terminal return utility, null pair
        if self.terminal() == 0 : #if 0 win, minimum value
            return [-1, 0]
        elif self.terminal() == 1 : #if X win, maximum value
            return [1, 0]
        elif self.terminal() == -1 : #if tie, neutral value
            return [0, 0]
        elif self.terminal() == 2 : #no win or tie, minmax moves
            for move in self.moves() : #for each a in actions

                self.move(move) #simulate move

                utilitymove = self.maxvalue() #get utility at simulated move
                v2 = utilitymove[0] 
                
                self.unmove(move) #un-simulate move

                if v2 < v : #if new utility is better than old utility

                    v = v2 #update utility and move
                    finalmove = move

        return [v, finalmove] #return utility move pair

    def minmax(self) : #performs minmax and returns utility move pair
        if self.turn : #if X, we want max value of next move
            move = self.maxvalue() 
        else : #if O, we want min value of next move
            move = self.minvalue()
        return move
    
    def maxvalueab(self, alpha, beta) : #returns max utility move pair with pruning
        global i
        i = i + 1
        finalmove = 0 
        v = -100 #v <- -inf    #essentially inf in a case of -1 < v > 1
        
        if self.terminal() == 0 : #if game is terminal then return utility move pair
            return [-1, 0]
        elif self.terminal() == 1 :
            return [1, 0]
        elif self.terminal() == -1 :
            return [0, 0]
        elif self.terminal() == 2 :
            for move in self.moves() : #for a in game actions

                #minvalue(game, game.result(state, a), alpha, beta)
                self.move(move)        #simulate the move
                utilitymove = self.minvalueab(alpha, beta) #get the utilitymove at the next node
                self.unmove(move) #undo the move (otherwise it just keeps it from tree to tree)
                
                v2 = utilitymove[0] #set new utility

                if v2 > v : #if new utility better

                    v = v2 #update utility move and alpha
                    finalmove = move
                    alpha = max(alpha, v)

                if v >= beta : #if we know that utility is more than upper bound,
                               #we know it wont get chosen by min. just skip this tree
                    return [v, finalmove]
                
            return [v, finalmove] #return utility move pair 

    def minvalueab (self, alpha, beta) : #returns min utility move pair with pruning
        global i
        i = i + 1
        finalmove = 0 
        v = 100 #v <- inf    #essentially inf in a case of -1 < v > 1
        
        if self.terminal() == 0 : #if game is terminal then return utility move pair
            return [-1, 0]
        elif self.terminal() == 1 :
            return [1, 0]
        elif self.terminal() == -1 :
            return [0, 0]
        elif self.terminal() == 2 :
            for move in self.moves() : #for a in game actions

                #minvalue(game, game.result(state, a), alpha, beta)
                self.move(move)        #simulate the move
                
                utilitymove = self.maxvalueab(alpha, beta) #get the utilitymove at the next node
                self.unmove(move) #undo the move (otherwise it just keeps it from tree to tree)
                
                v2 = utilitymove[0]

                if v2 < v : #if new utility better than old utility
                    v = v2
                    finalmove = move
                    beta = min(beta, v)

                if v <= alpha : #if we know that utility is less than lower bound, 
                                #we know it wont get chosen by max. just skip this tree
                    return [v, finalmove]
            return [v, finalmove]

    def minmaxab(self) : #performs minmax with pruning and returns utility move pair
        global i
        i = i + 1 #the root node
        move = 0
        if self.turn : #if X, we want max value of next move
            move = self.maxvalueab(-100, 100) 
        else : #if O, we want min value of next move
            move = self.minvalueab(-100, 100)
        return move

    def getbestmove(self) :
        #we need to check for Pruning here
        global pruning
        if pruning :
            return self.minmaxab()
        else :
            return self.minmax()

    def move(self, action) : #commits the move. changes the board at the move location
        #action = self.minmax(self.board, self.turn)

        action = action - 1 #list is technically 0-8 but for humans we did 1-9 so make them match

        row = action // 3 #this gets which list to be in. 1-3 = 1, 4-6 = 2, 7-9 = 3
        column = action % 3 #this gets the index in the list

        self.board[row][column] = self.turn #set the board spot to the turn  (0 or 1)

        
        self.turn = int(not(self.turn)) # this makes 1 -> 0 and 0 -> 1

    def unmove(self, action) : #undo any move on board 

        action = action - 1 #move is 1-9 but board in python is really 0-8

        row = action // 3 #get row
        column = action % 3 #get column

        self.board[row][column] = 2 #reset to neither X or O

        self.turn = int(not(self.turn)) #change turn

    def symbol(self, i) : #returns an O or X that matches the 0 or 1 for turn
        if i == 0 : return "O" 
        elif i == 1: return "X"
        else : return " " #otherwise i == 2 (or any unexpected values) should return an empty space

    

def startgame(turn) : #this is where the game actually runs and decisions are made
    global pruning #get the global variables (makes it easier)
    global human
    global i

    board = TicTacToe([[2, 2, 2], [2, 2, 2], [2, 2, 2]], turn, int(pruning)) #initialize our board
    if human : print(board)

    if human : # if we have a human player we need to let them play
        #we need to take turns until the game is over
        while board.terminal() == 2 :
            if board.turn == turn : #assume human goes first

                move = -1           #default to out of range move
                moves = board.moves() #get valid moves

                while (move not in moves) and move != 0 : #loop until valid move

                    #prompt user for move
                    print("What is your move? (Possible moves at the moment are: " + str(board.moves()) + " | enter 0 to exit the game)")
                    move = int(input())

                if move == 0 :#user exits

                    sys.exit("Player ended game.")
                
                else : #valid move, play it

                    board.move(move)
                    print()

            else : 

                #this definitely shouldve been a function in tictactoe class, but too late now
                bestmove = board.getbestmove()[1] #find best move 
                currturn = board.turn #remember turn
                board.move(bestmove) #make the best move

                print(board) #display board and print what computer did
                print(board.symbol(currturn) + "'s selected move: " + str(bestmove) + ". Number of search tree nodes generated: " + str(i))
                print()

                i = 0 #reset tree count

        if board.terminal() == -1 : #if tie, tell them

            print("TIE")

        else : #only remaining values are for winners

            print(board.symbol(board.terminal()) + " WINS!") #print out who won

    else : #if not a human player, just let them move over and over

        while board.terminal() == 2 : #loop until winner

            bestmove = board.getbestmove()[1] #find best move
            currturn = board.turn             #remember turn
            board.move(bestmove)              #make the best move

            print(board) #display board and print what computer did
            print(board.symbol(currturn) + "'s selected move: " + str(bestmove) + ". Number of search tree nodes generated: " + str(i))
            print()

            i = 0 #reset tree count

        if board.terminal() == -1 : #if tie tell them

            print(board)
            print("TIE")

        else : #if winner print who won

            print(board.symbol(board.terminal()) + " WINS!")


        

    #print(board)


def main() : #do pre-game requirements

    global pruning #get global variables
    global human

    #print assignment info
    print("Guttormsen, Hans, A20462410 solution:\nAlgorithm: MiniMax with alpha-beta pruning")

    #get number of command line args
    argnums = len(sys.argv)

    #logic for reading command line from script in discussions but changed var names and added logic (CS480 Jacek Dzikowski)
    #check to make sure we got all input and that arguments entered are valid answers
    if not argnums == 4 or (not (int(sys.argv[1]) == 2 or int(sys.argv[1]) == 1)) or (not (sys.argv[2] == 'X' or sys.argv[2] == 'O')) or (not (int(sys.argv[3]) == 2 or int(sys.argv[3]) == 1)) :
        sys.exit("ERROR: Not enough/too many/illegal input arguments.") 

    if int(sys.argv[1]) == 2 :
        pruning = True

    if int(sys.argv[3]) == 2 :
        human = False
        print("Mode: computer versus computer")
    else :
        print("Mode: human versus computer")

    print("First: " + sys.argv[2])

    if sys.argv[2] == 'O' : #determine who to start with
        startgame(0)
    else :
        startgame(1)

main() #I'm just doing this bc without it I usually end up with no functions and gross messy code without it


