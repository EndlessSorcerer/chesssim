from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.conf import settings

import copy
def checkvalidcell(nx,ny):
    return nx>=0 and ny>=0 and nx<8 and ny<8
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
    def removeinvalidmoves(self):
        for move in self.validmoves:
            ox=self.cell.x
            oy=self.cell.y
            nx=move[0][0]
            ny=move[0][1]
            potentialboard=self.parentgame.move(ox,oy,nx,ny)
            if potentialboard==None:
                print(f"Something went wrong: invalid move {self.label} from {ox}-{oy} to {nx}-{ny} in movelist")
                return
            if potentialboard.kings[self.color].ischecked():
                self.validmoves.remove(move)
            del potentialboard
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
    def updatemoves(self):
        self.updatemoveshelp()
        if not self.parentgame.iniflag:
            self.removeinvalidmoves()
class Rook(Piece):
    def __init__(self,label,cell,color):
        super().__init__(label,cell,color)
        self.symbol='R'
    def updatemoveshelp(self):
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
    def updatemoveshelp(self):
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
    def updatemoveshelp(self):
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
    def updatemoveshelp(self):
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
    def updatemoveshelp(self):
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
                while checkvalidcell(cx,cy+z):
                    cy=cy+z
                    isrook=board.cells[cx][cy].piece!=None and board.cells[cx][cy].piece.symbol=='R'
                    iscastleablerook = isrook and board.cells[cx][cy].piece.color==self.color and board.cells[cx][cy].piece.hasmoved==False
                    if iscastleablerook:
                        self.validmoves.append([[cx,oy+z*2],board.cells[cx][cy].piece])
                        self.targets.append(board.cells[cx][cy].piece)            
    def ischecked(self):
        board=self.cell.board
        for piece in board.activepieces:
            if piece.color!=self.color:
                if self in piece.targets:
                    return True
        return False

class Pawn(Piece):
    def __init__(self,label,cell,color):
        super().__init__(label,cell,color)
        self.symbol='p'
    def updatemoveshelp(self):
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
        self.kings=[None,None]
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
                    if self.cells[i][j].piece.symbol=="K":
                        self.kings[self.cells[i][j].piece.color]=self.cells[i][j].piece
        for piece in self.activepieces:
            piece.updatemoves()
    def getcell(self,x,y):
        if x<0 or y<0 or x>7 or y>7:
            return None
        return self.cells[x][y]
    def serializeboard(self):
        boardstr=""
        for i in range(0,8):
            for j in range(0,8):
                if self.cells[i][j].piece!=None:
                    if self.cells[i][j].piece.color==0:
                        col="w"
                    else:
                        col="b"
                    # print(self.cells[i][j].piece.symbol+col+" ",end="")
                    boardstr=boardstr+self.cells[i][j].piece.symbol+col+" "
                else:
                    # print(". ",end="")
                    boardstr=boardstr+". "
        return boardstr

