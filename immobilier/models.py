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


class Commune(models.Model):
    code_insee = models.CharField(max_length=5, primary_key=True)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Bien(models.Model):
    class TypeBien(models.TextChoices):
        MAISON = "maison", "Maison"
        APPARTEMENT = "appartement", "Appartement"

    class EtapeVente(models.TextChoices):
        PROSPECTION = "prospection", "Prospection"
        ESTIMATION = "estimation", "Estimation"
        MISE_EN_VENTE = "mise_en_vente", "Mise en vente"
        COMPROMIS = "compromis", "Compromis signé"
        VENTE = "vente", "Vente signée"

    type_bien = models.CharField(
        max_length=20,
        choices=TypeBien.choices,
    )
    etape_vente = models.CharField(
        max_length=20,
        choices=EtapeVente.choices,
        default=EtapeVente.PROSPECTION,
    )
    commune = models.ForeignKey(
        Commune,
        on_delete=models.PROTECT,
        related_name="biens",
    )
    adresse = models.CharField(max_length=100)
    superficie = models.FloatField()
    prix_demande = models.DecimalField(max_digits=10, decimal_places=2)
    nb_chambres = models.PositiveIntegerField()
    nb_garages = models.PositiveIntegerField()
    agent = models.ForeignKey(
        Agent,
        on_delete=models.PROTECT,
        related_name="biens",
    )
    vendeur = models.ForeignKey(
        Vendeur,
        on_delete=models.PROTECT,
        related_name="biens",
    )

    def __str__(self):
        return f"{self.adresse} - {self.prix_demande}€"


class Acheteur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    budget_max = models.DecimalField(max_digits=10, decimal_places=2)
    superficie_min = models.FloatField()
    chambres_min = models.PositiveIntegerField()
    garage_souhaite = models.BooleanField()
    agent = models.ForeignKey(
        Agent,
        on_delete=models.PROTECT,
        related_name="acheteurs",
    )
    communes_recherchees = models.ManyToManyField(
        Commune,
        related_name="acheteurs",
        blank=True,
    )

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Proposition(models.Model):
    class Decision(models.TextChoices):
        EN_ATTENTE = "en_attente", "En attente"
        INTERESSE = "interesse", "Intéressé"
        REFUSE = "refuse", "Refusé"

    date_proposition = models.DateTimeField(auto_now_add=True)
    prix_presente = models.DecimalField(max_digits=10, decimal_places=2)
    decision = models.CharField(
        max_length=20,
        choices=Decision.choices,
        default=Decision.EN_ATTENTE,
    )
    date_reponse = models.DateTimeField(null=True, blank=True)
    commentaire = models.TextField(blank=True)
    acheteur = models.ForeignKey(
        Acheteur,
        on_delete=models.PROTECT,
        related_name="propositions",
    )
    bien = models.ForeignKey(
        Bien,
        on_delete=models.PROTECT,
        related_name="propositions",
    )

    def __str__(self):
        return f"Proposition n°{self.pk} - {self.bien.adresse}"


class Visite(models.Model):
    class Statut(models.TextChoices):
        PLANIFIEE = "planifiee", "Planifiée"
        REALISEE = "realisee", "Réalisée"
        ANNULEE = "annulee", "Annulée"

    debut = models.DateTimeField()
    fin = models.DateTimeField()
    statut = models.CharField(
        max_length=20,
        choices=Statut.choices,
        default=Statut.PLANIFIEE,
    )
    compte_rendu = models.TextField(blank=True)
    acheteur = models.ForeignKey(
        Acheteur,
        on_delete=models.PROTECT,
        related_name="visites",
    )
    bien = models.ForeignKey(
        Bien,
        on_delete=models.PROTECT,
        related_name="visites",
    )
    agent = models.ForeignKey(
        Agent,
        on_delete=models.PROTECT,
        related_name="visites",
    )

    def __str__(self):
        return f"Visite n°{self.pk}"


class RendezVous(models.Model):
    class Statut(models.TextChoices):
        PLANIFIE = "planifie", "Planifié"
        REALISE = "realise", "Réalisé"
        ANNULE = "annule", "Annulé"

    debut = models.DateTimeField()
    fin = models.DateTimeField()
    objet = models.CharField(max_length=200)
    statut = models.CharField(
        max_length=20,
        choices=Statut.choices,
        default=Statut.PLANIFIE,
    )
    agent = models.ForeignKey(
        Agent,
        on_delete=models.PROTECT,
        related_name="rendez_vous",
    )
    vendeur = models.ForeignKey(
        Vendeur,
        on_delete=models.PROTECT,
        related_name="rendez_vous",
    )

    def __str__(self):
        return f"Rendez-vous n°{self.pk} : {self.objet}"


class Offre(models.Model):
    class Statut(models.TextChoices):
        EN_ATTENTE = "en_attente", "En attente"
        ACCEPTEE = "acceptee", "Acceptée"
        REFUSEE = "refusee", "Refusée"
        RETIREE = "retiree", "Retirée"

    date_offre = models.DateTimeField(auto_now_add=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(
        max_length=20,
        choices=Statut.choices,
        default=Statut.EN_ATTENTE,
    )
    acheteur = models.ForeignKey(
        Acheteur,
        on_delete=models.PROTECT,
        related_name="offres",
    )
    bien = models.ForeignKey(
        Bien,
        on_delete=models.PROTECT,
        related_name="offres",
    )

    def __str__(self):
        return f"Offre n°{self.pk} : {self.montant} €"
