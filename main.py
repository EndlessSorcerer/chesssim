'''functionalities needed:
-Add castling (partially added, when making move with king if target is same color then it'd be rook and add castling logic there)
-Add checking
-Implement 50 move rule
-Implement 3 repetitions
-Refactor
-En passant (done but needs testing)
-Add promotion
'''
import copy
def checkvalidcell(nx,ny):
    return checkvalidcell(nx,ny)
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
    def printmoves(self):
        print(f"printing moves for {self.label}")
        for move in self.validmoves:
            print(move)
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
            while checkvalidcell(nx+a[i],ny+b[i]):
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
            while checkvalidcell(nx+a[i],ny+b[i]):
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
            if checkvalidcell(nx,ny):
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
            while checkvalidcell(nx+a[i],ny+b[i]):
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
            if checkvalidcell(nx,ny):
                if board.cells[nx][ny].piece!=None:
                    if board.cells[nx][ny].piece.color!=self.color:
                        #incomplete implement check functionality for all pieces
                        self.validmoves.append([[nx,ny],board.cells[nx][ny].piece])
                        self.targets.append(board.cells[nx][ny].piece)
                    continue
                self.validmoves.append([[nx,ny],None])
        if self.hasmoved==False:
            for z in [1,-1]:
                cx=self.cell.x
                oy=self.cell.y
                cy=self.cell.y
                while checkvalidcell(cx,cy):
                    cy=cy+z
                    isrook=board.cells[cx][cy].piece!=None and board.cells[cx][cy].piece.symbol=='R'
                    iscastleablerook = isrook and board.cells[cx][cy].piece.color==self.color and board.cells[cx][cy].piece.hasmoved==False
                    if castleablerook:
                        self.validmoves.append([[cx,oy+z*2],board.cells[cx][cy].piece])
                        self.targets.append(board.cells[cx][cy].piece)


            
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
        prev=None
        if len(board.game.prevstates)>0:
            prev = board.game.prevstates[-1]
        # direction=self.color
        if self.color==0:
            direction=1
        else:
            direction=-1
        # print(f"direction for {self.label} {direction}")
        cx=self.cell.x
        cy=self.cell.y
        # print(f"cx {cx} cx+direction {cx+direction}")

        #Normal forward movement
        if board.cells[cx+direction][cy].piece==None:
            self.validmoves.append([[cx+direction,cy],None])
            if self.hasmoved==False and board.cells[cx+2*direction][cy].piece==None:
                self.validmoves.append([[cx+2*direction,cy],None])
        
        #Diagonal captures
        for z in [1,-1]:
            nx=cx+direction
            ny=cy+z
            isvalidcell=board.getcell(nx,ny) and board.getcell(nx,ny).piece!=None
            if isvalidcell and board.getcell(nx,ny).piece.color!=direction:
                self.validmoves.append([[nx,ny],board.cells[nx][ny].piece])
                self.targets.append(board.cells[nx][ny].piece)

        #For en passant check (work in progress)
        if prev!=None:
            for z in [1,-1]:
                nx=cx
                ny=cy+z
                isvalidcell=board.getcell(nx,ny)
                if isvalidcell and board.getcell(nx,ny).piece!=None and board.getcell(nx,ny).piece.color!=direction and isinstance(board.getcell(nx,ny).piece,Pawn):
                    if prev.getcell(nx+2*direction,ny) and prev.getcell(nx+2*direction,ny).piece.color==board.getcell(nx,ny).piece.color and prev.getcell(nx+2*direction,ny).piece.label==board.getcell(nx,ny).piece.label:
                        self.validmoves.append([[nx+direction,ny],board.cells[nx][ny].piece])
                        self.targets.append(board.cells[nx][ny].piece)


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
        for piece in self.activepieces:
            piece.updatemoves()
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

class Game:
    def __init__(self):
        self.prevstates = []
        self.whiteturn = True
        self.curboard = Board(self)
    # def start(self):

game=Game()
game.curboard.printboard()
game.curboard.cells[0][6].piece.printmoves()


#Scrap
#previous en passant code
    # isvalidcell3=board.getcell(cx,cy+1)

    # if isvalidcell3 and board.getcell(cx,cy+1).piece!=None and board.getcell(cx,cy+1).piece.color!=direction and isinstance(board.getcell(cx,cy+1).piece,Pawn):
    #     if prev.getcell(cx+2*direction,cy+1) and prev.getcell(cx+2*direction,cy+1).piece.color==board.getcell(cx,cy+1).piece.color and prev.getcell(cx+2*direction,cy+1).piece.label==board.getcell(cx,cy+1).piece.label:
    #         self.validmoves.append([[cx+direction,cy+1],board.cells[cx][cy+1].piece])
    #         self.targets.append(board.cells[cx][cy+1].piece)

    # isvalidcell4=board.getcell(cx,cy-1)

    # if isvalidcell4 and board.getcell(cx,cy-1).piece!=None and board.getcell(cx,cy-1).piece.color!=direction and isinstance(board.getcell(cx,cy-1).piece,Pawn):
    #     if prev.getcell(cx+2*direction,cy-1) and prev.getcell(cx+2*direction,cy-1).piece.color==board.getcell(cx,cy-1).piece.color and prev.getcell(cx+2*direction,cy-1).piece.label==board.getcell(cx,cy-1).piece.label:
    #         self.validmoves.append([[cx+direction,cy-1],board.cells[cx][cy-1].piece])
    #         self.targets.append(board.cells[cx][cy-1].piece)