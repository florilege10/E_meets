from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from .models import Profile, Publication, Like, Abonnement, Message, Photo
from .serializers import *
from .permissions import IsMan, IsOwnerOrReadOnly, IsWoman
from rest_framework.permissions import AllowAny, IsAuthenticated
from makutano import serializers






class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        return Response({
            'message': 'Utilisateur créé avec succès',
            'user_id': profile.id
        }, status=status.HTTP_201_CREATED)



class CustomLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        if user.sexe == 'H':
            return Response({
                'token': token.key,
                'redirect_url': '/men/publications/'
            }, status=status.HTTP_200_OK)
        elif user.sexe == 'F':
            return Response({
                'token': token.key,
                'redirect_url': '/women/publications/'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Sexe non reconnu'
            }, status=status.HTTP_400_BAD_REQUEST)












class PublicationListForMenView(generics.ListAPIView):
    serializer_class = PublicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsMan]

    def get_queryset(self):
        return Photo.objects.filter(profile__sexe='F')
    

class PublicationListForWomenView(generics.ListCreateAPIView):
    serializer_class = PublicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsWoman]

    def get_queryset(self):
        return Publication.objects.filter(profile=self.request.user)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user)








        

class LikeListForWomenView(generics.ListAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated, IsWoman]

    def get_queryset(self):
        return Like.objects.filter(publication__profile=self.request.user)

class MessageListForWomenView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsWoman]

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user)
    
 

 #Enregistrement de photos publier par les femmmes

class PhotoCreateView(generics.CreateAPIView):
    """
    Vue pour permettre aux femmes de publier des photos.
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticated, IsWoman]

    def perform_create(self, serializer):
        # Associe la photo au profil de l'utilisateur connecté
        serializer.save(profile=self.request.user)  





class PhotoListCreateView(generics.ListCreateAPIView):
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Photo.objects.filter(profile=self.request.user)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user)

class PhotoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Photo.objects.filter(profile=self.request.user)

class UserListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserDetailView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserUpdateView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class LoginFormView(APIView):
    """
    Vue pour la connexion des utilisateurs.
    """
    serializer_class = LoginFormSerializer  # Sérialiseur pour le formulaire interactif

    def post(self, request, *args, **kwargs):
        """
        Traite les requêtes POST pour la connexion.
        """
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.id,
            'email': user.email,
            'message': 'Connexion réussie'
        }, status=status.HTTP_200_OK)



class LoginView(APIView):
    permission_classes = [] 
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.id,
            'email': user.email,
            'message': 'Connexion réussie'
        }, status=status.HTTP_200_OK)






class LoginFormView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = LoginSerializer()
        form_fields = {
            field_name: {
                "type": field.__class__.__name__,
                "label": field.label if hasattr(field, 'label') else field_name,
                "required": field.required,
                "help_text": field.help_text if hasattr(field, 'help_text') else None,
                "style": field.style if hasattr(field, 'style') else None,
            }
            for field_name, field in serializer.fields.items()
        }
        return Response({"form": form_fields}, status=status.HTTP_200_OK)
    





class PhotoPublicationView(generics.CreateAPIView):
    serializer_class = PhotoPublicationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user)







# FOCTIONNALITE POUR L HOMME 
class PhotoListForMenView(generics.ListAPIView):
    """
    Vue pour permettre aux hommes de voir les photos publiées par les femmes.
    """
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticated, IsMan]

    def get_queryset(self):
        # Filtrer les photos publiées par les femmes
        return Photo.objects.filter(profile__sexe='F')
    



"""
Vue pour permettre aux hommes de liker une publication.
"""

class LikeCreateView(generics.CreateAPIView):
   
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated, IsMan]

    def perform_create(self, serializer):
        # Associe le like au profil de l'utilisateur connecté
        serializer.save(profile=self.request.user)



"""
    Vue pour permettre aux hommes de payer un abonnement.
"""
class AbonnementCreateView(generics.CreateAPIView):
    
    serializer_class = AbonnementSerializer
    permission_classes = [permissions.IsAuthenticated, IsMan]

    def perform_create(self, serializer):
        # Associe l'abonnement au profil de l'utilisateur connecté
        serializer.save(profile=self.request.user)


"""
    Vue pour permettre aux hommes de discuter avec une femme.
"""


from .permissions import IsMan, HasActiveAbonnement

class MessageCreateView(generics.CreateAPIView):
    """
    Vue pour permettre aux hommes de discuter avec une femme.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsMan, HasActiveAbonnement]

    def perform_create(self, serializer):
        # Vérifie que l'utilisateur a un abonnement actif
        if not self.request.user.abonnements.filter(is_active=True).exists():
            raise serializers.ValidationError("Vous devez avoir un abonnement actif pour envoyer un message.")
        
        # Associe le message à l'utilisateur connecté (sender)
        serializer.save(sender=self.request.user)