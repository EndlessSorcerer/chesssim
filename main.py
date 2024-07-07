'''functionalities needed:
-Add castling
-Implement 50 move rule
-Implement 3 repetitions
'''
class Cell:
    def __init__(self,x,y,piece):
        self.x=x
        self.y=y
        self.piece=piece
class Piece:
    def __init__(self,board,label,x,y,color):
        self.parentboard = board
        self.label=label
        self.x=x
        self.y=y
        self.color=color
        self.isalive=True
        self.validmoves={} # {[[x,y],Piece]
        self.targets={}
        self.symbol=''
        self.hasmoved=False
        self.updatemoves()
    def kill(self):
        self.isalive=False
        self.parentboard.cells[self.x][self.y].piece=None
    def move(self,game,x,y): #outdated
        board=game.curboard
        prev=game.prevstates[-1]
        if islegal(x,y):
            self.hasmoved=True
            piecetokill=None
            for outerlist in self.validmoves:
                coordinates = outerlist[0]
                if x==coordinates[0] and y==coordinates[1]:
                    piecetokill=outerlist[1]
                    break
            if piecetokill!=None:
                piecetokill.kill()
            
            board.cells[self.x][self.y].piece=None
            board.cells[x][y].piece=self
        else:
            print("invalid move")
    def islegal(self,x,y):
        for outerlist in self.validmoves:
            coordinates = outerlist[0]
            if x==coordinates[0] and y==coordinates[1]:
                return True
        return False
class Rook(Piece):
    def __init__(self,label,x,y,color):
        super().__init__(label,x,y,color)
        self.symbol='R'
    def updatemoves(self,game):
        board = game.curboard
        a=[1,0,-1,0]
        b=[0,1,0,-1]
        for i in range(4):
            nx=self.x
            ny=self.y
            while nx>=0 and ny>=0 and nx<8 and ny<8:
                nx=nx+a[i]
                ny=ny+b[i]
                if board.cells[nx][ny].piece!=None:
                    if board.cells[nx][ny].piece.color!=self.color:
                        self.validmoves.add([[nx,ny],board.cells[nx][ny].piece])
                        self.targets.add(board.cells[nx][ny].piece)
                    break
                self.validmoves.add([[nx,ny],None])
class Bishop(Piece):
    def __init__(self,label,x,y,color):
        super().__init__(label,x,y,color)
        self.symbol='B'
    def updatemoves(self,game):
        board = game.curboard
        a=[1,1,-1,-1]
        b=[1,-1,1,-1]
        for i in range(4):
            nx=self.x
            ny=self.y
            while nx>=0 and ny>=0 and nx<8 and ny<8:
                nx=nx+a[i]
                ny=ny+b[i]
                if board.cells[nx][ny].piece!=None:
                    if board.cells[nx][ny].piece.color!=self.color:
                        self.validmoves.add([[nx,ny],board.cells[nx][ny].piece])
                        self.targets.add(board.cells[nx][ny].piece)
                    break
                self.validmoves.add([[nx,ny],None])
class Knight(Piece):
    def __init__(self,label,x,y,color):
        super().__init__(label,x,y,color)
        self.symbol='H'
    def updatemoves(self,game):
        board = game.curboard
        a=[1,1,-1,-1,2,2,-2,-2]
        b=[2,-2,2,-2,1,-1,1,-1]
        for i in range(8):
            nx=self.x+a[i]
            ny=self.y+b[i]
            if board.cells[nx][ny].piece!=None:
                if board.cells[nx][ny].piece.color!=self.color:
                    self.validmoves.add([[nx,ny],board.cells[nx][ny].piece])
                    self.targets.add(board.cells[nx][ny].piece)
                continue
            self.validmoves.add([[nx,ny],None])

class Queen(Piece):
    def __init__(self,label,x,y,color):
        super().__init__(label,x,y,color)
        self.symbol='Q'
    def updatemoves(self,game):
        board = game.curboard
        a=[1,1,-1,-1,1,0,-1,0]
        b=[1,-1,1,-1,0,1,0,-1]
        for i in range(4):
            nx=self.x
            ny=self.y
            while nx>=0 and ny>=0 and nx<8 and ny<8:
                nx=nx+a[i]
                ny=ny+b[i]
                if board.cells[nx][ny].piece!=None:
                    if board.cells[nx][ny].piece.color!=self.color:
                        self.validmoves.add([[nx,ny],board.cells[nx][ny].piece])
                        self.targets.add(board.cells[nx][ny].piece)
                    break
                self.validmoves.add([[nx,ny],None])

