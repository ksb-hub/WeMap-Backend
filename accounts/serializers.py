from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'nickname', 'dis_level', 'created_at', 'updated_at', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            nickname=validated_data['nickname'],
            password=validated_data['password'],
            dis_level=validated_data['dis_level']   # Assuming you want to pass dis_level during user creation
        )
        return user