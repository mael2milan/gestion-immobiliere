from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from immobilier.models import (
    Agent, Vendeur, Commune, Bien, Acheteur,
    Proposition, Visite, RendezVous, Offre
)


class Command(BaseCommand):
    help = "Génère des données fictives pour la démonstration."

    @transaction.atomic
    def handle(self, *args, **options):

        # 1. Communes
        communes = {}

        for code, nom in [
            ("49007", "Angers"),
            ("44109", "Nantes"),
            ("35238", "Rennes"),
            ("75056", "Paris"),
        ]:
            commune, _ = Commune.objects.update_or_create(
                code_insee=code,
                defaults={"nom": nom}
            )
            communes[code] = commune

        # 2. Agents
        agents = []

        for i, (prenom, nom) in enumerate([
            ("Sophie", "Laurent"),
            ("Thomas", "Petit"),
            ("Emma", "Moreau"),
        ], start=1):
            agent, _ = Agent.objects.update_or_create(
                email=f"agent.demo{i}@example.com",
                defaults={"prenom": prenom, "nom": nom}
            )
            agents.append(agent)

        # 3. Vendeurs
        vendeurs = []

        for i, (prenom, nom) in enumerate([
            ("Paul", "Bernard"),
            ("Julie", "Robert"),
            ("Marc", "Richard"),
        ], start=1):
            vendeur, _ = Vendeur.objects.update_or_create(
                telephone=f"07990001{i:02d}",
                defaults={"prenom": prenom, "nom": nom}
            )
            vendeurs.append(vendeur)

        # 4. Acheteurs et critères de recherche
        acheteurs = []

        donnees_acheteurs = [
            ("Alice", "Dupont", 250000, 60, 2, True, 0, ["49007", "44109"]),
            ("Hugo", "Martin", 200000, 45, 2, False, 1, ["44109"]),
            ("Léa", "Durand", 340000, 90, 3, True, 2, ["35238"]),
            ("Lucas", "Michel", 380000, 35, 1, False, 2, ["75056", "44109"]),
        ]

        for i, (prenom, nom, budget, surface, chambres, garage, agent_i, codes) in enumerate(
            donnees_acheteurs, start=1
        ):
            acheteur, _ = Acheteur.objects.update_or_create(
                telephone=f"07990002{i:02d}",
                defaults={
                    "prenom": prenom,
                    "nom": nom,
                    "budget_max": Decimal(budget),
                    "superficie_min": surface,
                    "chambres_min": chambres,
                    "garage_souhaite": garage,
                    "agent": agents[agent_i],
                }
            )

            acheteur.communes_recherchees.set(
                [communes[code] for code in codes]
            )
            acheteurs.append(acheteur)

        # 5. Biens immobiliers
        biens = []

        donnees_biens = [
            ("17 rue des Tilleuls", "49007", "maison", 82, 230000, 3, 1, 0, 0),
            ("24 rue du Port", "49007", "appartement", 65, 198000, 2, 0, 1, 1),
            ("8 rue des Jardins", "44109", "maison", 95, 279000, 3, 1, 0, 2),
            ("36 rue du Centre", "44109", "appartement", 55, 175000, 2, 0, 1, 0),
            ("11 rue des Écoles", "35238", "maison", 105, 320000, 4, 1, 2, 1),
            ("52 rue des Fleurs", "75056", "appartement", 40, 350000, 1, 0, 2, 2),
        ]

        for adresse, code, type_bien, surface, prix, chambres, garages, agent_i, vendeur_i in donnees_biens:
            bien, _ = Bien.objects.update_or_create(
                adresse=adresse,
                commune=communes[code],
                defaults={
                    "type_bien": type_bien,
                    "superficie": surface,
                    "prix_demande": Decimal(prix),
                    "nb_chambres": chambres,
                    "nb_garages": garages,
                    "agent": agents[agent_i],
                    "vendeur": vendeurs[vendeur_i],
                    "etape_vente": "mise_en_vente",
                }
            )
            biens.append(bien)

        # 6. Propositions
        maintenant = timezone.now()

        for acheteur_i, bien_i, decision, commentaire in [
            (0, 0, "interesse", "Le bien correspond aux attentes."),
            (0, 1, "refuse", "Absence de garage."),
            (1, 3, "en_attente", "En attente du retour de l'acheteur."),
            (2, 4, "interesse", "Visite souhaitée."),
        ]:
            Proposition.objects.update_or_create(
                acheteur=acheteurs[acheteur_i],
                bien=biens[bien_i],
                defaults={
                    "prix_presente": biens[bien_i].prix_demande,
                    "decision": decision,
                    "commentaire": commentaire,
                    "date_reponse": (
                        maintenant if decision != "en_attente" else None
                    ),
                }
            )

        # 7. Visites
        for acheteur_i, bien_i, jours, statut in [
            (0, 0, 2, "planifiee"),
            (1, 3, 4, "planifiee"),
            (2, 4, -2, "realisee"),
        ]:
            debut = maintenant + timedelta(days=jours)

            Visite.objects.update_or_create(
                acheteur=acheteurs[acheteur_i],
                bien=biens[bien_i],
                defaults={
                    "agent": biens[bien_i].agent,
                    "debut": debut,
                    "fin": debut + timedelta(hours=1),
                    "statut": statut,
                }
            )

        # 8. Rendez-vous vendeurs
        for i in range(2):
            debut = maintenant + timedelta(days=i + 3)

            RendezVous.objects.update_or_create(
                agent=agents[i],
                vendeur=vendeurs[i],
                objet="Suivi du mandat",
                defaults={
                    "debut": debut,
                    "fin": debut + timedelta(hours=1),
                    "statut": "planifie",
                }
            )

        # 9. Offres d'achat
        for acheteur_i, bien_i, montant, statut in [
            (0, 0, 220000, "en_attente"),
            (2, 4, 310000, "refusee"),
        ]:
            Offre.objects.update_or_create(
                acheteur=acheteurs[acheteur_i],
                bien=biens[bien_i],
                defaults={
                    "montant": Decimal(montant),
                    "statut": statut,
                }
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Données de démonstration générées avec succès !"
            )
        )

        for modele in [
            Commune, Agent, Vendeur, Acheteur, Bien,
            Proposition, Visite, RendezVous, Offre
        ]:
            self.stdout.write(
                f"{modele.__name__} : {modele.objects.count()}"
            )