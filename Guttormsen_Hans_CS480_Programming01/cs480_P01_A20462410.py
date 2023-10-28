import sys

pruning = False #bool to determine if we should prune the tree
human = True
i = 0

class TicTacToe :
    def __init__(self, board = [[2, 2, 2], [2, 2, 2], [2, 2, 2]], turn = 0, prune = 0) :
        self.board = board #board is a list of 3 lists of ints 0, 1, or 2. 0 is O, 1 is X, 
        self.turn = turn #0 = O and 1 = X
        self.prune = prune

    def __str__(self) :
        string = ""
        for j in range(3) :
            row = self.board[j]
            line = ""
            for i in range(3) :
                if i == 2 :
                    line = line + " " + self.symbol(row[i]) + " \n"
                else :
                    line = line + " " + self.symbol(row[i]) + " |"
            string = string + line
            if not i == j :
                string = string + "---+---+---\n"
        return string
    
    def moves(self) :
        i = 0
        moves = []
        for row in self.board :
            for spot in row :
                i = i + 1
                if spot == 2 :
                    moves.append(i)
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

        return 2

    def maxvalue(self) :
        global i
        i = i + 1
        print(i)
        finalmove = 0
        v = -100
        #print("Terminal " + str(self.terminal()))
        if self.terminal() == 0 :
            #print(self)
            #print("Terminal " + str(self.terminal()))
            #print("Utility = -1\nMove = null")
            return [-1, 0]
        elif self.terminal() == 1 :
            #print(self)
            #print("Terminal " + str(self.terminal()))
            #print("Utility = 1\nMove = null")
            return [1, 0]
        elif self.terminal() == -1 :
            #print(self)
            #print("Terminal " + str(self.terminal()))
            #print("Utility = 0\nMove = null")
            return [0, 0]
        elif self.terminal() == 2:
            for move in self.moves() :
                
                self.move(move)
                #print(self)
                moveutility = self.minvalue()
                
                v2 = moveutility[0]
                self.unmove(move)
                '''
                newboard = TicTacToe(self.board, self.turn, self.prune)
                print(self)
                
                newboard.move(move)
                print(newboard)
                v2 = newboard.minvalue()
                '''
                if v2 > v :
                    #print("new move " + str(move))
                    finalmove = move
                    v = v2
        #print(themove)
        #print("Finalmove = " + str(finalmove))
        #print("Utility = " + str(v))
        #print("\n\n")
        return [v, finalmove]

    def minvalue(self) :
        global i
        i = i + 1
        print(i)
        finalmove = 0
        v = 100
        
        if self.terminal() == 0 :
            #print(self)
            #print("Terminal " + str(self.terminal()))
            #print("Utility = -1\nMove = null")
            return [-1, 0]
        elif self.terminal() == 1 :
            #print(self)
            #print("Terminal " + str(self.terminal()))
            #print("Utility = 1\nMove = null")
            return [1, 0]
        elif self.terminal() == -1 :
            #print(self)
            #print("Terminal " + str(self.terminal()))
            #print("Utility = 0\nMove = null")
            return [0, 0]
        elif self.terminal() == 2 :
            for move in self.moves() :
                self.move(move)
                #print(self)
                moveutiltiy = self.maxvalue()
                v2 = moveutiltiy[0]
                
                self.unmove(move)
                '''
                newboard = TicTacToe(self.board, self.turn, self.prune)
                print(self)
                newboard.move(move)
                print(newboard)
                v2 = newboard.maxvalue()
                '''
                if v2 < v :
                    v = v2
                    #print("new move " + str(move))
                    finalmove = move
        #print(themove)
        #print("Finalmove = " + str(finalmove))
        #print("Utility = " + str(v))
        #print("\n")
        #print("\n")
        return [v, finalmove]

    def minmax(self) : #performs minmax and returns a move (1-9)
            #print(self.turn)
            move = 0
            if self.turn : #if X, we want max value of next move
                move = self.maxvalue() 
            else : #if O, we want min value of next move
                move = self.minvalue()
            print("making it out of minmax")
            return move
            #call move on every move available
            #recursively do this until every tree is terminal
            #then we can build tree from bottom up

    def getbestmove(self) :
        #we need to check for Pruning here
        #if self.pruning :
            #self.minmaxab
        #else :
        return self.minmax()

    def move(self, action) : #commits the move. changes the board at the move location
        #action = self.minmax(self.board, self.turn)

        action = action - 1 #list is technically 0-8 but for humans we did 1-9 so make them match

        row = action // 3 #this gets which list to be in. 1-3 = 1, 4-6 = 2, 7-9 = 3
        column = action % 3 #this gets the index in the list

        self.board[row][column] = self.turn #set the board spot to the turn  (0 or 1)

        
        self.turn = int(not(self.turn)) # this makes 1 -> 0 and 0 -> 1

    def unmove(self, action) :
        action = action - 1

        row = action // 3
        column = action % 3

        self.board[row][column] = 2

        self.turn = int(not(self.turn))

    def symbol(self, i) : #returns an O or X that matches the 0 or 1 for turn
        if i == 0 : return "O" 
        elif i == 1: return "X"
        else : return " " #otherwise  2 (or any unexpected values) should return an empty space

    

