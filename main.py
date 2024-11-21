'''functionalities needed:
-Add castling
-Add checking
-Implement 50 move rule
-Implement 3 repetitions
-Refactor
'''
import copy
class Cell:
    def __init__(self,board,x,y,piece):
        self.x=x
        self.y=y
        self.piece=piece
        self.board=board
    def __str__(self):
        return f"Cell({self.x}, {self.y}){' with ' + str(self.piece) if self.piece else ' empty'}"
class Piece:
    def __init__(self,label,cell,color):
        self.parentgame = cell.board.game
        self.label=label
        # self.x=x
        # self.y=y
        self.cell=cell
        self.color=color
        self.isalive=True
        self.validmoves=[] # {[[x,y],Piece]
        self.targets=[]
        self.symbol=''
        self.hasmoved=False
        self.updatemoves()
    def kill(self):
        self.isalive=False
    def move(self,ncell):
        x=ncell.x
        y=ncell.y
        board=self.parentgame.curboard
        prev=self.parentgame.prevstates[-1]
        if islegal(x,y):
            nboard=copy.deepcopy(board)
            self.parentgame.prevstates.append(board)
            self.hasmoved=True
            piecetokill=None
            for outerlist in self.validmoves:
                coordinates = outerlist[0]
                if x==coordinates[0] and y==coordinates[1]:
                    piecetokill=outerlist[1]
                    break
            if piecetokill!=None:
                piecetokill.kill()
                nboard.cells[piecetokill.x][piecetokill.y].piece=None
            
            nboard.cells[self.x][self.y].piece=None
            nboard.cells[x][y].piece=self
            self.parentgame.curboard=nboard
        else:
            print("invalid move")
    def islegal(self,x,y):
        for outerlist in self.validmoves:
            coordinates = outerlist[0]
            if x==coordinates[0] and y==coordinates[1]:
                return True
        return False
class Rook(Piece):
    def __init__(self,label,cell,color):
        super().__init__(label,cell,color)
        self.symbol='R'
    def updatemoves(self):
        board = self.cell.board
        a=[1,0,-1,0]
        b=[0,1,0,-1]
        for i in range(4):
            nx=self.cell.x
            ny=self.cell.y
            while nx+a[i]>=0 and ny+b[i]>=0 and nx+a[i]<8 and ny+b[i]<8:
                nx=nx+a[i]
                ny=ny+b[i]
                if board.cells[nx][ny].piece!=None:
                    if board.cells[nx][ny].piece.color!=self.color:
                        self.validmoves.append([[nx,ny],board.cells[nx][ny].piece])
                        self.targets.append(board.cells[nx][ny].piece)
                    break
                self.validmoves.append([[nx,ny],None])
class Bishop(Piece):
    def __init__(self,label,cell,color):
        super().__init__(label,cell,color)
        self.symbol='B'
    def updatemoves(self):
        board = self.cell.board
        a=[1,1,-1,-1]
        b=[1,-1,1,-1]
        for i in range(4):
            nx=self.cell.x
            ny=self.cell.y
            while nx+a[i]>=0 and ny+b[i]>=0 and nx+a[i]<8 and ny+b[i]<8:
                nx=nx+a[i]
                ny=ny+b[i]
                if board.cells[nx][ny].piece!=None:
                    if board.cells[nx][ny].piece.color!=self.color:
                        self.validmoves.append([[nx,ny],board.cells[nx][ny].piece])
                        self.targets.append(board.cells[nx][ny].piece)
                    break
                self.validmoves.append([[nx,ny],None])
class Knight(Piece):
    def __init__(self,label,cell,color):
        super().__init__(label,cell,color)
        self.symbol='H'
    def updatemoves(self):
        board = self.cell.board
        a=[1,1,-1,-1,2,2,-2,-2]
        b=[2,-2,2,-2,1,-1,1,-1]
        for i in range(8):
            nx=self.cell.x+a[i]
            ny=self.cell.y+b[i]
            if nx>=0 and ny>=0 and nx<8 and ny<8:
                if board.cells[nx][ny].piece!=None:
                    if board.cells[nx][ny].piece.color!=self.color:
                        self.validmoves.append([[nx,ny],board.cells[nx][ny].piece])
                        self.targets.append(board.cells[nx][ny].piece)
                    continue
                self.validmoves.append([[nx,ny],None])