class King(Piece):
    def __init__(self,label,x,y,color):
        super().__init__(label,x,y,color)
        self.symbol='K'
    def updatemoves(self,game):
        board = game.curboard
        a=[1,1,1,0,0,-1,-1,-1]
        b=[0,1,-1,1,-1,0,1,-1]
        for i in range(8):
            nx=self.x+a[i]
            ny=self.y+b[i]
            if board.cells[nx][ny].piece!=None:
                if board.cells[nx][ny].piece.color!=self.color:
                    #incomplete implement check functionality for all pieces
                    self.validmoves.add([[nx,ny],board.cells[nx][ny].piece])
                    self.targets.add(board.cells[nx][ny].piece)
                continue
            self.validmoves.add([[nx,ny],None])
    def ischecked(self,board):
        for piece in board.activepieces:
            if piece.color!=self.color:
                if self in piece.targets:
                    return True
        return False

class Pawn(Piece):
    def __init__(self,label,x,y,color):
        super().__init__(label,x,y,color)
        self.symbol='p'
    def updatemoves(self,game):
        board = game.curboard
        prev = game.prevstates[-1]
        if board.cells[self.x+(self.color)][self.y].piece==None:
            self.validmoves.add([[self.x+(self.color),self.y],None])
            if self.hasmoved==False and board.cells[self.x+2*(self.color)][self.y].piece==None:
                self.validmoves.add([[self.x+2*(self.color),self.y],None])
        if board.getcell(self.x+(self.color),self.y+1) and board.getcell(self.x+(self.color),self.y+1).piece!=None and board.getcell(self.x+(self.color),self.y+1).piece.color!=self.color:
            self.validmoves.add([[self.x+(self.color),self.y+1],board.cells[self.x+(self.color)][self.y+1].piece])
            self.targets.add(board.cells[self.x+(self.color)][self.y+1].piece)
        if board.getcell(self.x+(self.color),self.y-1) and board.getcell(self.x+(self.color),self.y-1).piece!=None and board.getcell(self.x+(self.color),self.y-1).piece.color!=self.color:
            self.validmoves.add([[self.x+(self.color),self.y-1],board.cells[self.x+(self.color)][self.y-1].piece])
            self.targets.add(board.cells[self.x+(self.color)][self.y-1].piece)
        if board.getcell(self.x,self.y+1) and board.getcell(self.x,self.y+1).piece!=None and board.getcell(self.x,self.y+1).piece.color!=self.color and isinstance(board.getcell(self.x,self.y+1).piece,Pawn):
            if prev.getcell(self.x+2*(self.color),self.y+1) and prev.getcell(self.x+2*(self.color),self.y+1).piece.color==board.getcell(self.x,self.y+1).piece.color and prev.getcell(self.x+2*(self.color),self.y+1).piece.label==board.getcell(self.x,self.y+1).piece.label:
                self.validmoves.add([[self.x+(self.color),self.y+1],board.cells[self.x][self.y+1].piece])
                self.targets.add(board.cells[self.x][self.y+1].piece)
        if board.getcell(self.x,self.y-1) and board.getcell(self.x,self.y-1).piece!=None and board.getcell(self.x,self.y-1).piece.color!=self.color and isinstance(board.getcell(self.x,self.y-1).piece,Pawn):
            if prev.getcell(self.x+2*(self.color),self.y-1) and prev.getcell(self.x+2*(self.color),self.y-1).piece.color==board.getcell(self.x,self.y-1).piece.color and prev.getcell(self.x+2*(self.color),self.y-1).piece.label==board.getcell(self.x,self.y-1).piece.label:
                self.validmoves.add([[self.x+(self.color),self.y-1],board.cells[self.x][self.y-1].piece])
                self.targets.add(board.cells[self.x][self.y-1].piece)
        

