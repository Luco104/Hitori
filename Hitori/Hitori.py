import random
import g2d
from boardgame import BoardGame
from boardgameGUI import BoardGameGui, gui_play

class Hitori(BoardGame):

    def __init__(self, side=8):
        self._cols, self._rows = side, side
        self._board = []
        #self._board = [[random.randint(1, 9) for x in range(side)] for y in range(side)]
        with open("matrix.txt") as file:
            for i in file:
                i = i.strip()
                self._board.append(i.split(","))
        self._board2 = [["NULL" for y in range(side)] for x in range(side)]
        


    def cols(self) -> int:
        return self._cols

    def rows(self) -> int:
        return self._rows
       
    def play_at(self, x:int, y:int):
        
        if 0 <= x < self._cols and 0 <= y < self._rows:
            
            if self._board2[y][x] == "CIRCLED" or self._board2[y][x] == "NULL":
                self._board2[y][x] = "BLACKENED"
            else:
                self._board2[y][x] = "NULL"
                
            
    def flag_at(self, x:int, y:int):
        
        if 0 <= x < self._cols and 0 <= y < self._rows:
            
            if self._board2[y][x] == "NULL":
                self._board2[y][x] = "CIRCLED"
                

    def blacken_doubles(self, x:int, y:int): #se un numero è cerchiato, annerisce i suoi doppi nella riga/colonna corrispondente
        if self._board2[y][x] == "CIRCLED":
            num = self._board[y][x]
            
            for i in range(self._cols):
                if i != x and self._board[y][i] == num and self._board2[y][i] != "CIRCLED":
                    self._board2[y][i] = "BLACKENED"

            for i in range(self._rows):
                if i != x and self._board[i][x] == num and self._board2[i][x] != "CIRCLED":
                    self._board2[i][x] = "BLACKENED"


    def all_circle_around(self, x:int, y:int): #cerchia celle intorno
        
        if 0 <= x < self._cols and 0 <= y < self._rows:
            
            for dx, dy in ((0, -1), (1, 0),
                            (0, 1), (-1, 0)):
                if 0 <= x+dx < self._cols and 0 <= y+dy < self._rows:
                        self._board2[y+dy][x+dx] = "CIRCLED"

                
    def value_at(self, x:int, y:int) -> str:
        
        if 0 <= x <= self._cols and 0 <= y <= self._rows:
            
            if self._board2[y][x] == "BLACKENED":
                return str(self._board[y][x]) + 'X'
            
            elif self._board2[y][x] == "CIRCLED":
                return str(self._board[y][x]) + "O"
        return str(self._board[y][x]) + ' '

    
    def check4whitecells(self, y, x, Boole_matrix):
        
        '''se nelle 4 direzioni cardinali dx e dy c'è almeno una cella bianca, la matrice booleana assume valore TRUE nella cella corrispondente;
        tramite ricorsione il contatore memorizza il numero di celle con valore TRUE adiacenti tra loro'''
        
        counter = 1
        for dx, dy in ((0, 0), (0, -1), (1, 0),
                            (0, 1), (-1, 0)):
            if 0 <= x + dx < self._cols and 0 <= y + dy < self._rows:
                if self._board2[y+dy][x+dx] == "NULL" and Boole_matrix[y+dy][x+dx] == False:
                    Boole_matrix[y+dy][x+dx] = True
                    counter += self.check4whitecells(x+dx, y+dy, Boole_matrix)
        return counter
        
    def finished(self) -> bool:
        
        total_2 = 0
        
        for y in range(self._rows):
            for x in range(self._cols):
        
                if self._board2[y][x] != "BLACKENED": #se trova una cella non annerita controlla che non ci siano numeri doppi nella colonna/riga
                    total_2 += 1
                    num = self._board[y][x]
                    for i in range(self._cols):
                        if i != x and self._board[y][i] == num and self._board2[y][i] != "BLACKENED":
                            
                            #print("numero da annerire:", self._board[y][i],"posizione", y, x,
                            #      "OPPURE:", num, "Posizione", y, i)
                            
                            return False
                    
                    for i in range(self._rows):
                        if i != y and self._board[i][x] == num and self._board2[i][x] != "BLACKENED":
                            
                            #print("numero da annerire:", self._board[i][x],"posizione", y, x,
                            #     "OPPURE:", num, "Posizione", i, x)
                            
                            return False

                '''if self._board2[y][x] == "BLACKENED":
                    #controlla che non ci siano celle annerite adiacenti 
                    for dx, dy in ((0, -1), (1, 0),
                                   (0, 1), (-1, 0)):
                        
                        if 0 <= x + dx < self._cols and 0 <= y + dy < self._rows:
                            if self._board2[y+dy][x+dx] == "BLACKENED":
                                
                                #print("cella nera adiacente:", self._board[y][x])
                                
                                
                                return False'''
                            
        #finchè il numero di celle bianche e il numero di valori TRUE non sono uguali, il gioco non è risolto
        Boole_matrix = [[False for y in range(self._cols)] for x in range(self._rows)]
        pippo = False
        ttl = 0
        
        while not pippo:
            if self._board2[0][ttl] != "BLACKENED":
                pippo = True
                Boole_matrix[0][ttl] = True
                total = self.check4whitecells(0, ttl, Boole_matrix)
                
            ttl += 1
        #print(total, total_2)
        
        if total != total_2:
            return False

        if not self.wrong():
            return False
        
        return True
    
    def wrong(self) -> bool:
        for x in range(self._rows):
            for y in range(self._cols):
                
                if self._board2[y][x] == "BLACKENED":
                    #controlla che non ci siano celle annerite contigue 
                    for dx, dy in ((0, -1), (1, 0),
                                   (0, 1), (-1, 0)):
                        
                        if 0 <= x + dx < self._cols and 0 <= y + dy < self._rows:
                            if self._board2[y+dy][x+dx] == "BLACKENED":
                                
                                print("cella nera adiacente:", self._board[y][x])
                                g2d.alert("mossa errata")
                                return False
                            
                if self._board2[y][x] == "CIRCLED":
                    #controlla che non ci siano celle cerchiate uguali e allineate
                    num = self._board[y][x]
                    for i in range(self._cols):
                        if i != x and self._board[y][i] == num and self._board2[y][i] == "CIRCLED":
                            
                            return False
                    
                    for i in range(self._rows):
                        if i != y and self._board[i][x] == num and self._board2[i][x] == "CIRCLED":
                            
                            return False
        return True
                        
    def message(self) -> str:
        return "HAI VINTO"
    
def main():
    game = Hitori()
    gui_play(game)

main()
        
