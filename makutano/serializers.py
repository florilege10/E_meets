from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile, Publication, Like, Abonnement, Message, Photo
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'email', 'name', 'phone_number', 'sexe', 'address', 'is_active']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'email', 'name', 'phone_number', 'sexe', 'address', 'is_active']

class PublicationSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = Publication
        fields = ['id', 'profile', 'image', 'timestamp']


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'profile', 'image', 'uploaded_at']

class CustomRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    sexe = serializers.ChoiceField(choices=[("H", "Homme"), ("F", "Femme")], required=True)
    address = serializers.CharField(max_length=255, required=True)
    phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True)

    class Meta:
        model = Profile
        fields = ['email', 'password', 'phone_number', 'sexe', 'address', 'name']

    def create(self, validated_data):
        profile = Profile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            sexe=validated_data['sexe'],
            address=validated_data['address']
        )
        return profile

class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True)
    sexe = serializers.ChoiceField(choices=[("H", "Homme"), ("F", "Femme")])
    address = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)

    def validate_email(self, value):
        if Profile.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà pris.")
        return value

    def create(self, validated_data):
        profile = Profile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            sexe=validated_data['sexe'],
            address=validated_data['address']
        )
        return profile



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Utilisez email pour l'authentification
        user = authenticate(request=self.context.get('request'), email=email, password=password)
        
        if user is None:
            raise serializers.ValidationError("Identifiants invalides.")
        
        # Vérifiez si l'utilisateur est actif
        if not user.is_active:
            raise serializers.ValidationError("Ce compte est désactivé.")
        
        # Ajoutez l'utilisateur aux attributs validés
        attrs['user'] = user
        return attrs


from rest_framework import serializers

class LoginFormSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)



class PhotoPublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['image']

    def create(self, validated_data):
        user = self.context['request'].user
        return Photo.objects.create(profile=user, **validated_data)
    





from rest_framework import serializers
from .models import Photo

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'profile', 'image', 'uploaded_at']
        read_only_fields = ['id', 'profile', 'uploaded_at']


























#SERIALIZERS POUR L HOMME



class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'profile', 'photo', 'timestamp']
        read_only_fields = ['id', 'timestamp']




class AbonnementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Abonnement
        fields = ['id', 'profile', 'start_date', 'duration_days', 'tarif', 'expires_at', 'is_active']
        read_only_fields = ['id', 'start_date', 'expires_at', 'is_active']




class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender','receiver', 'content', 'image', 'timestamp', 'is_read', 'parent_message']
        read_only_fields = ['id','sender' ,'timestamp']