class Game():
    def __init__(self):
        self.prevstates = []
        self.whiteturn = True
        self.iniflag=True
        self.curboard = Board(self)
        self.iniflag=False
        self.game_end=False
        self.turncount=0
        self.colortomove=0
    def move(self,ox,oy,nx,ny):
        nboard=copy.deepcopy(self.curboard)
        ocell=nboard.cells[ox][oy]
        ncell=nboard.cells[nx][ny]
        if ocell.piece==None:
            return None
        piecetomove=ocell.piece
        if piecetomove.color!=piecetomove.parentgame.colortomove:
            return None
        x=ncell.x
        y=ncell.y
        board=self.curboard
        prev=None
        if len(self.prevstates)>0:
            prev=self.prevstates[-1]
        if piecetomove.islegal(x,y):
            # self.parentgame.prevstates.append(board)
            piecetomove.hasmoved=True
            piecetokill=None
            for outerlist in piecetomove.validmoves:
                coordinates = outerlist[0]
                if x==coordinates[0] and y==coordinates[1]:
                    piecetokill=outerlist[1]
                    break
            if piecetokill!=None:
                piecetokill.kill()
                nboard.cells[ox][oy].piece=None            
            nboard.cells[ox][oy].piece=None
            nboard.cells[x][y].piece=piecetomove
            piecetomove.cell=nboard.cells[x][y]
            # self.parentgame.curboard=nboard
            return nboard
        else:
            return None
    def makepossiblemove(self,ox,oy,nx,ny):
        board=self.curboard
        if board.cells[ox][oy].piece==None:
            print("no piece to move!")
            return
        board.cells[ox][oy].piece.updatemoves()
        nboard=self.move(ox,oy,nx,ny)
        if nboard==None:
            print("invalid move")
        else:
            self.prevstates.append(board)
            self.curboard=nboard
            self.turncount=self.turncount+1
    def gamestart(self):
        while not self.game_end:
            self.colortomove=self.turncount%2
            self.curboard.printboard()
            s=input(f'input your move in the format x1 y1 x2 y2: ')
            l=s.split()
            x1=int(l[0])
            y1=int(l[1])
            x2=int(l[2])
            y2=int(l[3])
            self.makepossiblemove(x1,y1,x2,y2)

# class User(models.Model):
#     username = models.CharField(max_length=255, unique=True)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255)
#     first_name = models.CharField(max_length=100, blank=True)
#     last_name = models.CharField(max_length=100, blank=True)
#     date_joined = models.DateTimeField(default=timezone.now)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)  # Staff user (admin privileges)
#     last_login = models.DateTimeField(null=True, blank=True)

#     def set_password(self, raw_password):
#         self.password = make_password(raw_password)

#     def check_password(self, raw_password):
#         return check_password(raw_password, self.password)

#     def __str__(self):
#         return self.username

#     def clean(self):
#         if not self.username:
#             raise ValidationError("Username is required")
#         if not self.email:
#             raise ValidationError("Email is required")
#         if User.objects.filter(username=self.username).exists():
#             raise ValidationError(f"Username '{self.username}' is already taken.")
#         if User.objects.filter(email=self.email).exists():
#             raise ValidationError(f"Email '{self.email}' is already registered.")

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Create and return a superuser with email, password, and other fields.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    
    objects = CustomUserManager()  # Use the custom manager

    def __str__(self):
        return self.username

class GameWrapper(models.Model):
    white = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='white_games', on_delete=models.CASCADE)
    black = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='black_games', on_delete=models.CASCADE)
    moves = models.TextField(default="")
    current_turn = models.CharField(max_length=10, choices=[('white', 'White'), ('black', 'Black')], default='white')
    status = models.CharField(max_length=10, choices=[('ongoing', 'Ongoing'), ('finished', 'Finished')], default='ongoing')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    serializedboard = models.TextField(default="")
    def to_game_instance(self):
        s=self.moves
        ss=s.split(",")
        game_instance=Game()
        for s in ss:
            if game_instance.game_end:
                break
            game_instance.colortomove=game_instance.turncount%2
            # game.curboard.printboard()
            s=input(f'input your move in the format x1 y1 x2 y2: ')
            l=s.split()
            x1=int(l[0])
            y1=int(l[1])
            x2=int(l[2])
            y2=int(l[3])
            game_instance.makepossiblemove(x1,y1,x2,y2)
        return game_instance
    def add_move(self, move):
        l=move.split()
        x1=int(l[0])
        y1=int(l[1])
        x2=int(l[2])
        y2=int(l[3])
        game_instance = self.to_game_instance()
        game_instance.makepossiblemove(x1,y1,x2,y2)
        self.moves=self.moves+","+move
        self.serializedboard=game_instance.serializeboard()
    def __str__(self):
        return f"Game {self.id}: {self.white} vs {self.black}"

# Create your models here.
