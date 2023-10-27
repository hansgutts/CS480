class TicTacToe :
    def __init__(self, board = [[2, 2, 2], [2, 2, 2], [2, 2, 2]], turn = 0) :
        self.board = board #board is a list of 3 lists of ints 0, 1, or 2. 0 is O, 1 is X, 
        self.turn = turn

    def __str__(self) :
        for lists in self.board :
            line = ""
            for i in range(3) :
                if i == 2 :
                    line = line + " " + self.symbol(lists[i]) + " "
                else :
                    line = line + " " + self.symbol(lists[i]) + " |"
            print("---+---+---")

    def move(self) :
        self.turn = int(not(self.turn))
    
    def symbol(self, i) :
        if i == 0 : return "O" 
        elif i == 1: return "X"
        else : return " "