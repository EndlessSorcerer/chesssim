from rest_framework import serializers
 
from .models import GameWrapper, User
 
class GameSerializer(serializers.ModelSerializer):
    white = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    black = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    class Meta:
        model = GameWrapper
        fields = ('__all__')
        # extra_kwargs = {
        #     'url': {'view_name': 'gamewrapper-detail'}  # Ensure this matches the view name
        # }

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