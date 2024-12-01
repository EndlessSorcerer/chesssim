from django.shortcuts import render
from rest_framework import viewsets
from .serializers import GameSerializer, UserLoginSerializer, UserRegistrationSerializer
from .models import GameWrapper, User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny

class GameList(APIView):
    def get(self, request, format=None):
        print("get in GameList")
        if not request.user.is_authenticated:
            return Response(
                {'detail': 'Authentication credentials were not provided.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        # games = GameWrapper.objects.all()
        games = GameWrapper.objects.filter(
            white=request.user
        ) | GameWrapper.objects.filter(
            black=request.user
        )
        serializer = GameSerializer(games, many=True) 
        return Response(serializer.data)

    def post(self, request, format=None):
        print("post in GameList")
        if not request.user.is_authenticated:
            return Response(
                {'detail': 'Authentication credentials were not provided.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        opponent_username = request.data.get('opponent')  # Get the opponent's username from the request
        
        if not opponent_username:
            return Response(
                {'detail': 'Opponent username is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            opponent = User.objects.get(username=opponent_username)
        except User.DoesNotExist:
            return Response(
                {'detail': 'Opponent not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Make sure the opponent is not the same as the user
        if opponent == request.user:
            return Response(
                {'detail': 'You cannot play with yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        white=request.user
        black=opponent
        game = GameWrapper.objects.create(
            white=white,
            black=black,
            status='ongoing',  # Default status
            current_turn='white',  # White goes first
        )
        serializer = GameSerializer(game)
        # if serializer.is_valid():
        #     # serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
class GameMatch(APIView):
    permission_classes = [AllowAny]
    def get(self,request,game_id, format=None):
        print("sdad")
        # if not request.user.is_authenticated:
        #     print("ads")
        #     return Response(
        #         {'detail': 'Authentication credentials were not provided.'},
        #         status=status.HTTP_401_UNAUTHORIZED
        #     )
        try:
            game = GameWrapper.objects.get(id=game_id)
        except GameWrapper.DoesNotExist:
            return Response({"error": "Game not found"}, status=status.HTTP_404_NOT_FOUND)
        if game.white != request.user and game.black != request.user:
            return Response(
                {"error": "You are not a participant in this game."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = GameSerializer(game)
        return Response(serializer.data) 

    def put(self, request,game_id, format=None):
        # if not request.user.is_authenticated:
        #     return Response(
        #         {'detail': 'Authentication credentials were not provided.'},
        #         status=status.HTTP_401_UNAUTHORIZED
        #     )
        print("put in GameMatch")
        try:
            game = GameWrapper.objects.get(id=game_id)
        except GameWrapper.DoesNotExist:
            return Response({"error": "Game not found"}, status=status.HTTP_404_NOT_FOUND)
        if game.white != request.user and game.black != request.user:
            return Response(
                {"error": "You are not a participant in this game."},
                status=status.HTTP_403_FORBIDDEN
            )
        move = request.data.get("move")
        if not move:
            return Response({"error": "Move is required"}, status=status.HTTP_400_BAD_REQUEST)
        game.add_move(move)
        game.save()
        serializer = GameSerializer(game) 
        return Response(serializer.data)

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        print("post in login")
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'message': 'Login successful',
                'access_token': access_token,
                'refresh_token': str(refresh),
            }, status=status.HTTP_200_OK)

        return Response({
            'message': 'Invalid credentials'
        }, status=status.HTTP_400_BAD_REQUEST)

# class GameViewSet(viewsets.ModelViewSet):
#     queryset = GameWrapper.objects.all()
#     serializer_class = GameSerializer
# Create your views here.
