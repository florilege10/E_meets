from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from .models import Profile, Publication, Like, Abonnement, Message, Photo
from .serializers import *
from .permissions import IsMan, IsOwnerOrReadOnly, IsWoman, HasActiveAbonnement

# VUES COMMUNES

# Vue pour l'inscription des utilisateurs
class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        profile = serializer.save()
        return Response({'message': 'Utilisateur créé avec succès', 'user_id': profile.id}, status=status.HTTP_201_CREATED)

# Vue personnalisée pour la connexion des utilisateurs
class CustomLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        redirect_url = '/men/publications/' if user.sexe == 'H' else '/women/publications/'
        return Response({'token': token.key, 'redirect_url': redirect_url}, status=status.HTTP_200_OK)

# Vue pour la connexion des utilisateurs
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer
from rest_framework.permissions import IsAuthenticated

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        # Sérialiser les données de la requête
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Récupérer l'utilisateur valide
        user = serializer.validated_data['user']

        # Obtenir ou créer un token
        token, _ = Token.objects.get_or_create(user=user)

        # Retourner la réponse avec le token et l'URL de redirection en fonction du sexe
        redirect_url = '/men/publications/' if user.sexe == 'H' else '/women/publications/'
        return Response({
            'token': token.key,
            'redirect_url': redirect_url
        }, status=status.HTTP_200_OK)
    


from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def home(request):
    return Response({
        "message": "Bienvenue sur Makutano API",
        "endpoints": {
            "inscription": "/api/register/",
            "connexion": "/api/login/",
            "documentation": "À implémenter",
            "pour_les_hommes": {
                "publications": "/api/men/publications/",
                "photos": "/api/men/photos/",
                "abonnements": "/api/men/abonnements/"
            },
            "pour_les_femmes": {
                "publications": "/api/women/publications/",
                "photos": "/api/women/photos/"
            }
        }
    })



# Vue pour gérer les informations utilisateur (affichage et mise à jour)
class UserView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

# VUES POUR LES FEMMES

# Vue pour gérer les publications des femmes
class PublicationListForWomenView(generics.ListCreateAPIView):
    serializer_class = PublicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsWoman]

    def get_queryset(self):
        return Publication.objects.filter(profile=self.request.user)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user)

# Vue pour gérer les photos des femmes
class PhotoListForWomenView(generics.ListCreateAPIView):
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticated, IsWoman]

    def get_queryset(self):
        return Photo.objects.filter(profile=self.request.user)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user)

# Vue pour voir les likes sur les publications des femmes
class LikeListForWomenView(generics.ListAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated, IsWoman]

    def get_queryset(self):
        return Like.objects.filter(publication__profile=self.request.user)

# Vue pour voir les messages reçus par les femmes
class MessageListForWomenView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsWoman]

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user)

# VUES POUR LES HOMMES

# Vue pour voir les publications des femmes
class PublicationListForMenView(generics.ListAPIView):
    serializer_class = PublicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsMan]

    def get_queryset(self):
        return Publication.objects.filter(profile__sexe='F')

# Vue pour voir les photos publiées par les femmes
class PhotoListForMenView(generics.ListAPIView):
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticated, IsMan]

    def get_queryset(self):
        return Photo.objects.filter(profile__sexe='F')

# Vue pour permettre aux hommes de liker une publication
class LikeCreateView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated, IsMan]

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user)

# Vue pour permettre aux hommes de souscrire à un abonnement
class AbonnementCreateView(generics.CreateAPIView):
    serializer_class = AbonnementSerializer
    permission_classes = [permissions.IsAuthenticated, IsMan]

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user)

# Vue pour permettre aux hommes d'envoyer un message à une femme
class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsMan, HasActiveAbonnement]

    def perform_create(self, serializer):
        if not self.request.user.abonnements.filter(is_active=True).exists():
            raise serializers.ValidationError("Vous devez avoir un abonnement actif pour envoyer un message.")
        serializer.save(sender=self.request.user)

