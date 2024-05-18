from django.db import models

class Utilisateur(models.Model):
    id_utilisateur = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    password = models.CharField(max_length=128)

    USERNAME_FIELD = 'nom'  # Définir le champ de nom d'utilisateur
    
    def __str__(self):
        return f'{self.nom}'

    class Meta:
        db_table = 'utilisateur'


class Taches(models.Model):
    STATUT_CHOICES = (
        ('En attente', 'En attente'),
        ('En cours', 'En cours'),
        ('fini', 'Fini'),
    )

    id_taches = models.AutoField(primary_key=True)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='taches')
    titre = models.CharField(max_length=255)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='En attente')
    date = models.DateField()

    

    def __str__(self):
        return self.titre

    class Meta:
        db_table = 'taches'
