from django.urls import path
from .views import (
     LoginFormView, LoginView, PhotoListForMenView, PhotoPublicationView, PublicationListForMenView, LikeCreateView, AbonnementCreateView, MessageCreateView,
    PublicationListForWomenView, LikeListForWomenView, MessageListForWomenView, PhotoListCreateView,
    PhotoRetrieveUpdateDestroyView, RegistrationView, UserListView, UserDetailView, UserUpdateView, CustomLoginView
)



urlpatterns = [
    
    
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('login-form/', LoginFormView.as_view(), name='login_form'),  # Pour obtenir les métadonnées du formulaire         # Pour soumettre le formulaire de connexion

    path('publish-photo/', PhotoPublicationView.as_view(), name='publish-photo'),

    path('men/publications/', PublicationListForMenView.as_view(), name='publication-list-men'),
    path('men/likes/', LikeCreateView.as_view(), name='like-create'),
    path('men/abonnements/', AbonnementCreateView.as_view(), name='abonnement-create'),
    path('men/messages/', MessageCreateView.as_view(), name='message-create'),
    path('men/photos/', PhotoListForMenView.as_view(), name='photo-list-for-men'),


    path('women/publications/', PublicationListForWomenView.as_view(), name='publication-list-women'),
    path('women/likes/', LikeListForWomenView.as_view(), name='like-list-women'),
    path('women/messages/', MessageListForWomenView.as_view(), name='message-list-women'),
    path('photos/', PhotoListCreateView.as_view(), name='photo-list-create'),
    path('photos/<int:pk>/', PhotoRetrieveUpdateDestroyView.as_view(), name='photo-retrieve-update-destroy'),
    
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('api/login/', LoginFormView.as_view(), name='login-form'),
]