
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Agent, Vendeur, Commune, Bien, Acheteur
from .services import score_compatibilite, recommander_biens


class RapprochementTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Données fictives uniquement pour les tests
        cls.commune = Commune.objects.create(
            code_insee="49007",
            nom="Angers"
        )

        cls.agent = Agent.objects.create(
            nom="Martin",
            prenom="Sophie",
            email="test.agent@example.com"
        )

        cls.vendeur = Vendeur.objects.create(
            nom="Bernard",
            prenom="Paul",
            telephone="0600000000"
        )

        cls.acheteur = Acheteur.objects.create(
            nom="Dupont",
            prenom="Alice",
            telephone="0611111111",
            budget_max=Decimal("250000.00"),
            superficie_min=60,
            chambres_min=2,
            garage_souhaite=True,
            agent=cls.agent
        )

        cls.acheteur.communes_recherchees.add(cls.commune)

        cls.bien = Bien.objects.create(
            adresse="10 rue des Tests",
            commune=cls.commune,
            type_bien=Bien.TypeBien.MAISON,
            etape_vente=Bien.EtapeVente.MISE_EN_VENTE,
            superficie=80,
            prix_demande=Decimal("230000.00"),
            nb_chambres=3,
            nb_garages=1,
            agent=cls.agent,
            vendeur=cls.vendeur
        )

    def test_compatibilite_parfaite(self):
        score = score_compatibilite(
            self.acheteur,
            self.bien,
            {"49007"}
        )

        self.assertEqual(score, 100)

    def test_compatibilite_approximative(self):
        self.bien.prix_demande = Decimal("260000.00")
        self.bien.superficie = 55

        score = score_compatibilite(
            self.acheteur,
            self.bien,
            {"49007"}
        )

        self.assertEqual(score, 75)

    def test_bien_en_compromis_non_recommande(self):
        self.bien.etape_vente = Bien.EtapeVente.COMPROMIS
        self.bien.save()

        recommandations = recommander_biens(self.acheteur)

        self.assertEqual(len(recommandations), 0)

    def test_bien_recommande(self):
        recommandations = recommander_biens(self.acheteur)

        self.assertEqual(len(recommandations), 1)
        self.assertEqual(recommandations[0]["score"], 100)
        self.assertEqual(recommandations[0]["bien"], self.bien)

    def test_page_detail_acheteur(self):
        url = reverse(
            "immobilier:detail_acheteur",
            args=[self.acheteur.pk]
        )

        reponse = self.client.get(url)

        self.assertEqual(reponse.status_code, 200)
        self.assertContains(reponse, "Alice")

    def test_filtre_commune(self):
        url = reverse("immobilier:liste_biens")

        reponse = self.client.get(url, {"commune": "49007"})
        self.assertIn(self.bien, reponse.context["biens"])

        reponse = self.client.get(url, {"commune": "44109"})
        self.assertNotIn(self.bien, reponse.context["biens"])

    def test_filtre_prix(self):
        url = reverse("immobilier:liste_biens")

        reponse = self.client.get(url, {"prix_max": "250000"})
        self.assertIn(self.bien, reponse.context["biens"])

        reponse = self.client.get(url, {"prix_max": "200000"})
        self.assertNotIn(self.bien, reponse.context["biens"])

    def test_bien_inexistant(self):
        url = reverse(
            "immobilier:detail_bien",
            args=[999999]
        )

        reponse = self.client.get(url)

        self.assertEqual(reponse.status_code, 404)

    def test_portefeuille_agent(self):
        url = reverse(
            "immobilier:detail_agent",
            args=[self.agent.pk]
        )

        reponse = self.client.get(url)

        self.assertEqual(reponse.status_code, 200)
        self.assertContains(reponse, self.bien.adresse)
        self.assertContains(reponse, self.acheteur.nom)
