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

class Commune(models.Model):
    code_insee = models.CharField(max_length=5, primary_key=True)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Acheteur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    budget_max = models.DecimalField(max_digits=10,decimal_places=2)
    superficie_min = models.FloatField()
    chambres_min = models.PositiveIntegerField()
    garage_souhaite = models.BooleanField()
    agent = models.ForeignKey(
        Agent,
        on_delete = models.PROTECT,
        related_name = "acheteurs"
    )
    communes_recherchees = models.ManyToManyField(
        Commune,
        related_name = "acheteurs",
        blank = True
    )

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Proposition(models.Model):
    date_proposition = models.DateTimeField(auto_now_add=True)
    prix_presente = models.DecimalField(max_digits=10,decimal_places=2)
    decision = models.CharField(max_length=20)
    date_reponse = models.DateTimeField(null=True,blank=True)
    commentaire = models.TextField(blank=True)
    acheteur = models.ForeignKey(
        Acheteur,
        on_delete = models.PROTECT,
        related_name = "propositions"
    )
    bien = models.ForeignKey(
        Bien,
        on_delete = models.PROTECT,
        related_name = "propositions"
    )

    def __str__(self):
        return f"Proposition n°{self.pk} - {self.bien.adresse}"