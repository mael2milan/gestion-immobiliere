from django.contrib import admin
from .models import (
    Agent, Vendeur, Commune, Bien, Acheteur,
    Proposition, Visite, RendezVous, Offre
)


@admin.register(Bien)
class BienAdmin(admin.ModelAdmin):
    list_display = (
        "id", "adresse", "type_bien",
        "prix_demande", "commune", "agent", "etape_vente"
    )
    list_filter = ("type_bien", "etape_vente")
    search_fields = (
        "adresse", "commune__nom",
        "agent__nom", "vendeur__nom"
    )


@admin.register(Acheteur)
class AcheteurAdmin(admin.ModelAdmin):
    list_display = (
        "nom", "prenom", "budget_max", "agent"
    )
    search_fields = (
        "nom", "prenom"
    )

admin.site.register([
    Agent, Vendeur, Commune,
    Proposition, Visite, RendezVous, Offre
])