class Board:
    def __init__(self):
        self.cells=[[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8]
        self.players=[]
        self.activepieces=[]
        self.reset()
    def reset(self):
        # figure out what to do with updatemoves
        self.cells[0][0]=Cell(0,0,Rook(self,"rook1",0,0,0))
        self.cells[0][1]=Cell(0,1,Knight(self,"knight1",0,1,0))
        self.cells[0][2]=Cell(0,2,Bishop(self,"bishop1",0,2,0))
        self.cells[0][3]=Cell(0,3,Queen(self,"queen",0,3,0))
        self.cells[0][4]=Cell(0,4,King(self,"king",0,4,0))
        self.cells[0][5]=Cell(0,5,Bishop(self,"bishop2",0,5,0))
        self.cells[0][6]=Cell(0,6,Knight(self,"knight2",0,6,0))
        self.cells[0][7]=Cell(0,7,Rook(self,"rook2",0,7,0))
        self.cells[1][0]=Cell(1,0,Pawn(self,"pawn1",1,0,0))
        self.cells[1][1]=Cell(1,1,Pawn(self,"pawn2",1,1,0))
        self.cells[1][2]=Cell(1,2,Pawn(self,"pawn3",1,2,0))
        self.cells[1][3]=Cell(1,3,Pawn(self,"pawn4",1,3,0))
        self.cells[1][4]=Cell(1,4,Pawn(self,"pawn5",1,4,0))
        self.cells[1][5]=Cell(1,5,Pawn(self,"pawn6",1,5,0))
        self.cells[1][6]=Cell(1,6,Pawn(self,"pawn7",1,6,0))
        self.cells[1][7]=Cell(1,7,Pawn(self,"pawn8",1,7,0))
        self.cells[7][0]=Cell(7,0,Rook(self,"rook1",7,0,1))
        self.cells[7][1]=Cell(7,1,Knight(self,"knight1",7,1,1))
        self.cells[7][2]=Cell(7,2,Bishop(self,"bishop1",7,2,1))
        self.cells[7][3]=Cell(7,3,Queen(self,"queen",7,3,1))
        self.cells[7][4]=Cell(7,4,King(self,"king",7,4,1))
        self.cells[7][5]=Cell(7,5,Bishop(self,"bishop2",7,5,1))
        self.cells[7][6]=Cell(7,6,Knight(self,"knight2",7,6,1))
        self.cells[7][7]=Cell(7,7,Rook(self,"rook2",7,7,1))
        self.cells[6][0]=Cell(6,0,Pawn(self,"pawn1",6,0,1))
        self.cells[6][1]=Cell(6,1,Pawn(self,"pawn2",6,1,1))
        self.cells[6][2]=Cell(6,2,Pawn(self,"pawn3",6,2,1))
        self.cells[6][3]=Cell(6,3,Pawn(self,"pawn4",6,3,1))
        self.cells[6][4]=Cell(6,4,Pawn(self,"pawn5",6,4,1))
        self.cells[6][5]=Cell(6,5,Pawn(self,"pawn6",6,5,1))
        self.cells[6][6]=Cell(6,6,Pawn(self,"pawn7",6,6,1))
        self.cells[6][7]=Cell(6,7,Pawn(self,"pawn8",6,7,1))

        for i in range(2,6):
            for j in range(0,8):
                self.cells[i][j]=Cell(i,j,None)
        for i in range(0,8):
            for j in range(0,8):
                if self.cells[i][j].piece!=None:
                    self.activepieces.append(self.cells[i][j].piece)
    def getcell(self,x,y):
        if x<0 or y<0 or x>7 or y>7:
            return None
        return self.cells[x][y]
    def printboard(self):
        for i in range(0,8):
            for j in range(0,8):
                if self.cells[i][j].piece!=None:
                    print(self.cells[i][j].piece.symbol+" ",end="")
                else:
                    print(". ",end="")
            print("\n")
# class Player:
#     def __init__(self,color):
#         self.color=color

class Game:
    def __init__(self):
        self.curboard = Board()
        self.prevstates = []
        self.whiteturn = True
    def start(self):

    
nboard = Board()
nboard.printboard()