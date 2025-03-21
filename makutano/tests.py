from multiprocessing.connection import Client
from unittest import TestCase
from django.middleware.csrf import get_token
from django.urls import reverse

from makutano.models import User

class AdminUserTests(TestCase):
    def setUp(self):
        # Créer un superutilisateur pour accéder à l'interface d'administration
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
            sexe='H'  # Homme
        )
        self.client = Client()
        self.client.force_login(self.admin_user)

        # Créer un utilisateur normal pour tester les modifications
        self.user = User.objects.create_user(
            username='testuserder',
            email='teste@example.com',
            password='testepassword',
            sexe='F'  # Femme
        )

    def test_user_sexe_field_in_admin(self):
        """
        Teste que le champ 'sexe' est correctement affiché et modifiable dans l'interface d'administration.
        """
        # URL pour modifier l'utilisateur dans l'interface d'administration
        url = reverse('admin:makutano_user_change', args=[self.user.id])
        response = self.client.get(url)

        # Vérifier que la page de modification de l'utilisateur est accessible
        self.assertEqual(response.status_code, 200)

        # Extraire le jeton CSRF
        csrf_token = get_token(self.client)

        # Modifier le champ 'sexe' de l'utilisateur
        data = {
            'username': 'testcduser',
            'email': 'testcd@example.com',
            'sexe': 'H',  # Changer de Femme (F) à Homme (H)
            'role': 'user',
            'csrfmiddlewaretoken': csrf_token,  # Ajouter le jeton CSRF
        }
        response = self.client.post(url, data)

        # Vérifier que la modification a été enregistrée
        self.assertEqual(response.status_code, 302)  # Redirection après succès
        self.user.refresh_from_db()
        self.assertEqual(self.user.sexe, 'H')  # Vérifier que le sexe a été mis à jour