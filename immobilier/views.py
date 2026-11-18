from decimal import Decimal, InvalidOperation

from django.shortcuts import render, get_object_or_404

from .models import Bien, Acheteur, Vendeur, RendezVous, Commune

from .services import recommander_biens

def liste_biens(request):
    biens = Bien.objects.select_related(
        "agent", "vendeur", "commune"
    )

    commune = request.GET.get("commune", "")
    type_bien = request.GET.get("type_bien", "")
    prix_max = request.GET.get("prix_max", "")
    tri = request.GET.get("tri", "prix_croissant")

    erreur_prix = ""

    # Filtrage par commune
    if commune:
        biens = biens.filter(commune__code_insee=commune)

    # Filtrage par type de bien
    if type_bien in Bien.TypeBien.values:
        biens = biens.filter(type_bien=type_bien)

    # Filtrage par prix maximal
    if prix_max:
        try:
            prix = Decimal(prix_max.replace(",", "."))

            if prix.is_finite() and prix >= 0:
                biens = biens.filter(prix_demande__lte=prix)
            else:
                erreur_prix = "Saisis un prix positif valide."

        except InvalidOperation:
            erreur_prix = "Saisis un prix numérique valide."

    # Tri par prix
    tris_autorises = {
        "prix_croissant": "prix_demande",
        "prix_decroissant": "-prix_demande",
    }

    biens = biens.order_by(
        tris_autorises.get(tri, "prix_demande"),
        "pk",
    )

    return render(
        request,
        "immobilier/liste_biens.html",
        {
            "biens": biens,
            "communes": Commune.objects.order_by("nom"),
            "types_biens": Bien.TypeBien.choices,
            "commune_selectionnee": commune,
            "type_selectionne": type_bien,
            "prix_max": prix_max,
            "tri_selectionne": tri,
            "erreur_prix": erreur_prix,
        }
    )


def detail_bien(request, pk):
    bien = get_object_or_404(
        Bien.objects.select_related(
            "agent", "vendeur", "commune"
        ),
        pk=pk
    )

    return render(
        request,
        "immobilier/detail_bien.html",
        {"bien": bien}
    )

def liste_acheteurs(request):
    acheteurs = Acheteur.objects.select_related(
        "agent"
    ).order_by("nom", "prenom")

    return render(
        request,
        "immobilier/liste_acheteurs.html",
        {"acheteurs": acheteurs}
    )


def detail_acheteur(request, pk):
    acheteur = get_object_or_404(
        Acheteur.objects.select_related("agent")
        .prefetch_related("communes_recherchees"),
        pk=pk
    )

    recommandations = recommander_biens(acheteur)

    return render(
        request,
        "immobilier/detail_acheteur.html",
        {
            "acheteur": acheteur,
            "recommandations": recommandations,
        }
    )


def liste_vendeurs(request):
    vendeurs = Vendeur.objects.order_by("nom", "prenom")

    return render(
        request,
        "immobilier/liste_vendeurs.html",
        {"vendeurs": vendeurs}
    )


def detail_vendeur(request, pk):
    vendeur = get_object_or_404(Vendeur, pk=pk)

    biens = Bien.objects.filter(
        vendeur=vendeur
    ).select_related("commune", "agent").order_by("adresse")

    rendez_vous = RendezVous.objects.filter(
        vendeur=vendeur
    ).select_related("agent").order_by("debut")

    return render(
        request,
        "immobilier/detail_vendeur.html",
        {
            "vendeur": vendeur,
            "biens": biens,
            "rendez_vous": rendez_vous,
        }
    )