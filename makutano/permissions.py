from rest_framework import permissions

class IsMan(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.sexe == 'H'

class IsWoman(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.sexe == 'F'

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.profile == request.user
    
from rest_framework import permissions

class HasActiveAbonnement(permissions.BasePermission):
    """
    Permission pour vérifier que l'utilisateur a un abonnement actif.
    """
    def has_permission(self, request, view):
        return request.user.abonnements.filter(is_active=True).exists()