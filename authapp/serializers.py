from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def save(self):
        user = User(username=self.validated_data['username'], email=self.validated_data['email'])
        user.set_password(self.validated_data['password'])
        user.save()

        return user
