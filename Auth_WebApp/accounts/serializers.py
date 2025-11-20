# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # Add phone_number explicitly
    phone_number = serializers.CharField(required=True)

    class Meta:
        model = User
        # Include phone_number in fields
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'phone_number')
        extra_kwargs = {
            'username': {'required': False} # We will auto-generate this from email
        }

    def create(self, validated_data):
        # Force username to be the email address
        email = validated_data['email']
        
        user = User.objects.create_user(
            username=email,  # <--- Force Username = Email
            email=email,
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user