def startgame(turn) : #this is where the game actually runs and decisions are made
    global pruning #get the global variables (makes it easier)
    global human
    print(human)

    board = TicTacToe([[2, 2, 2], [2, 2, 2], [2, 2, 2]], turn, int(pruning)) #initialize our board

    if human : # if we have a human player we need to let them play
        #we need to take turns until the game is over
        while board.terminal() == 2 :
            #we need to have a way to do human then computer actions
            move = -1
            moves = board.moves()
            while (move not in moves) and move != 0 :
                print("What is your move? Possible moves " + str(board.moves()))
                print("The current board\n" + str(board))
                move = int(input("Your move: "))
            if move == 0 :
                sys.exit("Player ended game.")
            else : 
                board.move(move)
                print("Move selected: " + str(move))
                print(board)
        
        print(board)
        if board.terminal() == -1 :
            print("TIE")
        else :
            print(board.symbol(board.terminal()) + " WINS!")
    else : #if not a human player, just let them move over and over
        while board.terminal() == 2 :
            if board.turn == turn :
                move = -1
                moves = board.moves()
                while (move not in moves) and move != 0 :
                    print("What is your move? Possible moves " + str(board.moves()))
                    print("The current board\n" + str(board))
                    move = int(input("Your move: "))
                if move == 0 :
                    sys.exit("Player ended game.")
                else : 
                    board.move(move)
                    print("Move selected: " + str(move))
            else :
                #print("Pre anything \n" + str(board))
                board.move(board.getbestmove()[1]) #determine best move based on
                print("Post everything \n" + str(board))
                global i
                i = 0


        

    #print(board)


def main() : #do pre-game requirements
    global pruning
    global human

    print("Guttormsen, Hans, A20462410 solution:\nAlgorithm: MiniMax with alpha-beta pruning")

    argnums = len(sys.argv)

    #logic for reading command line from script in discussions but changed var names and added logic (CS480 Jacek Dzikowski)
    #check to make sure we got all input and that arguments entered are valid answers
    if not argnums == 4 or (not (int(sys.argv[1]) == 2 or int(sys.argv[1]) == 1)) or (not (sys.argv[2] == 'X' or sys.argv[2] == 'O')) or (not (int(sys.argv[3]) == 2 or int(sys.argv[3]) == 1)) :
        sys.exit("ERROR: Not enough/too many/illegal input arguments.") 

    if int(sys.argv[1]) == 2 :
        pruning = True

    if int(sys.argv[3]) == 2 :
        human = False

    if sys.argv[2] == 'O' :
        startgame(0)
    else :
        startgame(1)

main() #I'm just doing this bc without it I usually end up with no functions and gross messy code