class Queen(Piece):
    def __init__(self,label,cell,color):
        super().__init__(label,cell,color)
        self.symbol='Q'
    def updatemoves(self):
        board = self.cell.board
        a=[1,1,-1,-1,1,0,-1,0]
        b=[1,-1,1,-1,0,1,0,-1]
        for i in range(4):
            nx=self.cell.x
            ny=self.cell.y
            while nx+a[i]>=0 and ny+b[i]>=0 and nx+a[i]<8 and ny+b[i]<8:
                nx=nx+a[i]
                ny=ny+b[i]
                if board.cells[nx][ny].piece!=None:
                    if board.cells[nx][ny].piece.color!=self.color:
                        self.validmoves.append([[nx,ny],board.cells[nx][ny].piece])
                        self.targets.append(board.cells[nx][ny].piece)
                    break
                self.validmoves.append([[nx,ny],None])

class King(Piece):
    def __init__(self,label,cell,color):
        super().__init__(label,cell,color)
        self.symbol='K'
    def updatemoves(self):
        board = self.cell.board
        a=[1,1,1,0,0,-1,-1,-1]
        b=[0,1,-1,1,-1,0,1,-1]
        for i in range(8):
            nx=self.cell.x+a[i]
            ny=self.cell.y+b[i]
            if nx>=0 and ny>=0 and nx<8 and ny<8:
                if board.cells[nx][ny].piece!=None:
                    if board.cells[nx][ny].piece.color!=self.color:
                        #incomplete implement check functionality for all pieces
                        self.validmoves.append([[nx,ny],board.cells[nx][ny].piece])
                        self.targets.append(board.cells[nx][ny].piece)
                    continue
                self.validmoves.append([[nx,ny],None])
    def ischecked(self,board):
        for piece in board.activepieces:
            if piece.color!=self.color:
                if self in piece.targets:
                    return True
        return False

class Pawn(Piece):
    def __init__(self,label,cell,color):
        super().__init__(label,cell,color)
        self.symbol='p'
    def updatemoves(self):
        board = self.cell.board
        # prev = board.game.prevstates[-1]
        direction=self.color
        cx=self.cell.x
        cy=self.cell.y
        if board.cells[cx+direction][cy].piece==None:
            self.validmoves.append([[cx+direction,cy],None])
            if self.hasmoved==False and board.cells[cx+2*direction][cy].piece==None:
                self.validmoves.append([[cx+2*direction,cy],None])
        if board.getcell(cx+direction,cy+1) and board.getcell(cx+direction,cy+1).piece!=None and board.getcell(cx+direction,cy+1).piece.color!=direction:
            self.validmoves.append([[cx+direction,cy+1],board.cells[cx+direction][cy+1].piece])
            self.targets.append(board.cells[cx+direction][cy+1].piece)
        if board.getcell(cx+direction,cy-1) and board.getcell(cx+direction,cy-1).piece!=None and board.getcell(cx+direction,cy-1).piece.color!=direction:
            self.validmoves.append([[cx+direction,cy-1],board.cells[cx+direction][cy-1].piece])
            self.targets.append(board.cells[cx+direction][cy-1].piece)
        if board.getcell(cx,cy+1) and board.getcell(cx,cy+1).piece!=None and board.getcell(cx,cy+1).piece.color!=direction and isinstance(board.getcell(cx,cy+1).piece,Pawn):
            if prev.getcell(cx+2*direction,cy+1) and prev.getcell(cx+2*direction,cy+1).piece.color==board.getcell(cx,cy+1).piece.color and prev.getcell(cx+2*direction,cy+1).piece.label==board.getcell(cx,cy+1).piece.label:
                self.validmoves.append([[cx+direction,cy+1],board.cells[cx][cy+1].piece])
                self.targets.append(board.cells[cx][cy+1].piece)
        if board.getcell(cx,cy-1) and board.getcell(cx,cy-1).piece!=None and board.getcell(cx,cy-1).piece.color!=direction and isinstance(board.getcell(cx,cy-1).piece,Pawn):
            if prev.getcell(cx+2*direction,cy-1) and prev.getcell(cx+2*direction,cy-1).piece.color==board.getcell(cx,cy-1).piece.color and prev.getcell(cx+2*direction,cy-1).piece.label==board.getcell(cx,cy-1).piece.label:
                self.validmoves.append([[cx+direction,cy-1],board.cells[cx][cy-1].piece])
                self.targets.append(board.cells[cx][cy-1].piece)
        

