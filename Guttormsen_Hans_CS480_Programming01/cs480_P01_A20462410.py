import sys

pruning = False #bool to determine if we should prune the tree
human = True

class TicTacToe :
    def __init__(self, board = [[2, 2, 2], [2, 2, 2], [2, 2, 2]], turn = 0) :
        self.board = board #board is a list of 3 lists of ints 0, 1, or 2. 0 is O, 1 is X, 
        self.turn = turn

    def __str__(self) :
        string = ""
        for j in range(3) :
            lists = self.board[j]
            line = ""
            for i in range(3) :
                if i == 2 :
                    line = line + " " + self.symbol(lists[i]) + " \n"
                else :
                    line = line + " " + self.symbol(lists[i]) + " |"
            string = string + line
            if not i == j :
                string = string + "---+---+---\n"
        return string

    def move(self) :
        self.turn = int(not(self.turn))
    
    def symbol(self, i) :
        if i == 0 : return "O" 
        elif i == 1: return "X"
        else : return " "

def startgame(turn) :
    global pruning
    global human

    board = TicTacToe([[2, 2, 2], [2, 2, 2], [2, 2, 2]], turn)
    print(board)



def main() : #do pre-game requirements
    global pruning
    global human

    print("Guttormsen, Hans, A20462410 solution:\nAlgorithm: MiniMax with alpha-beta pruning")

    argnums = len(sys.argv)

    #logic for reading command line from script in discussions but changed var names and added logic (CS480 Jacek Dzikowski)
    #check to make sure we got all input and that arguments entered are valid answers
    if not argnums == 4 or (not (int(sys.argv[1]) == 2 or int(sys.argv[1]) == 1)) or (not (sys.argv[2] == 'X' or sys.argv[2] == 'O')) or (not (int(sys.argv[3]) == 2 or int(sys.argv[3]) == 1)) :
        sys.exit("ERROR: Not enough/too many/illegal input arguments.") 

    if sys.argv[1] == 2 :
        pruning = True
    
    if sys.argv[3] == 2 :
        human = False

    if sys.argv[2] == 'O' :
        startgame(0)
    else :
        startgame(1)

main() #I'm just doing this bc without it I usually end up with no functions and gross messy code


