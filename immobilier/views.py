from decimal import Decimal, InvalidOperation

from django.shortcuts import render, get_object_or_404

from .models import Bien, Commune


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