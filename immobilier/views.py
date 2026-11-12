from django.shortcuts import render, get_object_or_404
from .models import Bien


def liste_biens(request):
    biens = Bien.objects.select_related(
        "agent", "vendeur", "commune"
    ).order_by("id")

    return render(
        request,
        "immobilier/liste_biens.html",
        {"biens": biens}
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