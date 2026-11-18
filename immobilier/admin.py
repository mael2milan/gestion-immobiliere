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
    list_filter = ("type_bien", "etape_vente", "commune")
    list_editable = ("etape_vente",)
    search_fields = (
        "adresse", "commune__nom",
        "agent__nom", "vendeur__nom"
    )


@admin.register(Acheteur)
class AcheteurAdmin(admin.ModelAdmin):
    list_display = ("nom", "prenom", "budget_max", "agent")
    search_fields = ("nom", "prenom", "agent__nom")


@admin.register(Proposition)
class PropositionAdmin(admin.ModelAdmin):
    list_display = (
        "acheteur", "bien", "prix_presente",
        "decision", "date_proposition", "date_reponse"
    )
    list_filter = ("decision",)
    search_fields = ("acheteur__nom", "bien__adresse")


@admin.register(Visite)
class VisiteAdmin(admin.ModelAdmin):
    list_display = (
        "acheteur", "bien", "agent", "debut", "statut"
    )
    list_filter = ("statut", "agent")
    search_fields = ("acheteur__nom", "bien__adresse")


@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):
    list_display = (
        "acheteur", "bien", "montant", "statut", "date_offre"
    )
    list_filter = ("statut",)
    search_fields = ("acheteur__nom", "bien__adresse")


@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = (
        "agent", "vendeur", "objet", "debut", "statut"
    )
    list_filter = ("statut", "agent")


admin.site.register([Agent, Vendeur, Commune])