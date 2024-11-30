from rest_framework import serializers
 
from .models import GameWrapper, User
 
class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GameWrapper
        fields = ('__all__')

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password before saving
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)