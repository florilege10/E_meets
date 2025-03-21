from datetime import timedelta, timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class ProfileManager(BaseUserManager):
    def create_user(self, email, name, sexe, address, password=None):
        if not email:
            raise ValueError("L'email est obligatoire")
        if not name:
            raise ValueError("Le nom est obligatoire")
        if not sexe:
            raise ValueError("Le sexe est obligatoire")
        if not address:
            raise ValueError("L'adresse est obligatoire")
        if not password:
            raise ValueError("Le mot de passe est obligatoire")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, sexe=sexe, address=address)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, sexe, address, password=None):
        user = self.create_user(email, name, sexe, address, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Profile(AbstractBaseUser, PermissionsMixin):
    HOMME = "H"
    FEMME = "F"
    SEXE_CHOICES = [
        (HOMME, "Homme"),
        (FEMME, "Femme"),
    ]

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = ProfileManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "sexe", "address"]

    def __str__(self):
        return self.email

class Publication(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, limit_choices_to={'sexe': "F"}, default=1)
    image = models.ImageField(upload_to='publications/')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Publication de {self.profile.name} - {self.timestamp}"
    


class Photo(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo de {self.profile.name}" 
    




class Like(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='likes')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='likes')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile.name} a liké la photo {self.photo.id}"



class Abonnement(models.Model):
    DUREE_CHOICES = [
        (1, "1 jour"),
        (7, "1 semaine"),
        (30, "1 mois"),
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='abonnements')
    start_date = models.DateTimeField(auto_now_add=True)
    duration_days = models.IntegerField(choices=DUREE_CHOICES, default=1)
    tarif = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)

    @property
    def expires_at(self):
        return self.start_date + timedelta(days=self.duration_days)

    def is_currently_active(self):
        return timezone.now() < self.expires_at

    def __str__(self):
        return f"Abonnement de {self.profile.name} (Expire le {self.expires_at})"








class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='messages/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"Message de {self.sender.name} à {self.receiver.name}"