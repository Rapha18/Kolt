from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, nom_complet, numero_telephone, mot_de_passe=None):
        if not numero_telephone:
            raise ValueError("Le numéro de téléphone est obligatoire.")
        user = self.model(
            nom_complet=nom_complet,
            numero_telephone=numero_telephone,
        )
        user.set_password(mot_de_passe)
        user.save(using=self._db)
        return user

    def create_superuser(self, nom_complet, numero_telephone, mot_de_passe):
        user = self.create_user(
            nom_complet=nom_complet,
            numero_telephone=numero_telephone,
            mot_de_passe=mot_de_passe,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    nom_complet = models.CharField(max_length=255)
    numero_telephone = models.CharField(unique=True, max_length=15)
    solde = models.DecimalField(max_digits=10, decimal_places=2, default=50000)
    pin_code = models.CharField(max_length=4, default='1234')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'numero_telephone'
    REQUIRED_FIELDS = ['nom_complet']

    def __str__(self):
        return self.nom_complet

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class TransactionHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    TYPE_CHOICES = [
        ('recharge', 'Recharge'),
        ('retrait', 'Retrait'),
        ('transfert', 'Transfert'),
    ]
    type_transaction = models.CharField(max_length=10, choices=TYPE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

