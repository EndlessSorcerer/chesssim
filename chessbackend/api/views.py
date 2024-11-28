from django.shortcuts import render
from rest_framework import viewsets
from .serializers import GameSerializer
from .models import GameWrapper
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class GameList(APIView):
    def get(self, request, format=None):
        games = GameWrapper.objects.all() 
        serializer = GameSerializer(games, many=True) 
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
class GameMatch(APIView):
    def get(self, request,game_id, format=None):
        try:
            game = GameWrapper.objects.get(id=game_id)
        except GameWrapper.DoesNotExist:
            return Response({"error": "Game not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = GameSerializer(game)
        return Response(serializer.data) 

    def put(self, request,game_id, format=None):
        try:
            game = GameWrapper.objects.get(id=game_id)
        except GameWrapper.DoesNotExist:
            return Response({"error": "Game not found"}, status=status.HTTP_404_NOT_FOUND)
        move = request.data.get("move")
        if not move:
            return Response({"error": "Move is required"}, status=status.HTTP_400_BAD_REQUEST)
        game.add_move(move)
        serializer = GameSerializer(game) 
        return Response(serializer.data)



# class GameViewSet(viewsets.ModelViewSet):
#     queryset = GameWrapper.objects.all()
#     serializer_class = GameSerializer
# Create your views here.
