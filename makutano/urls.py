from django.http import HttpResponseNotFound
from django.urls import path
from .views import (
    RegistrationView, CustomLoginView, LoginView, UserView,
    PublicationListForWomenView, PhotoListForWomenView, LikeListForWomenView, MessageListForWomenView,
    PublicationListForMenView, PhotoListForMenView, LikeCreateView, AbonnementCreateView, MessageCreateView
)

urlpatterns = [
    # URLs communes
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('custom-login/', CustomLoginView.as_view(), name='custom-login'),
    path('user/<int:pk>/', UserView.as_view(), name='user-detail'),
    
    # URLs pour les femmes
    path('women/publications/', PublicationListForWomenView.as_view(), name='publication-list-women'),
    path('women/photos/', PhotoListForWomenView.as_view(), name='photo-list-women'),
    path('women/likes/', LikeListForWomenView.as_view(), name='like-list-women'),
    path('women/messages/', MessageListForWomenView.as_view(), name='message-list-women'),
    
    # URLs pour les hommes
    path('men/publications/', PublicationListForMenView.as_view(), name='publication-list-men'),
    path('men/photos/', PhotoListForMenView.as_view(), name='photo-list-men'),
    path('men/likes/', LikeCreateView.as_view(), name='like-create-men'),
    path('men/abonnements/', AbonnementCreateView.as_view(), name='abonnement-create-men'),
    path('men/messages/', MessageCreateView.as_view(), name='message-create-men'),

    path('favicon.ico', lambda request: HttpResponseNotFound()),
]
