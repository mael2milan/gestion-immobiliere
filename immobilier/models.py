from django.db import models

class Agent(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Vendeur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Bien(models.Model):
    adresse = models.CharField(max_length=100)
    superficie = models.FloatField()
    prix_demande = models.DecimalField(max_digits=10,decimal_places=2)
    nb_chambres = models.PositiveIntegerField()
    nb_garages = models.PositiveIntegerField()
    agent = models.ForeignKey(
        Agent,
        on_delete = models.PROTECT,
        related_name = "biens"
    )
    vendeur = models.ForeignKey(
        Vendeur,
        on_delete = models.PROTECT,
        related_name = "biens"
    )

    def __str__(self):
        return f"{self.adresse} - {self.prix_demande}€"