class Board:
    def __init__(self,game):
        self.cells=[[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8]
        self.players=[]
        self.activepieces=[]
        self.game=game
        self.reset()
    def reset(self):
        # figure out what to do with updatemoves
        # print(self.cells)
        for i in range(0,8):
            for j in range(0,8):
                self.cells[i][j]=Cell(self,i,j,None)
        # print(str(self.cells))
        # for i in range(0,8):
        #     for j in range(0,8):
        #         print(str(self.cells[i][j]))

        self.cells[0][0].piece=Rook("rook1",self.cells[0][0],0)
        self.cells[0][1].piece=Knight("knight1",self.cells[0][1],0)
        self.cells[0][2].piece=Bishop("bishop1",self.cells[0][2],0)
        self.cells[0][3].piece=Queen("queen",self.cells[0][3],0)
        self.cells[0][4].piece=King("king",self.cells[0][4],0)
        self.cells[0][5].piece=Bishop("bishop2",self.cells[0][5],0)
        self.cells[0][6].piece=Knight("knight2",self.cells[0][6],0)
        self.cells[0][7].piece=Rook("rook2",self.cells[0][7],0)
        self.cells[1][0].piece=Pawn("pawn1",self.cells[1][0],0)
        self.cells[1][1].piece=Pawn("pawn2",self.cells[1][1],0)
        self.cells[1][2].piece=Pawn("pawn3",self.cells[1][2],0)
        self.cells[1][3].piece=Pawn("pawn4",self.cells[1][3],0)
        self.cells[1][4].piece=Pawn("pawn5",self.cells[1][4],0)
        self.cells[1][5].piece=Pawn("pawn6",self.cells[1][5],0)
        self.cells[1][6].piece=Pawn("pawn7",self.cells[1][6],0)
        self.cells[1][7].piece=Pawn("pawn8",self.cells[1][7],0)
        self.cells[7][0].piece=Rook("rook1",self.cells[7][0],1)
        self.cells[7][1].piece=Knight("knight1",self.cells[7][1],1)
        self.cells[7][2].piece=Bishop("bishop1",self.cells[7][2],1)
        self.cells[7][3].piece=Queen("queen",self.cells[7][3],1)
        self.cells[7][4].piece=King("king",self.cells[7][4],1)
        self.cells[7][5].piece=Bishop("bishop2",self.cells[7][5],1)
        self.cells[7][6].piece=Knight("knight2",self.cells[7][6],1)
        self.cells[7][7].piece=Rook("rook2",self.cells[7][7],1)
        self.cells[6][0].piece=Pawn("pawn1",self.cells[6][0],1)
        self.cells[6][1].piece=Pawn("pawn2",self.cells[6][1],1)
        self.cells[6][2].piece=Pawn("pawn3",self.cells[6][2],1)
        self.cells[6][3].piece=Pawn("pawn4",self.cells[6][3],1)
        self.cells[6][4].piece=Pawn("pawn5",self.cells[6][4],1)
        self.cells[6][5].piece=Pawn("pawn6",self.cells[6][5],1)
        self.cells[6][6].piece=Pawn("pawn7",self.cells[6][6],1)
        self.cells[6][7].piece=Pawn("pawn8",self.cells[6][7],1)

        # for i in range(0,8):
        #     for j in range(0,8):
        #         print(str(self.cells[i][j]))

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
        self.prevstates = []
        self.whiteturn = True
        self.curboard = Board(self)
    # def start(self):

game=Game()
game.curboard.printboard()