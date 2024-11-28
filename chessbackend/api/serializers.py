from rest_framework import serializers
 
from .models import GameWrapper
 
class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GameWrapper
        fields = ('__all__')