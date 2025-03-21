
from django.contrib import admin
from .models import Profile, Publication, Like, Abonnement, Message, Photo

admin.site.register(Profile)
admin.site.register(Publication)
admin.site.register(Like)
admin.site.register(Abonnement)
admin.site.register(Message)
admin.site.register(Photo)