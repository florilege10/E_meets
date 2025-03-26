from django.contrib import admin
from django.http import HttpResponseNotFound
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from makutano.views import *

urlpatterns = [
    path('', home, name='home'), 
    path('admin/', admin.site.urls),
       path('', home, name='home'), 
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
    
    
     # Remplacez par les URLs de votre application
]

# Ajouter les URLs pour les fichiers multimédias en mode développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)